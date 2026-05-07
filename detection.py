def find_orfs_advanced(dna):
    start = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    orfs = []

    for frame in range(3):
        for i in range(frame, len(dna), 3):
            if dna[i:i+3] == start:
                for j in range(i, len(dna), 3):
                    if dna[j:j+3] in stop_codons:
                        orfs.append(dna[i:j+3])
                        break
    return orfs