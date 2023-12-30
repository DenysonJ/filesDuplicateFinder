from argparse import ArgumentParser
from include.compareVideos import VideoCompare
from include.imageCompare import ImageCompare
from include.fileByteCompare import validate_file_contents

def parseArgs():
  parser = ArgumentParser(description='Find duplicate files in the given directory.')
  parser.add_argument('--version', action='version', version='%(prog)s 0.1')
  
  parser.add_argument('-d', '--directory', help='Find duplicates on this directory', default='.', type=str)
  
  
  
  return parser

if __name__ == '__main__':
  parser = parseArgs()
  args = parser.parse_args()
  
  print(args)