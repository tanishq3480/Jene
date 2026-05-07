import numpy as np
from data_loader import load_fasta
from embedding import encode_sequence
from deep_model import build_model

# Load data
sequences, labels = load_fasta("data/sample_sequences.fasta")

# Encode sequences
X = np.array([encode_sequence(seq) for seq in sequences])

# Convert labels to numbers
label_map = {label: i for i, label in enumerate(set(labels))}
y = np.array([label_map[label] for label in labels])

# Build model
model = build_model(input_length=300)

# Train
model.fit(X, y, epochs=5, batch_size=8)

# Save
model.save("models/dna_model.h5")