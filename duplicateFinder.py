import os
from argparse import ArgumentParser
from typing import Callable, Any, Sequence

from include.videoCompare import VideoCompare
from include.imageCompare import ImageCompare
from include.fileByteCompare import validate_file_contents
import include.files as files


def parser() -> ArgumentParser:
  """
  Parse command line arguments.

  Returns:
      ArgumentParser: The argument parser object.
  """
  parser = ArgumentParser(
      description='Find duplicate files in the given directory.')
  parser.add_argument('--version', action='version',
                      version='%(prog)s 1.0.0')

  parser.add_argument(
      '-d', '--directory', help='Find duplicates on this directory', default='.', type=str)
  parser.add_argument(
      '-v', '--verbose', help='Print verbose output', action='count', default=0)
  parser.add_argument(
      '-s', '--similarity', help='Set the similarity threshold', default=0.85, type=float)
  parser.add_argument(
      '-t', '--type', help='Set the type of comparison to use',
      choices=['soft', 'hard'], default='hard', type=str)
  parser.add_argument(
      '-r', '--recursive', help='Recursively search the directory', action='store_true')
  parser.add_argument(
      '-a', '--action', help='Action to take on duplicate files',
      choices=['delete', 'move', 'link'], default='delete', type=str)
  parser.add_argument(
      '-b', '--bulk', help='Confirm delete on all duplicate files, otherwise confirm each file',
      action='store_true')
  parser.add_argument(
      '-o', '--output', help='Output directory to write duplicate files',
      default='duplicated', type=str)

  parser.add_argument(
      '-f', '--fileChoice', help='Choose which file to keep', 
      choices=['first', 'last', 'bigger', 'smaller', 'best'], default='first', type=str)

  group = parser.add_mutually_exclusive_group()

  group.add_argument(
      '-e', '--exclude', help='Exclude from the search all these file extensions',
      nargs='+', default=[], type=str)
  group.add_argument(
      '-i', '--include', help='Include in the search only these file extensions',
      nargs='+', default=[], type=str)

  return parser


class DuplicateFinder:
  """
  Class to find duplicate files in a given directory.

  Attributes:
      directory (str): The directory to search for duplicate files.
      verbose (int): The level of verbosity for output.
      bulk (bool): Flag to indicate whether to confirm action on all duplicate files.
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
      fileChoice (str): How to choose a file to keep when there are duplicates
      duplicates (dict): Dictionary to store duplicate files.

  Methods:
      main(): Search for all duplicated an perform the choosed action over them
      search(): Get all duplicated files in the given directory with the given option
      get_all_files(): Get all files in the directory with the given option.
      compare_files(file1: str, file2: str) -> bool: Compare two files.
      compare_files_hard(file1: str, file2: str) -> bool: Compare two files \
          using hard comparison.
      compare_files_soft(file1: str, file2: str) -> bool: Compare two files \
          using soft comparison.
  """

  videoExtensions = {'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm'}
  imageExtensions = {'jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'tif'}

  def __init__(self, args: Sequence[str] | None = None) -> None:
    self.args = parser().parse_args(args)

    self.directory = self.args.directory
    self.verbose = self.args.verbose
    self.bulk = self.args.bulk
    self.similarity = self.args.similarity
    self.type = self.args.type
    self.recursive = self.args.recursive
    self.exclude = self.args.exclude
    self.include = self.args.include
    self.action = self.args.action
    self.output = self.args.output
    self.fileChoice = self.args.fileChoice

    self.duplicates = {}
    self.countDuplicates = 0

  def get_all_files(self) -> list[str]:
    """
    Get all files in the directory.

    Returns:
        list[str]: List of file paths.
    """
    allFiles = []

    allFiles = files.get_files(self.directory) if not self.recursive else files.get_recursive_files(self.directory)

    allFiles = filter(lambda x: os.path.splitext(x)[1] not in self.exclude, allFiles)

    if self.include:
      allFiles = filter(lambda x: os.path.splitext(x)[1] in self.include, allFiles)

    return list(allFiles)

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

    file1Extension = os.path.splitext(file1)[1].replace('.', '')
    file2Extension = os.path.splitext(file2)[1].replace('.', '')

    if not self.type_check(file1Extension, file2Extension):
      return validate_file_contents(file1, file2)

    if file1Extension in self.videoExtensions:
      return VideoCompare(file1, file2, verbose=self.verbose, 
                          similarity=self.similarity).compare_videos_hard()

    if file1Extension in self.imageExtensions:
      return ImageCompare(file1, file2, verbose=self.verbose, 
                          similarity=self.similarity).image_pixel_differences()

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
      result = VideoCompare(file1, file2, verbose=self.verbose, 
                            similarity=self.similarity).compare_videos_soft()
      if self.verbose > 0:
        print(f"Video similarity: {result[1]}")
      return result[0]

    if file1.split('.')[-1] in self.imageExtensions:
      result = ImageCompare(file1, file2, verbose=self.verbose, 
                            similarity=self.similarity).image_similarity()
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
            allFiles[i],
            allFiles[j]
          ):
          if allFiles[i] not in self.get_all_duplicates():
            self.duplicates[allFiles[i]] = set([allFiles[j]])
            self.countDuplicates += 1
            continue
          if allFiles[j] not in self.get_all_duplicates():
            self.duplicates[allFiles[i]].add(allFiles[j])
            self.countDuplicates += 1

  def get_all_duplicates(self) -> set[str]:
    """
    Get all duplicate files.

    Returns:
        list[str]: List of duplicate files.
    """
    if len(self.duplicates) == 0:
      return set()
    
    nestedList = list(self.duplicates.keys()) + [
      item for sublist in list(self.duplicates.values()) for item in sublist]
    
    return set(nestedList)

  def order_by_info(self, list: list[str], func: Callable[[str], Any], reverse: bool) -> list[str]:
    """
    Orders the given list of files based on the information returned by the provided function.

    Args:
      list (list[str]): The list of files to be ordered.
      func (Callable[[str], Any]): A function that takes a file path as input and
        returns the information used for ordering.
      reverse (bool): If True, the list will be ordered in reverse (descending)
        order. If False, the list will be ordered in ascending order.

    Returns:
      list[str]: The ordered list of files.
    """
    dic = [(func(file), file) for file in list]
    sort_list = sorted(dic, key=lambda x: x[0], reverse=reverse)

    return [file[1] for file in sort_list]

  def order_by_best_quality(self, list: list[str], reverse: bool) -> list[str]:
    """
    Orders the given list of files based on the quality of the file.
    Args:
        list (list[str]): The list of files to be ordered.
        reverse (bool): If True, the list will be ordered in reverse (descending)
        order. If False, the list will be ordered in ascending order.

    Returns:
        list[str]: The ordered list of files.
    """
    fileExtension = os.path.splitext(list[0])[1]
    fileExtension = fileExtension.replace('.', '')
    if fileExtension in self.videoExtensions:
      return self.order_by_info(list, files.get_video_pixels, reverse)

    if fileExtension in self.imageExtensions:
      return self.order_by_info(list, files.get_pixels, reverse)

    raise NotImplementedError(f"ERROR: Ordering by best quality is not" \
      " implemented for {} files.".format(fileExtension))

  def choose_duplicate(self) -> dict[str, set[str]]:
    """
    Choose which duplicate file to keep.

    Returns: 
      dict[str, list[str]]: A dictionary containing the file to keep as the key
        and the files to delete/move/link as the values.
    """
    choice = {
      'first': lambda x: self.order_by_info(x, files.return_file_create_time, False),
      'last': lambda x: self.order_by_info(x, files.return_file_create_time, True),
      'bigger': lambda x: self.order_by_info(x, files.return_file_size, True),
      'smaller': lambda x: self.order_by_info(x, files.return_file_size, False),
      'best': lambda x: self.order_by_best_quality(x, True)
    }[self.fileChoice]

    duplicates = {}

    for file in self.duplicates:
      list = choice([*self.duplicates[file], file])
      duplicates[list[0]] = set(list[1:])

    if self.verbose > 0:
      print(duplicates)

    return duplicates

  def delete_duplicates(self, dic: dict[str, set[str]]) -> None:
    """
    Delete duplicate files.
    """
    if self.bulk:
      for file in dic:
        for duplicate in dic[file]:
          os.remove(duplicate)
      return
    
    for file in dic:
      for duplicate in dic[file]:
        read = input(f"Are you sure you want to delete {duplicate}? (y/n): ")
        if read.lower() == 'y':
          os.remove(duplicate)

  def move_duplicates(self, dic: dict[str, set[str]]) -> None:
    """
    Move duplicate files.
    """
    os.makedirs(self.output, exist_ok=True)
    for file in dic:
      for duplicate in dic[file]:
        fileName = os.path.basename(duplicate)
        os.rename(duplicate, os.path.join(self.output, fileName))

  def link_duplicates(self, dic: dict[str, set[str]]) -> None:
    """
    Create soft links for duplicate files.
    """
    os.makedirs(self.output, exist_ok=True)
    for file in dic:
      for duplicate in dic[file]:
        fileName = os.path.basename(duplicate)
        os.symlink(os.path.abspath(duplicate), os.path.join(self.output, fileName))

  def action_on_duplicates(self, dic: dict[str, set[str]]) -> None:
    """
    Perform the action on duplicate files.
    """
    {
      'delete': self.delete_duplicates,
      'move': self.move_duplicates,
      'link': self.link_duplicates
    }[self.action](dic)
  
  def print_duplicates(self) -> None:
    """
    Print the duplicate files.
    """
    for file in self.duplicates:
      print(file)
      for duplicate in self.duplicates[file]:
        print(f"\t{duplicate}")

  def main(self) -> None:
    """
    Main function.
    """
    self.search()
    if self.bulk and self.action == 'delete':
      read = input("Are you sure you want to delete all {} duplicated files? (y/n): "
                   .format(self.countDuplicates))
      if read.lower() == 'y':
        self.action_on_duplicates(self.choose_duplicate())
        return
      
      self.print_duplicates()
      # which action to take if the user doesn't confirm?
      return
    
    self.action_on_duplicates(self.choose_duplicate())

if __name__ == '__main__':
  duplicate = DuplicateFinder()

  duplicate.main()