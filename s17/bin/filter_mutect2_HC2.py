import sys
import re

vcfFileTumour = sys.argv[1]
vcfFileMaternal = sys.argv[2]
vcfFileChild = sys.argv[3]
vcfFileOutput = sys.argv[4]

def read_vcf(file):
    with open(file, 'r') as f:
        lines = [line.strip() for line in f if not line.startswith('#')]
    return lines

def get_genotype_dict(vcf_lines):
    genotype_dict = {}
    for line in vcf_lines:
        fields = line.split('\t')
        chrom_pos = (fields[0], fields[1])  # (CHROM, POS)
        alleles = fields[4].split(',')
        genotype_dict[chrom_pos] = alleles
    return genotype_dict

maternal_lines = read_vcf(vcfFileMaternal)
child_lines = read_vcf(vcfFileChild)

maternal_dict = get_genotype_dict(maternal_lines)
child_dict = get_genotype_dict(child_lines)

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
        # pulls information on chromosome number
        chrom = fields["CHROM"]
        # pulls info from position
        pos = fields["POS"]
        # pull out allele information
        alleles = fields["ALT"].split(',')

        chrom_pos = (chrom, pos)

        # Look for maternal and child genotype
        mat_allele = maternal_dict.get(chrom_pos, [])
        child_allele = child_dict.get(chrom_pos, [])

        germline_alleles = set(mat_allele + child_allele)

        # continue with only pass
        pass_filter = fields["FILTER"] == "." or fields["FILTER"] == "PASS"
        pass_chromo = bool(re.match("^(chr)?[0-9XY]*$", fields["CHROM"]))
        germ_filter = any(allele not in germline_alleles for allele in alleles)

        if pass_chromo \
            and pass_filter \
            and germ_filter \
            and sum(t_info["AD"]) > 10 \
            and t_info["AD"][1] >= 3:
                out_vcf.write(mutation_line)
