from sys import argv
from filecmp import cmp

def validate_file_contents(file1: str, file2: str) -> bool:
  with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
    contents1 = f1.read()
    contents2 = f2.read()
  return contents1 == contents2

if __name__ == '__main__':
  print(validate_file_contents(argv[1], argv[2]))
  print(cmp(argv[1], argv[2], shallow=False))