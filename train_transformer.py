from Bio import SeqIO
from Bio.Seq import Seq

from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import Dataset

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from collections import Counter
from dna_tokenizer import kmer_tokenize

# -------------------------
# DNA → PROTEIN
# -------------------------
def dna_to_protein(seq):
    try:
        seq = seq[:len(seq)//3 * 3]  # trim to multiple of 3
        return str(Seq(seq).translate(to_stop=True))
    except:
        return ""


# -------------------------
# LOAD DATA
# -------------------------
def load_fasta(file_path):
    sequences = []
    labels = []

    for record in SeqIO.parse(file_path, "fasta"):
        seq = str(record.seq)
        desc = record.description.lower()

        if "bacteria" in desc or "escherichia" in desc:
            label = "bacteria"
        elif "virus" in desc:
            label = "virus"
        elif "homo sapiens" in desc:
            label = "human"
        else:
            continue

        sequences.append(seq)
        labels.append(label)

    return sequences, labels


sequences, labels = load_fasta("data/sample_sequences.fasta")
print("Label Distribution:", Counter(labels))


# -------------------------
# PREPROCESS (FIXED ALIGNMENT)
# -------------------------
proteins = []
filtered_labels = []

for seq, label in zip(sequences, labels):
    protein = dna_to_protein(seq)

    if len(protein) > 0:
        proteins.append(protein)
        filtered_labels.append(label)

# Protein-level tokenization (IMPORTANT)
def simple_tokenize(seq):
    return " ".join(list(seq))  # space-separated amino acids

def kmer_tokenize(sequence, k=3):
    """
    Converts a sequence into k-mers (substrings of length k)
    Example:
    ATGCGT → ATG TGC GCG CGT
    """
    if not sequence:
        return ""

    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    
    return " ".join(kmers)

texts = []
y = []
label_map = {label: i for i, label in enumerate(set(filtered_labels))}
for seq, label in zip(sequences, labels):
    protein = dna_to_protein(seq)
    
    if len(protein) == 0:
        continue
        
    texts.append(kmer_tokenize(protein))
    y.append(label_map[label])
# Label encoding


# -------------------------
# TRAIN-TEST SPLIT
# -------------------------
train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, y, test_size=0.2, stratify=y
)


# -------------------------
# CREATE DATASETS
# -------------------------
train_dataset = Dataset.from_dict({"text": train_texts, "label": train_labels})
test_dataset = Dataset.from_dict({"text": test_texts, "label": test_labels})


# -------------------------
# TOKENIZER (PROTEIN MODEL)
# -------------------------
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "Rostlab/prot_bert",
    do_lower_case=False
)

def preprocess_protein(seq):
    return " ".join(list(seq))  # VERY IMPORTANT

texts = [preprocess_protein(p) for p in proteins if len(p) > 0]

def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

# Remove raw text
train_dataset = train_dataset.remove_columns(["text"])
test_dataset = test_dataset.remove_columns(["text"])

train_dataset.set_format("torch")
test_dataset.set_format("torch")


# -------------------------
# MODEL (BIO MODEL 🔥)
# -------------------------
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "Rostlab/prot_bert",
    num_labels=len(label_map)
)


# -------------------------
# TRAINING
# -------------------------
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    num_train_epochs=10,
    learning_rate=2e-5,
    logging_steps=5,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

print("Sample input:", train_dataset[0])

# Train
trainer.train()


# -------------------------
# EVALUATION
# -------------------------
predictions = trainer.predict(test_dataset)
preds = predictions.predictions.argmax(axis=1)

print(classification_report(test_labels, preds))
print(tokenizer.tokenize(texts[0])[:20])