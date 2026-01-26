import re  #delete excessive whitespace, split by paragraphs, removing header footers heavy line breaks etc. 

def chunk_text(text: str, max_chunk_size: int = 500) -> list:
    """
    Splits text into semantically meaningful chunks for embeddings.
    
    Args:
        text (str): The full text of the document.
        max_chunk_size (int): Maximum number of words per chunk.
    
    Returns:
        List[str]: A list of text chunks.
    """
    # Step 1: Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    '''
    1. re.sub(r'\s+', ' ', text)
re.sub: This is a "search and replace" function using Regular Expressions (regex).

r'\s+': This looks for any whitespace character (spaces, tabs, newlines, carriage returns). The + means "one or more."

' ': This is the replacement. It tells Python to take those chunks of whitespace and turn them into a single, standard space.

The Result: If you had five spaces or a mix of tabs and newlines, they are all squashed down into one space.

2. .strip()
Once the middle of the text is cleaned, strip() removes any leading or trailing whitespace that might be left at the very beginning or the very end of the string.'''
    
    
    # Step 2: Split into paragraphs (or by line breaks)
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    chunks = []
    current_chunk = ""
    current_length = 0

    for para in paragraphs:
        para_words = para.split()
        para_len = len(para_words)
        
        # If adding this paragraph exceeds max_chunk_size, start a new chunk
        if current_length + para_len > max_chunk_size:
            if current_chunk:  # save current chunk
                chunks.append(current_chunk.strip())
            # Start new chunk with current paragraph
            current_chunk = para
            current_length = para_len
        else:
            # Append paragraph to current chunk
            if current_chunk:
                current_chunk += " " + para
            else:
                current_chunk = para
            current_length += para_len

    # Add last chunk if any
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
