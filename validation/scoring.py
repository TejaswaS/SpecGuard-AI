def calculate_quality_score(product, issues):
    total_specs = len(product.specifications)

    if total_specs == 0:
        return 0

    score = 100

    for issue in issues:
        if issue.severity == "ERROR":
            score -= 10
        elif issue.severity == "WARNING":
            score -=7
        elif issue.severity == "MISSING":
            score -= 10

    score = max(0, min(100, score))
    return score
