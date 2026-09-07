from typing import List


def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Full extracted document text.
        chunk_size: Maximum characters per chunk.
        overlap: Characters shared with previous chunk.

    Returns:
        List of text chunks.
    """

    if not text.strip():
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks