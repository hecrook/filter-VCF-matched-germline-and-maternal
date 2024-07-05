# Make sure overall coverage is high enough at a variant site (above 10)
# alt allele > 3
#######################################################
# Filters VCF files 			                      #
# Analysis 1: tumour, maternal, child                 #
# How to use: python3 script.sh tumour.vcf output.vcf #
#######################################################


import sys
import re

print("Script started", flush=True)
sys.stderr.flush()

print("Pulling files from the command line", flush=True)
sys.stderr.flush()

vcfFileTumour = sys.argv[1]
vcfFileOutput = sys.argv[2]

print("Opening files", flush=True)
sys.stderr.flush()

with open(vcfFileTumour, 'r') as tumour_vcf, \
     open(vcfFileOutput, 'w') as out_vcf:


    # parse the header:
    for header_line in tumour_vcf:
        out_vcf.write(header_line)

        if header_line.startswith("##tumor_sample="):
            tumor_id = header_line[len("##tumor_sample="):][:-1]

        if header_line.startswith("#CHROM"):
            row_names = header_line[1:-1].split('\t')
            break

    # parse mutations
    for mutation_line in tumour_vcf:
        # creates dictionary of the given mutation line, splitting values by \t and assigning them to the previously defined row_names in chronological order
        fields = dict(zip(row_names, mutation_line[:-1].split('\t')))
        # fetches the dictionary entry under "FORMAT" and splits the entry by :
        info = fields["FORMAT"].split(':')
        # creates a second dictionary where info is now the key (originally from format column), and fetches values from the field dictionary under the tumour_id key (which has all the real info on the GT:AD etc.)
        t_info = dict(zip(info, fields[tumor_id].split(':')))
        # this takes the values from the AD key in the t_info dictionary and splits them by ',' then for each new string it creates it converts them to integers.
        t_info["AD"] = [int(e) for e in t_info["AD"].split(',')]


        # continue with only pass
        pass_filter = fields["FILTER"] == "." or fields["FILTER"] == "PASS"
        pass_chromo = bool(re.match("^(chr)?[0-9XY]*$", fields["CHROM"]))

        if pass_chromo \
            and pass_filter \
            and sum(t_info["AD"]) > 10 \
            and t_info["AD"][1] >= 3:
                out_vcf.write(mutation_line)


print("Script finished", flush=True)
sys.stderr.flush()



