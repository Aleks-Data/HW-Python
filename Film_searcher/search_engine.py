def parse_query(text: str, stop_words: set[str]) -> set[str]:
    words = set(text.lower().split())
    cleaned_words = words - stop_words

    return cleaned_words


def match_document(document_words: set[str], query_words: set[str]) -> int:
    document_words_lower = {word.lower() for word in document_words}
    return len(document_words_lower.intersection(query_words))


def find_documents(documents: list[tuple[int, set[str]]], stop_words: set[str], query: str) -> list[tuple[int, int]]:
    query_no_stop_words = parse_query(query, stop_words)
    results = []

    for doc_id, document in documents:
        relevance = match_document(document, query_no_stop_words)
        if relevance > 0:
            results.append((doc_id, relevance))

    if results:
        results.sort(key=lambda x: x[1], reverse=True)

    return results
