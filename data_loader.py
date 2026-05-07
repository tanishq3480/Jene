from Bio import SeqIO

def load_fasta(file_path):
    sequences = []
    labels = []

    for record in SeqIO.parse(file_path, "fasta"):
        seq = str(record.seq)
        label = record.id.split("_")[-1]  # crude label extraction
        sequences.append(seq)
        labels.append(label)

    return sequences, labels