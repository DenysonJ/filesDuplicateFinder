import os


def get_recursive_files(directory: str) -> list[str]:
  """
  Get all files in the directory recursively.

  Returns:
      list[str]: List of file paths.
  """
  return [os.path.join(dirpath, f) 
          for (dirpath, dirnames, filenames) 
          in os.walk(directory) 
            for f in filenames]

def get_files(directory: str) -> list[str]:
  """
  Get all files in the directory.

  Returns:
      list[str]: List of file paths.
  """
  return [os.path.join(directory, f) for f in os.listdir(directory)
            if isFile(f, directory)]
  
def isFile(file: str, dir: str) -> bool:
  """ Check if the file is a file.

  Args:
      file (str): Name of the file.
      dir (str): Path to the directory containing the file.

  Returns:
      bool: True if the file is a file, False otherwise.
  """
  return os.path.isfile(os.path.join(dir, file))

def return_file_create_time(file: str) -> float:
  """
  Get the creation time of the file.

  Args:
      file (str): Path to the file.

  Returns:
      float: Creation time of the file.
  """
  # works on Windows only?
  return os.path.getctime(file)

def return_file_size(file: str) -> int:
  """
  Get the size of the file.

  Args:
      file (str): Path to the file.

  Returns:
      int: Size of the file.
  """
  return os.path.getsize(file)

def get_image_resolution(image: str) -> tuple[int, int]:
  """
  Get the resolution of the image.

  Args:
      image (str): Path to the image.

  Returns:
      tuple[int, int]: Resolution of the image.
  """
  import cv2 as cv
  return cv.imread(image).shape[:2]

def get_video_info(video: str) -> tuple[int, int, float]:
  """
  Get the resolution and fps of the video.

  Args:
      video (str): Path to the video.

  Returns:
      tuple[int, int, float]: Resolution and fps of the video.
  """
  import cv2 as cv
  cap = cv.VideoCapture(video)
  width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
  height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
  fps = cap.get(cv.CAP_PROP_FPS)
  return (width, height, fps)

def get_pixels(image: str) -> int:
  """
  Get the number of pixels in the resolution.

  Args:
      resolution (tuple[int, int]): Resolution of the image.

  Returns:
      int: Number of pixels in the resolution.
  """
  resolution = get_image_resolution(image)
  return resolution[0] * resolution[1]

def get_video_pixels(video: str) -> float:
  """
  Get the number of pixels in the video.

  Args:
      resolution (tuple[int, int]): Resolution of the video.
      fps (float): Frames per second of the video.

  Returns:
      float: Number of pixels in the video.
  """
  width, height, fps = get_video_info(video)
  return width * height * fps