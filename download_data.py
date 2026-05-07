from Bio import Entrez, SeqIO
import os
import time

Entrez.email = "lipitanishq@gmail.com"

def download_sequences(query, label, max_results=10):
    handle = Entrez.esearch(db="nucleotide", term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]

    sequences = []

    for seq_id in ids:
        try:
            fetch = Entrez.efetch(
                db="nucleotide",
                id=seq_id,
                rettype="fasta",
                retmode="text"
            )

            record = SeqIO.read(fetch, "fasta")

            # 🔥 Add label to description
            record.description += f" | label={label}"

            sequences.append(record)

            time.sleep(0.4)  # ⚠️ rate limiting

        except Exception as e:
            print(f"Error fetching {seq_id}: {e}")

    return sequences


def save_fasta(sequences, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    SeqIO.write(sequences, filename, "fasta")


# 🔥 MULTI-CLASS DATASET
bacteria = download_sequences(
    "16S ribosomal RNA[Title] AND bacteria[Organism]",
    "bacteria",
    30
)

virus = download_sequences(
    "complete genome[Title] AND virus[Organism]",
    "virus",
    30
)

human = download_sequences(
    "Homo sapiens[Organism] AND gene[Title]",
    "human",
    30
)

all_sequences = bacteria + virus + human

save_fasta(all_sequences, "data/sample_sequences.fasta")

print(f"Downloaded {len(all_sequences)} sequences")

# Preview
for i, seq in enumerate(all_sequences[:3]):
    print(f"\nSequence {i+1}:")
    print(seq.id)
    print(seq.description)
    print(seq.seq[:60])