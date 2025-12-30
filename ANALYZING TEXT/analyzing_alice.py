from pathlib import Path

path = Path('EXCEPTIONS/alice.txt')
try:
    contents = path.read_text(encoding='utf-8')
except FileNotFoundError:
    print(f"Sorry, the file {path} does not exist.")
else:
    #COUNT THE APPROXIMATE NUMBER OF WORDS IN THE FILE
    words = contents.split()
    num_words = len(words)
    print(f"The file {path} has about {num_words} words.")