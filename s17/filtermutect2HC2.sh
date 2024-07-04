#!/bin/bash
#SBATCH --job-name=filter_try
#SBATCH --ntasks=1
#SBATCH --time=2:00:00
#SBATCH --mem-per-cpu=4021
#SBATCH --mail-user=hannah.crook@icr.ac.uk
#SBATCH --mail-type=ALL

cd /data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/filterVCF/1anal/s17

python3 filter_mutect2_HC2.py  t_S17.mutect2.filtered.vcf m_S17.haplotypecaller.filtered.vcf c_S17.haplotypecaller.filtered.vcf s17_filterMutect2HC2_output.vcf