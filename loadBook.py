import sys
from qabot import QABot


if len(sys.argv) < 5:
    usage = """
Usage: python loadBook.py <title> <document> <chunk-size> <overlap>
Where: <title> -- string, title to appear on web app, in quotes
       <document> -- PDF to ingest, file path or URL
       <chunk-size> -- integer, tokens in each chunk
       <overlap> - integer, tokens overlapped between adjacent chunks
"""
    print(usage)
else:
    title = sys.argv[1]
    book = sys.argv[2]
    chunk_size = int(sys.argv[3])
    overlap = int(sys.argv[4])
    print(f'Chunk-size: {chunk_size} Overlap: {overlap}')
    qabot = QABot()
    qabot.loadDocument(title, book, chunk_size, overlap)
