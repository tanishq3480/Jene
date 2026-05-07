def kmer_tokenize(sequence, k=3):
    tokens = [sequence[i:i+k] for i in range(len(sequence)-k+1)]
    return " ".join(tokens)