def find_orfs(dna):
    start = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    orfs = []

    for i in range(len(dna)):
        if dna[i:i+3] == start:
            for j in range(i, len(dna), 3):
                codon = dna[j:j+3]
                if codon in stop_codons:
                    orfs.append(dna[i:j+3])
                    break
    return orfs