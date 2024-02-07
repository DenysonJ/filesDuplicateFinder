import cv2 as cv
import numpy as np
import logging

from include.imageCompare import ImageCompare


class FrameError(Exception):
  """
  Exception raised when a frame is not read correctly.
  """
  pass


class VideoCompare:
  """
  Class for comparing two videos based on their frames.

  Args:
    base_video (str): Path to the base video file.
    compare_video (str): Path to the video file to compare with the base video.
    verbose (int, optional): Verbosity level. Defaults to 0.
    similarity (float, optional): Similarity threshold for considering frames 
      as equal. Defaults to 0.85.
    timeThreshold (float, optional): Time threshold for considering videos as
      equal in length. Defaults to 1. Length is in seconds.

  Attributes:
    base_video (str): Path to the base video file.
    compare_video (str): Path to the video file to compare with the base video.
    verbose (int): Verbosity level.
    similarity (float): Similarity threshold for considering frames as equal.
    video1 (cv2.VideoCapture): VideoCapture object for the base video.
    video2 (cv2.VideoCapture): VideoCapture object for the compare video.

  Methods:
    compare_videos_hard: Compares the two videos strictly, frame by frame.
    compare_videos_soft: Compares the two videos with a similarity threshold.

  """

  def __init__(
    self, base_video: str, compare_video: str, verbose: int=0, similarity: float=0.85, timeThreshold: float=1) -> None:

    self.base_video = base_video
    self.compare_video = compare_video
    self.verbose = verbose
    self.similarity = similarity
    self.timeThreshold = timeThreshold

    # Read in the videos
    self.video1 = cv.VideoCapture(self.base_video)
    self.video2 = cv.VideoCapture(self.compare_video)

  def compare_videos_hard(self) -> bool:
    """
    Compares the two videos strictly, frame by frame.

    Returns:
      bool: True if the videos are identical, False otherwise.
    """
    # Get the frame count of each video
    video1_frames = int(self.video1.get(cv.CAP_PROP_FRAME_COUNT))
    video2_frames = int(self.video2.get(cv.CAP_PROP_FRAME_COUNT))

    # If the videos have different frame counts, return False
    if video1_frames != video2_frames:
      return False

    # Loop through each frame and compare them
    for i in range(video1_frames):
      # Read in the frames
      ret1, frame1 = self.video1.read()
      ret2, frame2 = self.video2.read()

      # If either frame is not read correctly, return False
      if not ret1 or not ret2:
        raise FrameError("Error reading frames. Frame count: {}".format(i))

      # Compare the frames
      if not np.array_equal(frame1, frame2):
        return False

    # If all frames are equal, return True
    return True

  def compare_videos_soft(self, scale: int=1) -> tuple[bool, float]:
    """
    Compares the two videos with a similarity threshold.

    Args:
      scale (int, optional): The scale of the frames to compare. Defaults to 1.
      This is used to skip x frames when comparing the videos, where x will be 
      equal to scale * fps.

    Returns:
      tuple[bool, float]: A tuple containing a boolean indicating if the videos
        are similar and the average similarity score.
    """
    # Get the frame count of each video
    video1_frames = int(self.video1.get(cv.CAP_PROP_FRAME_COUNT))
    video2_frames = int(self.video2.get(cv.CAP_PROP_FRAME_COUNT))

    # Get the frame rate of each video
    fps1 = self.video1.get(cv.CAP_PROP_FPS)
    fps2 = self.video2.get(cv.CAP_PROP_FPS)

    # Calculate the length of each video
    video1_length = video1_frames / fps1
    video2_length = video2_frames / fps2

    # If the videos have different lengths, return False
    if (video1_length >= video2_length + self.timeThreshold or
      video1_length <= video2_length - self.timeThreshold):
      if self.verbose > 0:
        print("Videos have different lengths")
        print("Video 1: {:.4f} seconds".format(video1_length))
        print("Video 2: {:.4f} seconds".format(video2_length))
      logging.info(f"Videos have different lengths => Video 1: {video1_length}\
        seconds vs Video 2: {video2_length}")
      return False, 0

    if scale * fps1 > video1_frames or scale * fps2 > video2_frames:
      raise ValueError("Scale is too large for the video")

    if scale * fps1 < 1 or scale * fps2 < 1:
      raise ValueError("Scale is too small for the video")

    scores = []

    # Loop through each first frame of scale of fps and compare them
    for i in range(0, min(video1_frames, video2_frames), int(scale)):
      f1 = i * fps1
      f2 = i * fps2
      
      if f1 >= video1_frames or f2 >= video2_frames:
        break
      
      # Set the frame position of each video
      self.video1.set(cv.CAP_PROP_POS_FRAMES, int(f1))
      self.video2.set(cv.CAP_PROP_POS_FRAMES, int(f2))

      # Read in the frames
      ret1, frame1 = self.video1.read()
      ret2, frame2 = self.video2.read()

      # If either frame is not read correctly, return False
      if not ret1 or not ret2:
        logging.warning(f"Error reading frames. Frame count: {f1} and {f2}")
        logging.warning(f"File 1: {self.base_video} File 2: {self.compare_video}")
        # If previous frames were read correctly, return the average score
        # > 1 because it assumes that the first frame is not enough to comparison
        if len(scores) > 1:
          break
          # result = np.mean(scores)
          # if self.verbose > 0:
          #   print("Video similarity (SSIM): {:.4f}".format(result))
          # return result >= self.similarity, result
        raise FrameError("Error reading frames. Frame count: {f1} and {f2}".format(f1, f2))

      # Compare the frames
      cmp = ImageCompare(frame1, frame2, self.verbose - 1, False)
      score = cmp.image_similarity()

      scores.append(score[1])

    result = np.mean(scores)

    if self.verbose > 0:
      print("Video similarity (SSIM): {:.4f}".format(result))
    logging.info(f"Video similarity (SSIM): {result}")

    # If all frames are similar, return True
    return result >= self.similarity, result 
