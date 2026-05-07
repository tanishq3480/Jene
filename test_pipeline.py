from Bio import SeqIO
from Bio.Seq import Seq

def dna_to_protein(seq):
    return str(Seq(seq).translate(to_stop=True))

for record in SeqIO.parse("data/sample_sequences.fasta", "fasta"):
    dna = str(record.seq)
    protein = dna_to_protein(dna)

    print("DNA:", dna[:50])
    print("Protein:", protein[:30])
    print("-" * 50)