from pathlib import Path

path = Path('PYTHON/READING FROM A FILE/pi_digits.txt')
contents = path.read_text()
print(contents)