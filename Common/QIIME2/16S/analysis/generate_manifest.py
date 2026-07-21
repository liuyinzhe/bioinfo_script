#!/usr/bin/env python3
"""
Generate a QIIME2-style manifest file from sample metadata and paired-end FASTQ files.

Reads a sample-metadata TSV to get sample IDs, scans a data directory for
matching .gz files, identifies R1 (forward) and R2 (reverse) reads using
flexible naming patterns, and writes a manifest with absolute paths.

Supported R1/R2 naming conventions:
    sample.R1.fastq.gz          sample.R2.fastq.gz
    sample_4498670S_R1.fq.gz    Sample_4498670S_R2.fq.gz
    sample_161319-Left_L1_R1.fq.gz   sample_161319-Left_L1_R2.fq.gz
    sample_161319-Left_L1.1.fq.gz    sample_161319-Left_L1.2.fq.gz

Usage:
    python generate_manifest.py --metadata sample-metadata.tsv --data-dir ./data
    python generate_manifest.py --metadata sample-metadata.tsv --data-dir ./data --output manifest.txt
"""

import argparse
import os
import re
import sys
from pathlib import Path


def classify_read(filename: str) -> str | None:
    """
    Classify a gzipped FASTQ filename as R1 (forward) or R2 (reverse).

    Returns 'R1', 'R2', or None if the read direction cannot be determined.
    """
    # Explicit R1/R2 markers separated by dot or underscore
    # Matches: .R1. / _R1. / .R1_ / _R1_  (case-insensitive)
    if re.search(r"[._]R1[._]", filename, re.IGNORECASE):
        return "R1"
    if re.search(r"[._]R2[._]", filename, re.IGNORECASE):
        return "R2"

    # Numeric read markers: .1. / _1. / .2. / _2. before .fq.gz / .fastq.gz
    if re.search(r"[._]1\.(?:fq|fastq)\.gz$", filename, re.IGNORECASE):
        return "R1"
    if re.search(r"[._]2\.(?:fq|fastq)\.gz$", filename, re.IGNORECASE):
        return "R2"

    return None


def find_sample_files(sample_id: str, data_dir: Path) -> tuple[str | None, str | None]:
    """
    Find R1 and R2 file paths for a given sample ID.

    Scans the data directory for .gz files whose names contain the sample ID
    (case-insensitive), then classifies each as R1 or R2.

    Returns (r1_absolute_path, r2_absolute_path). Either may be None if not found.
    """
    gz_files = list(data_dir.glob("*.gz"))
    if not gz_files:
        print(f"Warning: No .gz files found in {data_dir}", file=sys.stderr)
        return None, None

    # Case-insensitive match on sample ID within the filename
    matching = [f for f in gz_files if sample_id.lower() in f.name.lower()]

    if not matching:
        print(f"Warning: No files matching sample '{sample_id}' in {data_dir}",
              file=sys.stderr)
        return None, None

    r1_files = []
    r2_files = []

    for f in matching:
        direction = classify_read(f.name)
        abs_path = str(f.resolve())
        if direction == "R1":
            r1_files.append(abs_path)
        elif direction == "R2":
            r2_files.append(abs_path)

    # Warn on ambiguous matches
    if len(r1_files) > 1:
        print(f"Warning: Multiple R1 files for sample '{sample_id}': {r1_files}",
              file=sys.stderr)
    if len(r2_files) > 1:
        print(f"Warning: Multiple R2 files for sample '{sample_id}': {r2_files}",
              file=sys.stderr)

    r1 = r1_files[0] if r1_files else None
    r2 = r2_files[0] if r2_files else None

    if r1 is None:
        print(f"Warning: No R1 (forward) file found for sample '{sample_id}'",
              file=sys.stderr)
    if r2 is None:
        print(f"Warning: No R2 (reverse) file found for sample '{sample_id}'",
              file=sys.stderr)

    return r1, r2


def read_metadata(metadata_path: str) -> list[dict]:
    """
    Read a sample-metadata TSV file.

    Expects a header row followed by sample rows.
    Returns a list of dicts with keys from the header.
    """
    samples = []
    with open(metadata_path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            record = re.split("\t",line.strip())
            samples.append(record[0])

    return samples


def write_manifest(samples, data_dir: Path, output_path: str) -> None:
    """
    Write the manifest TSV with absolute paths for each sample's R1/R2 files.
    """
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("sample-id\tforward-absolute-filepath\treverse-absolute-filepath\n")

        for sid in samples:
            r1, r2 = find_sample_files(sid, data_dir)
            r1 = r1 or "NOT_FOUND"
            r2 = r2 or "NOT_FOUND"
            out.write(f"{sid}\t{r1}\t{r2}\n")

    print(f"Manifest written to: {os.path.abspath(output_path)}")
    print(f"  Samples processed: {len(samples)}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a QIIME2 manifest from sample metadata and paired-end FASTQ files."
    )
    parser.add_argument(
        "--metadata", "-m",
        required=True,
        help="Path to sample-metadata TSV file (e.g. sample-metadata.tsv)",
    )
    parser.add_argument(
        "--data-dir", "-d",
        required=True,
        help="Directory containing gzipped FASTQ files (*.gz)",
    )
    parser.add_argument(
        "--output", "-o",
        default="manifest.tsv",
        help="Output manifest file path (default: manifest.tsv)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.metadata):
        print(f"Error: Metadata file not found: {args.metadata}", file=sys.stderr)
        sys.exit(1)

    data_dir = Path(args.data_dir)
    if not data_dir.is_dir():
        print(f"Error: Data directory not found: {args.data_dir}", file=sys.stderr)
        sys.exit(1)

    samples = read_metadata(args.metadata)
    if not samples:
        print("Error: No samples found in metadata file", file=sys.stderr)
        sys.exit(1)
    print(f"Read {len(samples)} samples from metadata")
    print(f"Scanning data directory: {data_dir}")
    print(f"Found {len(list(data_dir.glob('*.gz')))} .gz files")

    write_manifest(samples, data_dir, args.output)


if __name__ == "__main__":
    main()
