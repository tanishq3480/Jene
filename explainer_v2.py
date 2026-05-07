def explain_protein_advanced(protein):
    explanations = []

    for i, aa in enumerate(protein):
        context = protein[max(0, i-2):i+3]

        explanations.append(
            f"Position {i}: {aa} | Context: {context} | Likely structural/functional role"
        )

    return explanations