def rank_recommendations(items: list[dict], key: str = "score") -> list[dict]:
    return sorted(items, key=lambda item: item.get(key, 0), reverse=True)
