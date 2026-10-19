# panel of normals (PoN)
#https://github.com/dellytools/sansa#somatic-sv-filtering
#https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/release/v1.0/delly-unfiltered-hg38/
#https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/release/v1.0/delly-unfiltered-hg38/all.delly.hg38.1kGP.ont.bcf 
#https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/release/v1.0/delly-unfiltered-hg38/all.delly.hg38.1kGP.ont.bcf.csi 

# bcf
rsync -avzP --timeout=60 --partial --progress --checksum \
  rsync://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/release/v1.0/delly-unfiltered-hg38/all.delly.hg38.1kGP.ont.bcf \
  ./all.delly.hg38.1kGP.ont.bcf
# bcf index
rsync -avzP --timeout=60 --partial --progress --checksum \
  rsync://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1KG_ONT_VIENNA/release/v1.0/delly-unfiltered-hg38/all.delly.hg38.1kGP.ont.bcf.csi \
  ./all.delly.hg38.1kGP.ont.bcf.csi
