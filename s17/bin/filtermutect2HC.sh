#!/bin/bash
#SBATCH --job-name=filter_mutect2_HC-TEST
#SBATCH --output=filter_mutect2_HC.out  # Standard output and error log
#SBATCH --error=filter_mutect2_HC.err   # Error log
#SBATCH --cpus-per-task=16
#SBATCH --time=12:00:00
#SBATCH --mem-per-cpu=4021
#SBATCH --mail-user=hannah.crook@icr.ac.uk
#SBATCH --mail-type=ALL

echo "changing directory" 

cd /data/scratch/DMP/UCEC/EVOLIMMU/hcrook/gestational_WES_WGS/analysis/filterVCF/1anal/s17

pwd

module load anaconda/3

python filter_mutect2_HC.py t_S17.mutect2.filtered.vcf m_S17.haplotypecaller.filtered.vcf c_S17.haplotypecaller.filtered.vcf s17_filterMutect2HC_TEST_output.vcf
