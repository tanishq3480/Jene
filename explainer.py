amino_acid_info = {
    "A": "Alanine - small, hydrophobic",
    "R": "Arginine - positively charged",
    "N": "Asparagine - polar",
    "D": "Aspartic acid - negatively charged",
    "C": "Cysteine - forms disulfide bonds",
    "E": "Glutamic acid - acidic",
    "Q": "Glutamine - polar",
    "G": "Glycine - flexible",
    "H": "Histidine - pH sensitive",
    "I": "Isoleucine - hydrophobic",
    "L": "Leucine - hydrophobic",
    "K": "Lysine - basic",
    "M": "Methionine - start codon",
    "F": "Phenylalanine - aromatic",
    "P": "Proline - rigid structure",
    "S": "Serine - polar",
    "T": "Threonine - polar",
    "W": "Tryptophan - bulky",
    "Y": "Tyrosine - aromatic",
    "V": "Valine - hydrophobic"
}

def explain_protein(protein):
    explanation = []
    for aa in protein:
        info = amino_acid_info.get(aa, "Unknown")
        explanation.append(f"{aa}: {info}")
    return explanation