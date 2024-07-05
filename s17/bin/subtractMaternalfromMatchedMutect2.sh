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

# Define inputs and outputs
S17_mat='/data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/filterVCF/1anal/s17/m_S17.haplotypecaller.filtered.vcf.gz'
S17_tum='/data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/filterVCF/1anal/s17/results/filteredHC/t_s17_filteredHC.mutect2.filtered.vcf'
s17_child='/data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/filterVCF/1anal/s17/c_S17.haplotypecaller.filtered.vcf'

S17_tum_minus_maternal='/data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/bcftools/tumour_somatic_VC/results/S17/germlinefilteredHC/S17_tumourMinusMaternal.vcf.gz'
S17_tum_minus_germline='/data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/bcftools/tumour_somatic_VC/results/S17/germlinefilteredHC/S17_tumourMinusGermline.vcf.gz'


# Subtract maternal germline variants from tumour VCF
bcftools isec -C $S17_tum $S17_mat -Oz -o $S17_tum_minus_maternal

# subtract child germline variants from tumourminusmaternal VCF (all germline variants removed after this)
bcftools isec -C $S17_tum_minus_maternal $ -Oz -o $S17_tum_minus_germline
