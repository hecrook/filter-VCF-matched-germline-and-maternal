#!/bin/bash
#SBATCH --job-name=matched-maternal
#SBATCH --ntasks=1
#SBATCH --time=2:00:00
#SBATCH --mem-per-cpu=4021
#SBATCH --mail-user=hannah.crook@icr.ac.uk
#SBATCH --mail-type=ALL

module load anaconda/3
source activate bcftools

# Analysing samples 
# S17

### SUBTRACTING MATERNAL HAPLOTYPECALLER VCF FROM TUMOUR MUTECT2 VCF ###

## S17 ##
cd /data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/filterVCF/1anal/s17

# Define inputs and outputs
S17_mat='input/m_S17.haplotypecaller.filtered.vcf.gz'
S17_tum='results/filteredHC/t_s17_filteredHC.mutect2.filtered.vcf.gz'
S17_child='input/c_S17.haplotypecaller.filtered.vcf.gz'

S17_germline='input/s17_maternalAndChildGermline.vcf.gz'
S17_tum_minus_germline='results/germlinefilteredHC/S17_tumourMinusGermline.vcf.gz'

# merge
bcftools merge $S17_mat $S17_child -Oz -o $S17_germline

# index
bcftools index $S17_germline

# Subtract maternal germline variants from tumour VCF
bcftools isec -C $S17_tum $S17_germline -Oz -o $S17_tum_minus_germline
