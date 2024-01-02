from sys import argv
from filecmp import cmp


"""
  Compare the contents of two files byte by byte.

  Args:
    file1 (str): Path to the first file.
    file2 (str): Path to the second file.

  Returns:
    bool: True if the files are the same, False otherwise.
"""
def validate_file_contents(file1: str, file2: str) -> bool:
  with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
    contents1 = f1.read()
    contents2 = f2.read()
  return contents1 == contents2
