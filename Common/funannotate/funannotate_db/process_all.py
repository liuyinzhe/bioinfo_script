#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# funannotate setup - Process Phase (standalone)
# ============================================================================
# Processes downloaded database files: decompresses archives, reformats
# sequences, builds diamond/HMMER indexes, extracts metadata, and generates
# funannotate-db-info.txt.
#
# ZERO dependencies on the funannotate Python package.
# Requires these external tools on PATH:
#   - diamond   (for merops, uniprot, repeats, mibig)
#   - hmmpress  (for dbCAN, pfam) — part of HMMER suite
#   - gunzip, tar (always available on Linux)
#
# Usage:
#   python process_all.py -d /path/to/funannotate_db [-i all] [-b dikarya]
#   python process_all.py -d /path/to/funannotate_db -i merops,uniprot
#   python process_all.py -d /path/to/funannotate_db --force
#
# Options:
#   -d DIR    Database directory (required) — also reads $FUNANNOTATE_DB
#   -i LIST   Comma-separated DBs to process (default: all)
#   -b LIST   BUSCO lineages to process (default: dikarya)
#   -f        Force reprocessing even if already done
#   -h        Show help
# ============================================================================

import os
import sys
import re
import io
import gzip
import hashlib
import shutil
import subprocess
import datetime
import argparse
import json
from xml.etree import cElementTree


# ═══════════════════════════════════════════════════════════════════════════
# Logging (standalone, no funannotate dependency)
# ═══════════════════════════════════════════════════════════════════════════

class Logger:
    """Minimal replacement for funannotate.library's logger."""
    def __init__(self):
        self._log = []

    def info(self, msg):
        print(f"[{datetime.datetime.now():%H:%M:%S}] INFO:  {msg}")

    def debug(self, msg):
        print(f"[{datetime.datetime.now():%H:%M:%S}] DEBUG: {msg}")

    def error(self, msg):
        print(f"[{datetime.datetime.now():%H:%M:%S}] ERROR: {msg}", file=sys.stderr)

    def warn(self, msg):
        print(f"[{datetime.datetime.now():%H:%M:%S}] WARN:  {msg}")

log = Logger()


# ═══════════════════════════════════════════════════════════════════════════
# Utility functions (standalone equivalents of funannotate.library)
# ═══════════════════════════════════════════════════════════════════════════

def calcmd5(filepath):
    """Calculate MD5 checksum of a local file."""
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def countfasta(input_path):
    """Count FASTA records (> lines) in a file (supports gzip)."""
    count = 0
    # Detect gzip magic
    with open(input_path, 'rb') as probe:
        magic = probe.read(2)
    opener = gzip.open if magic == b'\x1f\x8b' else open
    with opener(input_path, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('>'):
                count += 1
    return count


def run_cmd(cmd, cwd=None, check=True):
    """Run a subprocess command. Returns True on success."""
    log.debug(" ".join(cmd))
    try:
        result = subprocess.run(
            cmd, cwd=cwd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        if result.stdout:
            log.debug(result.stdout.strip())
        if result.stderr:
            # HMMER writes info to stderr; only log at debug level
            log.debug(result.stderr.strip())
        if check and result.returncode != 0:
            log.error(f"Command failed (exit {result.returncode}): {' '.join(cmd)}")
            log.error(result.stderr.strip())
            return False
        return True
    except FileNotFoundError as e:
        log.error(f"Executable not found: {cmd[0]} — is it installed and on PATH?")
        raise


def require_tool(name, hint=None):
    """Verify an external tool is on PATH. Exits if not found."""
    if shutil.which(name) is None:
        hint_msg = f" ({hint})" if hint else ""
        log.error(f"Required tool not found: {name}{hint_msg}")
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════
# Database info tracking (mirrors funannotate-db-info.txt format)
# ═══════════════════════════════════════════════════════════════════════════

DBINFO = {}  # key -> (type, name, version, date, num_records, md5)


def load_existing_info(fundb):
    """Load existing funannotate-db-info.txt if present."""
    dbfile = os.path.join(fundb, 'funannotate-db-info.txt')
    if os.path.isfile(dbfile):
        with open(dbfile, 'r') as f:
            for line in f:
                line = line.strip()
                try:
                    db, typ, name, version, date, records, checksum = line.split('\t')
                    DBINFO[db] = (typ, name, version, date, int(records), checksum)
                except ValueError:
                    pass
    return DBINFO


def write_info_file(fundb):
    """Write DBINFO dictionary to funannotate-db-info.txt."""
    dbfile = os.path.join(fundb, 'funannotate-db-info.txt')
    with open(dbfile, 'w') as out:
        for k, v in sorted(DBINFO.items()):
            line = f"{k}\t{v[0]}\t{v[1]}\t{v[2]}\t{v[3]}\t{v[4]}\t{v[5]}\n"
            out.write(line)
    log.info(f"Database info written to: {dbfile}")


# ═══════════════════════════════════════════════════════════════════════════
# Database processors
# ═══════════════════════════════════════════════════════════════════════════

def process_merops(fundb, force=False, today=None):
    """
    MEROPS database: reformat headers, build diamond DB.
    Input:  meropsscan.lib
    Output: merops.formatted.fa, merops.dmnd
    """
    log.info("=== Processing MEROPS database ===")

    fasta = os.path.join(fundb, 'meropsscan.lib')
    filtered = os.path.join(fundb, 'merops.formatted.fa')
    database = os.path.join(fundb, 'merops.dmnd')

    if not os.path.isfile(fasta):
        log.error(f"Input file not found: {fasta} — run download_all.sh first")
        return None

    if not force and os.path.isfile(database) and 'merops' in DBINFO:
        log.info("MEROPS already processed, skipping (use --force to redo)")
        return DBINFO['merops']

    # Clean old outputs
    for f in [filtered, database]:
        if os.path.isfile(f):
            os.remove(f)

    # Reformat FASTA headers: add family ID from comment
    with open(filtered, 'w') as out:
        with io.open(fasta, encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                if line.startswith('>'):
                    line = line.rstrip()
                    ID = line.split()[0]
                    try:
                        family = line.split('#')[1]
                    except IndexError:
                        family = 'unknown'
                    out.write(f'{ID} {family}\n')
                else:
                    out.write(line)

    # Build diamond database
    log.info("Building diamond DB for MEROPS...")
    cmd = ['diamond', 'makedb', '--in', 'merops.formatted.fa', '--db', 'merops']
    run_cmd(cmd, cwd=fundb)

    md5 = calcmd5(fasta)
    num = countfasta(filtered)
    DBINFO['merops'] = ('diamond', database, '12.5', '2023-01-19', num, md5)
    log.info(f"MEROPS: {num:,} records processed")
    return DBINFO['merops']


def process_uniprot(fundb, force=False, today=None):
    """
    UniProtKB/SwissProt: decompress, build diamond, extract release info.
    Input:  uniprot_sprot.fasta.gz, uniprot.release-date.txt
    Output: uniprot_sprot.fasta, uniprot.dmnd
    """
    log.info("=== Processing UniProtKB/SwissProt database ===")

    fasta_gz = os.path.join(fundb, 'uniprot_sprot.fasta.gz')
    fasta = os.path.join(fundb, 'uniprot_sprot.fasta')
    versionfile = os.path.join(fundb, 'uniprot.release-date.txt')
    database = os.path.join(fundb, 'uniprot.dmnd')

    if not os.path.isfile(fasta_gz):
        log.error(f"Input file not found: {fasta_gz} — run download_all.sh first")
        return None

    if not force and os.path.isfile(database) and 'uniprot' in DBINFO:
        log.info("UniProt already processed, skipping (use --force to redo)")
        return DBINFO['uniprot']

    # Clean old outputs
    for f in [fasta, database]:
        if os.path.isfile(f):
            os.remove(f)

    # Decompress
    log.info("Decompressing UniProt FASTA...")
    run_cmd(['gunzip', '-f', 'uniprot_sprot.fasta.gz'], cwd=fundb)

    # Parse release date and version
    unidate = today
    univers = 'unknown'
    if os.path.isfile(versionfile):
        md5 = calcmd5(versionfile)
        with io.open(versionfile, encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('UniProtKB/Swiss-Prot Release'):
                    rest, datepart = line.split(' of ')
                    try:
                        unidate = datetime.datetime.strptime(
                            datepart.rstrip(), "%d-%b-%Y"
                        ).strftime("%Y-%m-%d")
                    except ValueError:
                        unidate = today
                    univers = rest.split(' ')[-1]
    else:
        md5 = calcmd5(fasta)

    # Build diamond database
    log.info("Building diamond DB for UniProt...")
    cmd = ['diamond', 'makedb', '--in', 'uniprot_sprot.fasta', '--db', 'uniprot']
    run_cmd(cmd, cwd=fundb)

    num = countfasta(fasta)
    DBINFO['uniprot'] = ('diamond', database, univers, unidate, num, md5)
    log.info(f"UniProt: version={univers} date={unidate} records={num:,}")
    return DBINFO['uniprot']


def process_dbcan(fundb, force=False, today=None):
    """
    dbCAN CAZyme HMMs: reformat NAME lines, hmmpress.
    Input:  dbCAN.tmp (raw HMM), dbCAN-fam-HMMs.txt, dbCAN.changelog.txt
    Output: dbCAN.hmm + .h3{m,f,i,p}
    """
    log.info("=== Processing dbCAN database ===")

    raw_hmm = os.path.join(fundb, 'dbCAN.tmp')
    hmm = os.path.join(fundb, 'dbCAN.hmm')
    versionfile = os.path.join(fundb, 'dbCAN.changelog.txt')

    if not os.path.isfile(raw_hmm):
        log.error(f"Input file not found: {raw_hmm} — run download_all.sh first")
        return None

    if not force and os.path.isfile(hmm + '.h3m') and 'dbCAN' in DBINFO:
        log.info("dbCAN already processed, skipping (use --force to redo)")
        return DBINFO['dbCAN']

    # Clean old outputs
    for f in [hmm, hmm + '.h3m', hmm + '.h3f', hmm + '.h3i', hmm + '.h3p']:
        if os.path.isfile(f):
            os.remove(f)

    # Reformat: strip ".hmm" suffix from NAME lines
    num_records = 0
    with open(hmm, 'w') as out:
        with io.open(raw_hmm, encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                if line.startswith('NAME'):
                    num_records += 1
                    line = line.replace('.hmm\n', '\n').replace('.hmm\r\n', '\r\n').replace('.hmm\r', '\r')
                out.write(line)

    # Parse version info from changelog
    dbdate = today
    dbvers = 'V12'
    if os.path.isfile(versionfile):
        with io.open(versionfile, encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        if len(lines) >= 2:
            dbdate = lines[1].replace('# ', '').strip()
            dbvers = lines[0].strip().split(' ')[-1]
        try:
            dbdate = datetime.datetime.strptime(dbdate, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass

    md5 = calcmd5(raw_hmm)

    # Build HMMER database
    log.info("Pressing dbCAN HMM database...")
    cmd = ['hmmpress', '-f', 'dbCAN.hmm']
    run_cmd(cmd, cwd=fundb)

    # Cleanup temp file
    if os.path.isfile(raw_hmm):
        os.remove(raw_hmm)

    DBINFO['dbCAN'] = ('hmmer3', hmm, dbvers, dbdate, num_records, md5)
    log.info(f"dbCAN: version={dbvers} date={dbdate} records={num_records:,}")
    return DBINFO['dbCAN']


def process_pfam(fundb, force=False, today=None):
    """
    Pfam HMMs: decompress, hmmpress, extract metadata.
    Input:  Pfam-A.hmm.gz, Pfam-A.clans.tsv.gz, Pfam.version.gz
    Output: Pfam-A.hmm + .h3{m,f,i,p}
    """
    log.info("=== Processing Pfam database ===")

    hmm = os.path.join(fundb, 'Pfam-A.hmm')
    hmm_gz = hmm + '.gz'
    version_gz = os.path.join(fundb, 'Pfam.version.gz')
    versionfile = os.path.join(fundb, 'Pfam.version')
    clans_gz = os.path.join(fundb, 'Pfam-A.clans.tsv.gz')

    if not os.path.isfile(hmm_gz):
        log.error(f"Input file not found: {hmm_gz} — run download_all.sh first")
        return None

    if not force and os.path.isfile(hmm + '.h3m') and 'pfam' in DBINFO:
        log.info("Pfam already processed, skipping (use --force to redo)")
        return DBINFO['pfam']

    # Clean old outputs
    for f in [hmm, hmm + '.h3m', hmm + '.h3f', hmm + '.h3i', hmm + '.h3p', versionfile]:
        if os.path.isfile(f):
            os.remove(f)

    # Decompress all
    log.info("Decompressing Pfam files...")
    run_cmd(['gunzip', '-f', 'Pfam-A.hmm.gz'], cwd=fundb)
    run_cmd(['gunzip', '-f', 'Pfam-A.clans.tsv.gz'], cwd=fundb)
    md5 = calcmd5(version_gz)  # MD5 of compressed version file (matches original)
    run_cmd(['gunzip', '-f', 'Pfam.version.gz'], cwd=fundb)

    # Parse version info
    pfamdate = today
    pfamvers = 'unknown'
    num_records = 0
    if os.path.isfile(versionfile):
        with io.open(versionfile, encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('Pfam release'):
                    pfamvers = line.split(': ')[-1].strip()
                if line.startswith('Pfam-A families'):
                    try:
                        num_records = int(line.split(': ')[-1].strip())
                    except ValueError:
                        pass
                if line.startswith('Date'):
                    pfamdate = line.split(': ')[-1].strip()

    # Build HMMER database
    log.info("Pressing Pfam HMM database...")
    cmd = ['hmmpress', '-f', 'Pfam-A.hmm']
    run_cmd(cmd, cwd=fundb)

    DBINFO['pfam'] = ('hmmer3', hmm, pfamvers, pfamdate, num_records, md5)
    log.info(f"Pfam: version={pfamvers} date={pfamdate} records={num_records:,}")
    return DBINFO['pfam']


def process_repeats(fundb, force=False, today=None):
    """
    Repeat proteins: extract tar.gz, reformat headers, build diamond.
    Input:  funannotate.repeat.proteins.fa.tar.gz
    Output: funannotate.repeat.proteins.fa, funannotate.repeats.reformat.fa, repeats.dmnd
    """
    log.info("=== Processing Repeat proteins database ===")

    tar_file = os.path.join(fundb, 'funannotate.repeat.proteins.fa.tar.gz')
    fasta = os.path.join(fundb, 'funannotate.repeat.proteins.fa')
    filtered = os.path.join(fundb, 'funannotate.repeats.reformat.fa')
    database = os.path.join(fundb, 'repeats.dmnd')

    if not os.path.isfile(tar_file):
        log.error(f"Input file not found: {tar_file} — run download_all.sh first")
        return None

    if not force and os.path.isfile(database) and 'repeats' in DBINFO:
        log.info("Repeats already processed, skipping (use --force to redo)")
        return DBINFO['repeats']

    # Clean old outputs
    for f in [fasta, filtered, database]:
        if os.path.isfile(f):
            os.remove(f)

    # Extract
    log.info("Extracting repeat proteins archive...")
    run_cmd(['tar', '-zxf', 'funannotate.repeat.proteins.fa.tar.gz'], cwd=fundb)

    md5 = calcmd5(tar_file)

    # Reformat headers (clean up messy repeat FASTA headers)
    with open(filtered, 'w') as out:
        with io.open(fasta, encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                if line.startswith('>'):
                    line = line.replace('#', '_')
                    line = line.replace('/', '-')
                    line = line.replace('&', '')
                out.write(line)

    # Build diamond database
    log.info("Building diamond DB for repeats...")
    cmd = ['diamond', 'makedb', '--in', 'funannotate.repeats.reformat.fa',
           '--db', 'repeats', '-parse_seqids']
    run_cmd(cmd, cwd=fundb)

    num = countfasta(filtered)
    DBINFO['repeats'] = ('diamond', database, '1.0', today, num, md5)
    log.info(f"Repeats: {num:,} records processed")
    return DBINFO['repeats']


def process_go(fundb, force=False, today=None):
    """
    GO Ontology: parse OBO for version and term count.
    Input:  go.obo
    Output: (metadata only, no index building)
    """
    log.info("=== Processing GO Ontology ===")

    go_obo = os.path.join(fundb, 'go.obo')

    if not os.path.isfile(go_obo):
        log.error(f"Input file not found: {go_obo} — run download_all.sh first")
        return None

    if not force and 'go' in DBINFO:
        log.info("GO already processed, skipping (use --force to redo)")
        return DBINFO['go']

    md5 = calcmd5(go_obo)
    num_records = 0
    version = today
    with io.open(go_obo, encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('data-version:'):
                version = line.split(' ')[1].strip().replace('releases/', '')
            if line.startswith('[Term]'):
                num_records += 1

    DBINFO['go'] = ('text', go_obo, version, version, num_records, md5)
    log.info(f"GO: version={version} terms={num_records:,}")
    return DBINFO['go']


def process_mibig(fundb, force=False, today=None):
    """
    MiBIG secondary metabolism: build diamond DB.
    Input:  mibig.fa
    Output: mibig.dmnd
    """
    log.info("=== Processing MiBIG database ===")

    fasta = os.path.join(fundb, 'mibig.fa')
    database = os.path.join(fundb, 'mibig.dmnd')

    if not os.path.isfile(fasta):
        log.error(f"Input file not found: {fasta} — run download_all.sh first")
        return None

    if not force and os.path.isfile(database) and 'mibig' in DBINFO:
        log.info("MiBIG already processed, skipping (use --force to redo)")
        return DBINFO['mibig']

    # Clean old outputs
    if os.path.isfile(database):
        os.remove(database)

    md5 = calcmd5(fasta)

    # Extract version from filename: mibig_prot_seqs_1.4.fasta -> 1.4
    basename = os.path.basename(fasta)
    try:
        version = basename.split('_')[-1].replace('.fasta', '').replace('.fa', '')
    except Exception:
        version = 'unknown'

    # Build diamond database
    log.info("Building diamond DB for MiBIG...")
    cmd = ['diamond', 'makedb', '--in', 'mibig.fa', '--db', 'mibig']
    run_cmd(cmd, cwd=fundb)

    num = countfasta(fasta)
    DBINFO['mibig'] = ('diamond', database, version, today, num, md5)
    log.info(f"MiBIG: version={version} records={num:,}")
    return DBINFO['mibig']


def process_interpro(fundb, force=False, today=None):
    """
    InterProScan XML: decompress, parse metadata from XML.
    Input:  interpro.xml.gz
    Output: interpro.xml (decompressed)
    """
    log.info("=== Processing InterPro database ===")

    ipr_gz = os.path.join(fundb, 'interpro.xml.gz')
    ipr_xml = os.path.join(fundb, 'interpro.xml')

    if not os.path.isfile(ipr_gz):
        log.error(f"Input file not found: {ipr_gz} — run download_all.sh first")
        return None

    if not force and 'interpro' in DBINFO:
        log.info("InterPro already processed, skipping (use --force to redo)")
        return DBINFO['interpro']

    # Clean old outputs
    if os.path.isfile(ipr_xml):
        os.remove(ipr_xml)

    md5 = calcmd5(ipr_gz)

    # Decompress
    log.info("Decompressing InterPro XML...")
    run_cmd(['gunzip', '-f', 'interpro.xml.gz'], cwd=fundb)

    # Parse XML for metadata
    num_records = 0
    version = 'unknown'
    iprdate = today
    try:
        for event, elem in cElementTree.iterparse(ipr_xml):
            if elem.tag == 'release':
                for x in list(elem):
                    if x.attrib.get('dbname') == 'INTERPRO':
                        num_records = int(x.attrib.get('entry_count', 0))
                        version = x.attrib.get('version', 'unknown')
                        iprdate = x.attrib.get('file_date', today)
                elem.clear()  # Free memory
    except cElementTree.ParseError as e:
        log.warn(f"XML parse warning (metadata may be incomplete): {e}")

    try:
        iprdate = datetime.datetime.strptime(iprdate, "%d-%b-%y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            iprdate = datetime.datetime.strptime(iprdate, "%d-%b-%Y").strftime("%Y-%m-%d")
        except ValueError:
            iprdate = today

    DBINFO['interpro'] = ('xml', ipr_xml, version, iprdate, num_records, md5)
    log.info(f"InterPro: version={version} date={iprdate} entries={num_records:,}")
    return DBINFO['interpro']


def process_busco_outgroups(fundb, force=False, today=None):
    """
    BUSCO outgroups: extract tar.gz.
    Input:  busco_outgroups.tar.gz
    Output: outgroups/ directory
    """
    log.info("=== Processing BUSCO outgroups ===")

    tar_file = os.path.join(fundb, 'busco_outgroups.tar.gz')
    outgroups_dir = os.path.join(fundb, 'outgroups')

    if not os.path.isfile(tar_file):
        log.error(f"Input file not found: {tar_file} — run download_all.sh first")
        return None

    if not force and os.path.isdir(outgroups_dir) and 'busco_outgroups' in DBINFO:
        log.info("BUSCO outgroups already processed, skipping (use --force to redo)")
        return DBINFO['busco_outgroups']

    # Clean old outputs
    if os.path.isdir(outgroups_dir):
        shutil.rmtree(outgroups_dir)

    md5 = calcmd5(tar_file)

    # Extract
    log.info("Extracting BUSCO outgroups...")
    run_cmd(['tar', '-zxf', 'busco_outgroups.tar.gz'], cwd=fundb)

    num = len([n for n in os.listdir(outgroups_dir)
               if os.path.isfile(os.path.join(outgroups_dir, n)) and not n.startswith('.')])

    DBINFO['busco_outgroups'] = ('outgroups', outgroups_dir, '1.0', today, num, md5)
    log.info(f"BUSCO outgroups: {num} group files")
    return DBINFO['busco_outgroups']


def process_gene2product(fundb, force=False, today=None):
    """
    Curated gene names and product descriptions: parse metadata.
    Input:  ncbi_cleaned_gene_products.txt
    Output: (metadata only)
    """
    log.info("=== Processing gene2product database ===")

    curated = os.path.join(fundb, 'ncbi_cleaned_gene_products.txt')

    if not os.path.isfile(curated):
        log.error(f"Input file not found: {curated} — run download_all.sh first")
        return None

    if not force and 'gene2product' in DBINFO:
        log.info("gene2product already processed, skipping (use --force to redo)")
        return DBINFO['gene2product']

    md5 = calcmd5(curated)
    num_records = 0
    curdate = today
    version = 'unknown'
    with io.open(curated, encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('#version'):
                version = line.split(' ')[-1].strip()
            elif line.startswith('#Date'):
                curdate = line.split(' ')[-1].strip()
            else:
                num_records += 1

    try:
        curdate = datetime.datetime.strptime(curdate, "%m-%d-%Y").strftime("%Y-%m-%d")
    except ValueError:
        curdate = today

    DBINFO['gene2product'] = ('text', curated, version, curdate, num_records, md5)
    log.info(f"gene2product: version={version} date={curdate} records={num_records:,}")
    return DBINFO['gene2product']


def process_busco(fundb, lineages, force=False):
    """
    BUSCO lineage models: extract tar.gz, rename folder.
    Input:  <lineage>.tar.gz per lineage
    Output: <lineage>/ directory per lineage
    """
    log.info(f"=== Processing BUSCO lineages: {lineages} ===")

    # BUSCO lineage dir mapping (matches downloads.json)
    busco_dirs = {
        'fungi': 'fungi_odb9',
        'microsporidia': 'microsporidia_odb9',
        'dikarya': 'dikarya_odb9',
        'ascomycota': 'ascomycota_odb9',
        'pezizomycotina': 'pezizomycotina_odb9',
        'eurotiomycetes': 'eurotiomycetes_odb9',
        'sordariomycetes': 'sordariomyceta_odb9',
        'saccharomycetes': 'saccharomyceta_odb9',
        'saccharomycetales': 'saccharomycetales_odb9',
        'basidiomycota': 'basidiomycota_odb9',
        'eukaryota': 'eukaryota_odb9',
        'protists': 'protists_ensembl',
        'alveolata_stramenophiles': 'alveolata_stramenophiles_ensembl',
        'metazoa': 'metazoa_odb9',
        'nematoda': 'nematoda_odb9',
        'arthropoda': 'arthropoda_odb9',
        'insecta': 'insecta_odb9',
        'endopterygota': 'endopterygota_odb9',
        'hymenoptera': 'hymenoptera_odb9',
        'diptera': 'diptera_odb9',
        'vertebrata': 'vertebrata_odb9',
        'actinopterygii': 'actinopterygii_odb9',
        'tetrapoda': 'tetrapoda_odb9',
        'aves': 'aves_odb9',
        'mammalia': 'mammalia_odb9',
        'euarchontoglires': 'euarchontoglires_odb9',
        'laurasiatheria': 'laurasiatheria_odb9',
        'embryophyta': 'embryophyta_odb9',
    }

    for lineage in lineages:
        if lineage not in busco_dirs:
            log.warn(f"Unknown BUSCO lineage: {lineage} — skipping")
            continue

        log.info(f"--- BUSCO lineage: {lineage} ---")
        tar_file = os.path.join(fundb, f"{lineage}.tar.gz")
        target_dir = os.path.join(fundb, lineage)
        extracted_dir = os.path.join(fundb, busco_dirs[lineage])

        if not os.path.isfile(tar_file):
            log.warn(f"BUSCO tar not found: {tar_file} — download it first")
            continue

        if not force and os.path.isdir(target_dir):
            log.info(f"  BUSCO {lineage} already processed, skipping")
            continue

        # Clean old dirs
        if os.path.isdir(target_dir):
            shutil.rmtree(target_dir)
        if os.path.isdir(extracted_dir):
            shutil.rmtree(extracted_dir)

        # Extract
        log.info(f"  Extracting {lineage}.tar.gz...")
        run_cmd(['tar', '-zxf', f"{lineage}.tar.gz"], cwd=fundb)

        # Rename extracted folder to lineage name
        if os.path.isdir(extracted_dir) and extracted_dir != target_dir:
            os.rename(extracted_dir, target_dir)
            log.info(f"  Renamed: {busco_dirs[lineage]} -> {lineage}")
        elif not os.path.isdir(target_dir):
            log.warn(f"  Extracted directory not found: expected {extracted_dir} or {target_dir}")

    log.info("BUSCO lineages processed.")


def setup_augustus_species(fundb, force=False):
    """
    Copy Augustus pre-trained species into the database.
    Requires $AUGUSTUS_CONFIG_PATH to be set.
    Creates trained_species/<name>/augustus/ and info.json per species.
    """
    augustus_config = os.environ.get("AUGUSTUS_CONFIG_PATH", "")
    if not augustus_config:
        log.warn("$AUGUSTUS_CONFIG_PATH not set — skipping Augustus species setup")
        return

    species_src_dir = os.path.join(augustus_config, 'species')
    if not os.path.isdir(species_src_dir):
        log.warn(f"Augustus species dir not found: {species_src_dir}")
        return

    dest_dir = os.path.join(fundb, 'trained_species')
    os.makedirs(dest_dir, exist_ok=True)

    # Get Augustus version
    try:
        result = subprocess.run(
            ['augustus', '--version'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        aug_version = result.stdout.strip().split(' is ')[0]
    except Exception:
        aug_version = 'unknown'

    today = datetime.date.today().strftime("%Y-%m-%d")

    for sp in os.listdir(species_src_dir):
        if sp.startswith('.'):
            continue
        sp_path = os.path.join(species_src_dir, sp)
        if not os.path.isdir(sp_path):
            continue

        sp_dir = os.path.join(dest_dir, sp)
        sp_aug_dir = os.path.join(sp_dir, 'augustus')
        param_file = os.path.join(sp_dir, 'info.json')

        os.makedirs(sp_aug_dir, exist_ok=True)

        # Create or load info.json
        if os.path.isfile(param_file) and not force:
            with open(param_file) as jf:
                data = json.load(jf)
        else:
            data = {
                'augustus': [{
                    'version': aug_version,
                    'source': 'augustus pre-trained',
                    'date': today,
                    'path': os.path.abspath(sp_aug_dir),
                }],
                'genemark': [{}],
                'codingquarry': [{}],
                'snap': [{}],
                'glimmerhmm': [{}],
            }
            with open(param_file, 'w') as out:
                json.dump(data, out, indent=2)

        # Copy Augustus parameter files
        for f in os.listdir(sp_path):
            src = os.path.join(sp_path, f)
            dst = os.path.join(sp_aug_dir, f)
            if os.path.isfile(src) and not os.path.isfile(dst):
                shutil.copyfile(src, dst)

    count = len([d for d in os.listdir(dest_dir)
                 if os.path.isdir(os.path.join(dest_dir, d)) and not d.startswith('.')])
    log.info(f"Augustus species: {count} pre-trained species set up")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

ALL_DATABASES = [
    'merops', 'uniprot', 'dbcan', 'pfam', 'repeats', 'go',
    'mibig', 'interpro', 'busco_outgroups', 'gene2product', 'busco'
]

ALL_BUSCO_LINEAGES = [
    'fungi', 'microsporidia', 'dikarya', 'ascomycota', 'pezizomycotina',
    'eurotiomycetes', 'sordariomycetes', 'saccharomycetes', 'saccharomycetales',
    'basidiomycota', 'eukaryota', 'protists', 'alveolata_stramenophiles',
    'metazoa', 'nematoda', 'arthropoda', 'insecta', 'endopterygota',
    'hymenoptera', 'diptera', 'vertebrata', 'actinopterygii', 'tetrapoda',
    'aves', 'mammalia', 'euarchontoglires', 'laurasiatheria', 'embryophyta',
]

# Map processor names to functions (handles case variations)
PROCESSORS = {
    'merops': process_merops,
    'uniprot': process_uniprot,
    'dbcan': process_dbcan,
    'dbCAN': process_dbcan,
    'pfam': process_pfam,
    'repeats': process_repeats,
    'go': process_go,
    'mibig': process_mibig,
    'interpro': process_interpro,
    'busco_outgroups': process_busco_outgroups,
    'gene2product': process_gene2product,
}


def main():
    import argparse

    epilog = """Examples:
  python process_all.py -d /path/to/funannotate_db
  python process_all.py -d /path/to/funannotate_db -i merops,uniprot,pfam
  python process_all.py -d /path/to/funannotate_db -i busco -b "dikarya,sordariomycetes,fungi"
  python process_all.py -d /path/to/funannotate_db --force"""

    parser = argparse.ArgumentParser(
        prog='process_all.py',
        description='Process funannotate databases (decompress, index, extract metadata)',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-d', '--database',
                        help='Path to funannotate database directory')
    parser.add_argument('-i', '--install', default='all',
                        help=f'Databases to process, comma-separated (default: all). '
                             f'Choices: {",".join(ALL_DATABASES)}')
    parser.add_argument('-b', '--busco_db', default='dikarya',
                        help='BUSCO lineages to process, comma-separated (default: dikarya)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force reprocessing even if already done')
    args = parser.parse_args()

    # Resolve database directory
    fundb = args.database or os.environ.get("FUNANNOTATE_DB", "")
    if not fundb:
        log.error("Database directory required. Use -d <path> or set $FUNANNOTATE_DB")
        sys.exit(1)

    if not os.path.isdir(fundb):
        log.error(f"Database directory does not exist: {fundb}")
        sys.exit(1)

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    log.info("=" * 60)
    log.info(f"Database directory: {fundb}")
    log.info(f"Date: {today}")
    log.info("=" * 60)

    # Check required external tools
    log.info("Checking external tools...")
    require_tool('diamond', hint='conda install -c bioconda diamond')
    require_tool('hmmpress', hint='conda install -c bioconda hmmer')
    require_tool('gunzip', hint='should be part of coreutils on Linux')
    require_tool('tar', hint='should be part of coreutils on Linux')
    log.info("All required tools found.")

    # Load existing database info
    load_existing_info(fundb)

    # Determine which databases to process
    if args.install == 'all':
        dbs_to_process = list(ALL_DATABASES)
    else:
        dbs_to_process = [x.strip() for x in args.install.split(',')]

    # Determine BUSCO lineages
    if args.busco_db == 'all':
        busco_list = list(ALL_BUSCO_LINEAGES)
    else:
        busco_list = [x.strip() for x in args.busco_db.split(',')]

    # Setup Augustus pre-trained species (always runs if AUGUSTUS_CONFIG_PATH is set)
    setup_augustus_species(fundb, force=args.force)

    # Process each database
    failed = []
    for db in dbs_to_process:
        try:
            if db == 'busco':
                process_busco(fundb, busco_list, force=args.force)
            elif db in PROCESSORS:
                PROCESSORS[db](fundb, force=args.force, today=today)
            else:
                log.warn(f"Unknown database: {db} — skipping")
        except Exception as e:
            log.error(f"Failed to process {db}: {e}")
            import traceback
            traceback.print_exc()
            failed.append(db)

    # Write database info file
    write_info_file(fundb)

    # Summary
    print("")
    log.info("=" * 60)
    if failed:
        log.error(f"Failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        log.info("All databases processed successfully!")
        log.info(f"Don't forget: export FUNANNOTATE_DB={os.path.abspath(fundb)}")

    # Print installed database summary
    print("")
    print("Installed databases:")
    print("-" * 80)
    print(f"{'Database':<20} {'Type':<12} {'Version':<15} {'Date':<12} {'Records':>10}")
    print("-" * 80)
    for k, v in sorted(DBINFO.items()):
        if len(v) >= 5:
            print(f"{k:<20} {v[0]:<12} {v[2]:<15} {v[3]:<12} {v[4]:>10,}")
    print("-" * 80)
    print("")


if __name__ == "__main__":
    main()
