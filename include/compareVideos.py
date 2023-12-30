
import cv2 as cv
import numpy as np
from filesDuplicateFinder.include.imageCompare import ImageCompare

class VideoCompare:
  
  def __init__(self, base_video: str, compare_video: str, verbose: int=0, similarity: float=0.85) -> None:
    self.base_video = base_video
    self.compare_video = compare_video
    self.verbose = verbose
    self.similarity = similarity
    
    # Read in the videos
    self.video1 = cv.VideoCapture(self.base_video)
    self.video2 = cv.VideoCapture(self.compare_video)

  def compare_videos_hard(self) -> bool:
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
        return False

      # Compare the frames
      if not np.array_equal(frame1, frame2):
        return False

    # If all frames are equal, return True
    return True

  def compare_videos_soft(self) -> tuple[bool, float]:
    # Get the frame count of each video
    video1_frames = int(self.video1.get(cv.CAP_PROP_FRAME_COUNT))
    video2_frames = int(self.video2.get(cv.CAP_PROP_FRAME_COUNT))
    
    # Get the frame rate of each video
    fps1 = int(self.video1.get(cv.CAP_PROP_FPS))
    fps2 = int(self.video2.get(cv.CAP_PROP_FPS))
    
    # Calculate the length of each video
    video1_length = video1_frames / fps1
    video2_length = video2_frames / fps2
    
    # If the videos have different lengths, return False
    if video1_length != video2_length:
      if self.verbose > 0:
        print("Videos have different lengths")
        print(f"Video 1: {video1_length} seconds")
        print(f"Video 2: {video2_length} seconds")
      return False, 0
    
    scores = []
    
    # Loop through each first frame of a second and compare them
    for i in range(0, video1_frames, fps1):
      # Set the frame position of each video
      self.video1.set(cv.CAP_PROP_POS_FRAMES, i)
      self.video2.set(cv.CAP_PROP_POS_FRAMES, i)
      
      # Read in the frames
      ret1, frame1 = self.video1.read()
      ret2, frame2 = self.video2.read()
      
      # If either frame is not read correctly, return False
      if not ret1 or not ret2:
        raise Exception("Error reading frames")
      
      # Compare the frames
      cmp = ImageCompare(frame1, frame2, self.verbose, False)
      score = cmp.image_similarity()
      
      scores.append(score)

    # If all frames are similar, return True
      return np.mean(scores) > self.similarity, np.mean(scores)
