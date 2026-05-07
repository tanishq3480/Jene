from dna_utils import translate_dna
from gene_finder import find_orfs
from classifier import train_classifier, predict
from explainer import explain_protein

# Sample training data
sequences = [
    "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG",
    "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAA"
]
labels = ["bacteria", "virus"]

train_classifier(sequences, labels)

# Input DNA
dna = input("Enter DNA sequence: ")

# Step 1: Find genes
orfs = find_orfs(dna)
print("Detected ORFs:", orfs)

for gene in orfs:
    # Step 2: Translate
    protein = translate_dna(gene)
    print("\nProtein:", protein)

    # Step 3: Classification
    prediction = predict(gene)
    print("Predicted Organism:", prediction)

    # Step 4: Explanation
    explanation = explain_protein(protein)
    print("Amino Acid Explanation:")
    for line in explanation:
        print(line)