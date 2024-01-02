import os
from argparse import ArgumentParser

from include.videoCompare import VideoCompare
from include.imageCompare import ImageCompare
from include.fileByteCompare import validate_file_contents


def parser() -> ArgumentParser:
  """
  Parse command line arguments.

  Returns:
      ArgumentParser: The argument parser object.
  """
  parser = ArgumentParser(
      description='Find duplicate files in the given directory.')
  parser.add_argument('--version', action='version',
                      version='%(prog)s 0.1')

  parser.add_argument(
      '-d', '--directory', help='Find duplicates on this directory', default='.', type=str)
  parser.add_argument(
      '-v', '--verbose', help='Print verbose output', action='count', default=0)
  parser.add_argument(
      '-s', '--similarity', help='Set the similarity threshold', default=0.85, type=float)
  parser.add_argument('-t', '--type', help='Set the type of comparison to use',
                      choices=['soft', 'hard'], default='soft', type=str)
  parser.add_argument(
      '-r', '--recursive', help='Recursively search the directory', action='store_true')
  parser.add_argument('-a', '--action', help='Action to take on duplicate files',
                      choices=['delete', 'move', 'link'], default='delete', type=str)
  parser.add_argument(
      '-o', '--output', help='Output file to write duplicate files', default='duplicated', type=str)

  group = parser.add_mutually_exclusive_group()

  group.add_argument(
      '-e', '--exclude', help='Exclude these file types', nargs='+', default=[], type=str)
  group.add_argument(
      '-i', '--include', help='Include these file types', nargs='+', default=[], type=str)

  return parser


class DuplicateFinder:
  """
  Class to find duplicate files in a given directory.

  Attributes:
      directory (str): The directory to search for duplicate files.
      verbose (int): The level of verbosity for output.
      similarity (float): The similarity threshold for file comparison.
      type (str): The type of comparison to use ('soft' or 'hard').
      recursive (bool): Flag to indicate whether to search the directory recursively.
      exclude (list[str]): List of file types to exclude from comparison.
      include (list[str]): List of file types to include in comparison.
      action (str): The action to take on duplicate files 
          ('delete', 
          'move', 
          or 'link').
      output (str): The output file to write duplicate files.
      duplicates (dict): Dictionary to store duplicate files.

  Methods:
      get_all_files(): Get all files in the directory with the given option.
      get_recursive_files(): Get all files in the directory recursively.
      get_files(): Get all files in the directory.
      compare_files(file1: str, file2: str) -> bool: Compare two files.
      compare_files_hard(file1: str, file2: str) -> bool: Compare two files \
          using hard comparison.
  """

  videoExtensions = {'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm'}
  imageExtensions = {'jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'tif'}

  def __init__(self) -> None:
    self.args = parser().parse_args()

    self.directory = self.args.directory
    self.verbose = self.args.verbose
    self.similarity = self.args.similarity
    self.type = self.args.type
    self.recursive = self.args.recursive
    self.exclude = self.args.exclude
    self.include = self.args.include
    self.action = self.args.action
    self.output = self.args.output

    self.duplicates = {}

  def get_all_files(self) -> list[str]:
    """
    Get all files in the directory.

    Returns:
        list[str]: List of file paths.
    """
    allFiles = []

    allFiles = self.get_files() if not self.recursive else self.get_recursive_files()

    allFiles = filter(lambda x: x.split('.')[-1] not in self.exclude, allFiles)

    if self.include:
        allFiles = filter(lambda x: x.split('.')[-1] in self.include, allFiles)

    return list(allFiles)

  def get_recursive_files(self) -> list[str]:
    """
    Get all files in the directory recursively.

    Returns:
        list[str]: List of file paths.
    """
    return [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(self.directory) for f in filenames]

  def get_files(self) -> list[str]:
    """
    Get all files in the directory.

    Returns:
        list[str]: List of file paths.
    """
    return [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

  def compare_files(self, file1: str, file2: str) -> bool:
    """
    Compare two files.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.

    Returns:
        bool: True if the files are considered duplicates, False otherwise.
    """
    if self.type == 'soft':
        return self.compare_files_soft(file1, file2)

    return self.compare_files_hard(file1, file2)

  def type_check(self, extension1: str, extension2: str) -> bool:
    """
    Check if the file types are the same.

    Args:
        extension1 (str): Extension of the first file.
        extension2 (str): Extension of the second file.

    Returns:
        bool: True if the file types are the same, False otherwise.
    """

    if extension1 == extension2:
        return True

    if extension1 in self.videoExtensions and extension2 in self.imageExtensions:
        return False

    if extension1 in self.imageExtensions and extension2 in self.videoExtensions:
        return False

    if extension1 in self.videoExtensions and extension2 in self.videoExtensions:
        return True

    if extension1 in self.imageExtensions and extension2 in self.imageExtensions:
        return True

    return False

  def compare_files_hard(self, file1: str, file2: str) -> bool:
    """
    Compare two files using hard comparison.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.

    Returns:
        bool: True if the files are considered duplicates, False otherwise.
    """
    if self.verbose > 0:
      print(f"Comparing {file1} and {file2} using hard comparison")

    file1Extension = os.path.splitext(file1)[1]
    file2Extension = os.path.splitext(file2)[1]

    if not self.type_check(file1Extension, file2Extension):
      return validate_file_contents(file1, file2)

    if file1Extension in self.videoExtensions:
      return VideoCompare(file1, file2, verbose=self.verbose, similarity=self.similarity).compare_videos_hard()

    if file1Extension in self.imageExtensions:
      return ImageCompare(file1, file2, verbose=self.verbose, similarity=self.similarity).image_pixel_differences()

    return validate_file_contents(file1, file2)

  def compare_files_soft(self, file1: str, file2: str) -> bool:
    """
    Compare two files using soft comparison.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.

    Returns:
        bool: True if the files are considered duplicates, False otherwise.
    """
    if self.verbose > 0:
      print(f"Comparing {file1} and {file2} using soft comparison")

    file1Extension = os.path.splitext(file1)[1]
    file2Extension = os.path.splitext(file2)[1]

    if not self.type_check(file1Extension, file2Extension):
      return False

    if file1.split('.')[-1] in self.videoExtensions:
      result = VideoCompare(file1, file2, verbose=self.verbose, similarity=self.similarity).compare_videos_soft()
      if self.verbose > 0:
        print(f"Video similarity: {result[1]}")
      return result[0]

    if file1.split('.')[-1] in self.imageExtensions:
      result = ImageCompare(file1, file2, verbose=self.verbose, similarity=self.similarity).image_similarity()
      if self.verbose > 0:
        print(f"Image similarity: {result[1]}")
      return result[0]

    # TODO: Implement soft comparison for different file types
    return False
    
  def search(self) -> None:
    """
    Search the directory for duplicate files.
    """
    allFiles = self.get_all_files()
    for i in range(len(allFiles)):
      for j in range(i+1, len(allFiles)):
        if self.compare_files(
            os.path.join(self.directory, allFiles[i]),
            os.path.join(self.directory, allFiles[j])
          ):
          if allFiles[i] not in self.duplicates:
            self.duplicates[allFiles[i]] = [allFiles[j]]

if __name__ == '__main__':
  duplicate = DuplicateFinder()
  
  duplicate.search()
  
  print(duplicate.duplicates)
    