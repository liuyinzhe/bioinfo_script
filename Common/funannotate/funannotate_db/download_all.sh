#!/bin/bash
# ============================================================================
# funannotate setup - Download Phase (standalone, curl-only)
# ============================================================================
# Downloads all third-party database files required by funannotate.
# Requires: curl (follows redirects automatically with -L)
#
# Usage:
#   ./download_all.sh -d /path/to/funannotate_db [-i all] [-b dikarya]
#   ./download_all.sh -d /path/to/funannotate_db -i merops,uniprot,pfam
#   ./download_all.sh -d /path/to/funannotate_db -i busco -b "dikarya,sordariomycetes"
#
# Options:
#   -d DIR   Database directory (required) — also reads $FUNANNOTATE_DB
#   -i LIST  Comma-separated DBs to download (default: all)
#            Choices: all, merops, uniprot, dbCAN, pfam, repeats, go, mibig,
#                     interpro, busco_outgroups, gene2product, busco
#   -b LIST  BUSCO lineages to download (default: dikarya)
#            Choices: all (28 lineages) or comma-separated list of:
#              fungi, microsporidia, dikarya, ascomycota, pezizomycotina,
#              eurotiomycetes, sordariomycetes, saccharomycetes, saccharomycetales,
#              basidiomycota, eukaryota, protists, alveolata_stramenophiles,
#              metazoa, nematoda, arthropoda, insecta, endopterygota,
#              hymenoptera, diptera, vertebrata, actinopterygii, tetrapoda,
#              aves, mammalia, euarchontoglires, laurasiatheria, embryophyta
#   -h       Show this help
# ============================================================================

set -euo pipefail

# --- URLs (direct download links, no PHP redirects) ---
declare -A DB_URLS
DB_URLS[merops]="https://ftp.ebi.ac.uk/pub/databases/merops/current_release/meropsscan.lib"
DB_URLS[uniprot]="https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz"
DB_URLS[uniprot_release]="https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/reldate.txt"
DB_URLS[dbcan]="https://bcb.unl.edu/dbCAN2/download/Databases/V12/dbCAN-HMMdb-V12.txt"
DB_URLS[dbcan_tsv]="https://bcb.unl.edu/dbCAN2/download/Databases/V12/CAZyDB.08062022.fam-activities.txt"
DB_URLS[dbcan_log]="https://bcb.unl.edu/dbCAN2/download/Databases/V12/readme.txt"
DB_URLS[pfam]="https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz"
DB_URLS[pfam_tsv]="https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz"
DB_URLS[pfam_log]="https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam.version.gz"
DB_URLS[outgroups]="https://osf.io/download/r9sne/?version=1"
DB_URLS[repeats]="https://osf.io/download/vp87c/?version=1"
DB_URLS[go_obo]="https://current.geneontology.org/ontology/go.obo"
DB_URLS[mibig]="https://dl.secondarymetabolites.org/mibig/mibig_prot_seqs_1.4.fasta"
DB_URLS[interpro]="https://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro.xml.gz"
DB_URLS[interpro_tsv]="https://ftp.ebi.ac.uk/pub/databases/interpro/current_release/entry.list"
DB_URLS[gene2product]="https://raw.githubusercontent.com/nextgenusfs/gene2product/master/ncbi_cleaned_gene_products.txt"

# --- BUSCO lineage URLs (osf.io direct download links, odb9 format) ---
declare -A BUSCO_URLS BUSCO_DIRS
BUSCO_URLS[fungi]="https://osf.io/download/xvzmu/?version=1";             BUSCO_DIRS[fungi]="fungi_odb9"
BUSCO_URLS[microsporidia]="https://osf.io/download/r47nx/?version=1";     BUSCO_DIRS[microsporidia]="microsporidia_odb9"
BUSCO_URLS[dikarya]="https://osf.io/download/av6f8/?version=1";           BUSCO_DIRS[dikarya]="dikarya_odb9"
BUSCO_URLS[ascomycota]="https://osf.io/download/z2736/?version=1";        BUSCO_DIRS[ascomycota]="ascomycota_odb9"
BUSCO_URLS[pezizomycotina]="https://osf.io/download/bj3sm/?version=1";    BUSCO_DIRS[pezizomycotina]="pezizomycotina_odb9"
BUSCO_URLS[eurotiomycetes]="https://osf.io/download/nvt3z/?version=1";    BUSCO_DIRS[eurotiomycetes]="eurotiomycetes_odb9"
BUSCO_URLS[sordariomycetes]="https://osf.io/download/r24kn/?version=1";   BUSCO_DIRS[sordariomycetes]="sordariomyceta_odb9"
BUSCO_URLS[saccharomycetes]="https://osf.io/download/mpu2k/?version=1";   BUSCO_DIRS[saccharomycetes]="saccharomyceta_odb9"
BUSCO_URLS[saccharomycetales]="https://osf.io/download/dhk47/?version=1"; BUSCO_DIRS[saccharomycetales]="saccharomycetales_odb9"
BUSCO_URLS[basidiomycota]="https://osf.io/download/2xnsj/?version=1";     BUSCO_DIRS[basidiomycota]="basidiomycota_odb9"
BUSCO_URLS[eukaryota]="https://osf.io/download/psj2k/?version=1";         BUSCO_DIRS[eukaryota]="eukaryota_odb9"
BUSCO_URLS[protists]="https://osf.io/download/a4tsk/?version=1";          BUSCO_DIRS[protists]="protists_ensembl"
BUSCO_URLS[alveolata_stramenophiles]="https://osf.io/download/waqpe/?version=1"; BUSCO_DIRS[alveolata_stramenophiles]="alveolata_stramenophiles_ensembl"
BUSCO_URLS[metazoa]="https://osf.io/download/5bvam/?version=1";           BUSCO_DIRS[metazoa]="metazoa_odb9"
BUSCO_URLS[nematoda]="https://osf.io/download/u87d3/?version=1";          BUSCO_DIRS[nematoda]="nematoda_odb9"
BUSCO_URLS[arthropoda]="https://osf.io/download/w26ez/?version=1";        BUSCO_DIRS[arthropoda]="arthropoda_odb9"
BUSCO_URLS[insecta]="https://osf.io/download/8qsa5/?version=1";           BUSCO_DIRS[insecta]="insecta_odb9"
BUSCO_URLS[endopterygota]="https://osf.io/download/pxdqg/?version=1";     BUSCO_DIRS[endopterygota]="endopterygota_odb9"
BUSCO_URLS[hymenoptera]="https://osf.io/download/q4ce6/?version=1";       BUSCO_DIRS[hymenoptera]="hymenoptera_odb9"
BUSCO_URLS[diptera]="https://osf.io/download/e2n49/?version=1";           BUSCO_DIRS[diptera]="diptera_odb9"
BUSCO_URLS[vertebrata]="https://osf.io/download/w6kf8/?version=1";        BUSCO_DIRS[vertebrata]="vertebrata_odb9"
BUSCO_URLS[actinopterygii]="https://osf.io/download/dj2cw/?version=1";    BUSCO_DIRS[actinopterygii]="actinopterygii_odb9"
BUSCO_URLS[tetrapoda]="https://osf.io/download/bp4cf/?version=1";         BUSCO_DIRS[tetrapoda]="tetrapoda_odb9"
BUSCO_URLS[aves]="https://osf.io/download/e7qym/?version=1";              BUSCO_DIRS[aves]="aves_odb9"
BUSCO_URLS[mammalia]="https://osf.io/download/dvy5m/?version=1";          BUSCO_DIRS[mammalia]="mammalia_odb9"
BUSCO_URLS[euarchontoglires]="https://osf.io/download/p3nc7/?version=1";  BUSCO_DIRS[euarchontoglires]="euarchontoglires_odb9"
BUSCO_URLS[laurasiatheria]="https://osf.io/download/2v9hj/?version=1";    BUSCO_DIRS[laurasiatheria]="laurasiatheria_odb9"
BUSCO_URLS[embryophyta]="https://osf.io/download/m67p4/?version=1";       BUSCO_DIRS[embryophyta]="embryophyta_odb9"

ALL_BUSCO_LINEAGES=(
    fungi microsporidia dikarya ascomycota pezizomycotina
    eurotiomycetes sordariomycetes saccharomycetes saccharomycetales
    basidiomycota eukaryota protists alveolata_stramenophiles metazoa
    nematoda arthropoda insecta endopterygota hymenoptera diptera
    vertebrata actinopterygii tetrapoda aves mammalia euarchontoglires
    laurasiatheria embryophyta
)

# --- Helper functions ---
log_info()  { echo "[$(date '+%H:%M:%S')] INFO:  $*"; }
log_warn()  { echo "[$(date '+%H:%M:%S')] WARN:  $*" >&2; }
log_error() { echo "[$(date '+%H:%M:%S')] ERROR: $*" >&2; }

download_file() {
    # Usage: download_file <url> <output_path>
    # Uses curl with: -L (follow redirects), -C (resume), --retry (auto-retry)
    local url="$1"
    local out="$2"
    local outdir
    outdir=$(dirname "$out")
    mkdir -p "$outdir"

    if [[ -f "$out" ]] && [[ -s "$out" ]]; then
        log_info "Already exists, skipping: $(basename "$out")"
        return 0
    fi

    log_info "Downloading: $url"
    log_info "       -> $out"

    # curl flags:
    #   -L           follow HTTP 3xx redirects to final destination
    #   -C -         resume interrupted downloads (append to partial file)
    #   --retry 5    retry up to 5 times on failure
    #   --retry-delay 10  wait 10s between retries (increasing)
    #   --retry-connrefused  also retry on connection refused
    #   --retry-max-time 300   stop retrying after 5 minutes total
    #   -o FILE      write output to FILE
    #   --progress-bar  show progress bar in terminal
    curl -L \
         -C - \
         --retry 5 \
         --retry-delay 10 \
         --retry-connrefused \
         --retry-max-time 300 \
         --progress-bar \
         -o "$out" \
         "$url"

    local curl_rc=$?
    if [[ $curl_rc -ne 0 ]]; then
        log_error "curl exited with code ${curl_rc}: $url"
        return 1
    fi
    if [[ ! -f "$out" ]] || [[ ! -s "$out" ]]; then
        log_error "Download failed or file is empty: $out"
        return 1
    fi
    log_info "Download complete: $(basename "$out") ($(du -h "$out" | cut -f1))"
}

# --- Individual DB downloaders ---
download_merops() {
    log_info "=== Downloading MEROPS database ==="
    download_file "${DB_URLS[merops]}" "${FUNDB}/meropsscan.lib"
}

download_uniprot() {
    log_info "=== Downloading UniProtKB/SwissProt database ==="
    download_file "${DB_URLS[uniprot]}"         "${FUNDB}/uniprot_sprot.fasta.gz"
    download_file "${DB_URLS[uniprot_release]}" "${FUNDB}/uniprot.release-date.txt"
}

download_dbcan() {
    log_info "=== Downloading dbCAN CAZyme database ==="
    download_file "${DB_URLS[dbcan]}"     "${FUNDB}/dbCAN.tmp"
    download_file "${DB_URLS[dbcan_tsv]}" "${FUNDB}/dbCAN-fam-HMMs.txt"
    download_file "${DB_URLS[dbcan_log]}" "${FUNDB}/dbCAN.changelog.txt"
}

download_pfam() {
    log_info "=== Downloading Pfam database ==="
    download_file "${DB_URLS[pfam]}"     "${FUNDB}/Pfam-A.hmm.gz"
    download_file "${DB_URLS[pfam_tsv]}" "${FUNDB}/Pfam-A.clans.tsv.gz"
    download_file "${DB_URLS[pfam_log]}" "${FUNDB}/Pfam.version.gz"
}

download_repeats() {
    log_info "=== Downloading Repeat proteins database ==="
    download_file "${DB_URLS[repeats]}" "${FUNDB}/funannotate.repeat.proteins.fa.tar.gz"
}

download_go() {
    log_info "=== Downloading GO Ontology ==="
    download_file "${DB_URLS[go_obo]}" "${FUNDB}/go.obo"
}

download_mibig() {
    log_info "=== Downloading MiBIG database ==="
    download_file "${DB_URLS[mibig]}" "${FUNDB}/mibig.fa"
}

download_interpro() {
    log_info "=== Downloading InterProScan mapping files ==="
    download_file "${DB_URLS[interpro]}"     "${FUNDB}/interpro.xml.gz"
    download_file "${DB_URLS[interpro_tsv]}" "${FUNDB}/interpro.tsv"
}

download_busco_outgroups() {
    log_info "=== Downloading BUSCO outgroups ==="
    download_file "${DB_URLS[outgroups]}" "${FUNDB}/busco_outgroups.tar.gz"
}

download_gene2product() {
    log_info "=== Downloading curated gene2product database ==="
    download_file "${DB_URLS[gene2product]}" "${FUNDB}/ncbi_cleaned_gene_products.txt"
}

download_busco() {
    local lineages=("$@")
    log_info "=== Downloading BUSCO lineage models: ${lineages[*]} ==="
    for lineage in "${lineages[@]}"; do
        if [[ -z "${BUSCO_URLS[$lineage]:-}" ]]; then
            log_error "Unknown BUSCO lineage: $lineage"
            log_error "Available: ${ALL_BUSCO_LINEAGES[*]}"
            return 1
        fi
        log_info "--- BUSCO lineage: $lineage ---"
        download_file "${BUSCO_URLS[$lineage]}" "${FUNDB}/${lineage}.tar.gz"
    done
}

# --- Main ---
usage() {
    head -30 "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

# Parse arguments
FUNDB=""
INSTALL="all"
BUSCO_LINEAGES="dikarya"

while getopts "d:i:b:h" opt; do
    case $opt in
        d) FUNDB="$OPTARG" ;;
        i) INSTALL="$OPTARG" ;;
        b) BUSCO_LINEAGES="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Resolve database directory
if [[ -z "$FUNDB" ]]; then
    if [[ -n "${FUNANNOTATE_DB:-}" ]]; then
        FUNDB="$FUNANNOTATE_DB"
    else
        log_error "Database directory required. Use -d <path> or set \$FUNANNOTATE_DB"
        exit 1
    fi
fi

# Verify curl is available
if ! command -v curl &>/dev/null; then
    log_error "curl is required but not found. Install it: apt-get install curl / yum install curl"
    exit 1
fi

log_info "Downloader: curl (follows redirects with -L)"
log_info "Database directory: $FUNDB"
log_info "Databases to download: $INSTALL"
log_info "BUSCO lineages: $BUSCO_LINEAGES"

# Create database directory
mkdir -p "$FUNDB"

# Determine which databases to install
if [[ "$INSTALL" == "all" ]]; then
    DBS_TO_DOWNLOAD=(merops uniprot dbcan pfam repeats go mibig interpro busco_outgroups gene2product busco)
else
    IFS=',' read -ra DBS_TO_DOWNLOAD <<< "$INSTALL"
fi

# Determine BUSCO lineages
if [[ "$BUSCO_LINEAGES" == "all" ]]; then
    BUSCO_LIST=("${ALL_BUSCO_LINEAGES[@]}")
else
    IFS=',' read -ra BUSCO_LIST <<< "$BUSCO_LINEAGES"
fi

# Execute downloads
FAILED=()
for db in "${DBS_TO_DOWNLOAD[@]}"; do
    case "$db" in
        merops)          download_merops || FAILED+=("$db") ;;
        uniprot)         download_uniprot || FAILED+=("$db") ;;
        dbcan|dbCAN)     download_dbcan || FAILED+=("$db") ;;
        pfam)            download_pfam || FAILED+=("$db") ;;
        repeats)         download_repeats || FAILED+=("$db") ;;
        go)              download_go || FAILED+=("$db") ;;
        mibig)           download_mibig || FAILED+=("$db") ;;
        interpro)        download_interpro || FAILED+=("$db") ;;
        busco_outgroups) download_busco_outgroups || FAILED+=("$db") ;;
        gene2product)    download_gene2product || FAILED+=("$db") ;;
        busco)           download_busco "${BUSCO_LIST[@]}" || FAILED+=("$db") ;;
        *)
            log_warn "Unknown database: $db — skipping"
            ;;
    esac
done

# Summary
echo ""
echo "=============================================="
log_info "Download phase complete."
if [[ ${#FAILED[@]} -gt 0 ]]; then
    log_error "The following databases failed to download: ${FAILED[*]}"
    log_error "Re-run with: $0 -d $FUNDB -i $(IFS=,; echo "${FAILED[*]}")"
    exit 1
else
    log_info "All requested databases downloaded successfully to: $FUNDB"
    log_info "Next step: run process_all.py to build indexes"
fi
echo "=============================================="
