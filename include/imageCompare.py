from sys import argv

from PIL import Image
from PIL import ImageChops
import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity

class ImageCompare:
  """
  Class to compare images
  """
  def __init__(
    self, base_image, compare_image, verbose=0, show_images=False, similarity=0.85):
    
    if type(base_image) != np.ndarray:
      self.base_image = base_image
      self.cv_base_image = cv.imread(base_image)
  
    if type(compare_image) != np.ndarray:
      self.compare_image = compare_image
      self.cv_compare_image = cv.imread(compare_image)
    
    if type(base_image) == np.ndarray:
      self.cv_base_image = base_image
    
    if type(compare_image) == np.ndarray:
      self.cv_compare_image = compare_image
    
    self.verbose = verbose
    self.show_images = show_images
    self.similarity = similarity
    
    h1, w1 = self.cv_base_image.shape[:2]
    h2, w2 = self.cv_compare_image.shape[:2]
    
    if h1 > h2 or w1 > w2:
      self.cv_base_image = cv.resize(self.cv_base_image, (w2, h2))
      return
    
    if h1 < h2 or w1 < w2:
      self.cv_compare_image = cv.resize(self.cv_compare_image, (w1, h1))
      return
  
  
  def image_pixel_differences(self) -> bool:
    """
    Calculates the bounding box of the non-zero regions in the image.
    
    Returns: 
      bool: If the images have the same pixels, return True, otherwise False.
    """
    # Open the images to compare as PIL images
    
    base_image_pil = Image.open(self.base_image)
    compare_image_pil = Image.open(self.compare_image)
    
    # Returns the absolute value of the pixel-by-pixel
    # difference between two images.

    diff = ImageChops.difference(base_image_pil, compare_image_pil)
    if diff.getbbox():
      return False
    else:
      return True
    
  def image_similarity(
    self) -> tuple[bool, float] | tuple[bool,
                                        float,
                                        tuple[
                                          np.ndarray,
                                          np.ndarray,
                                          np.ndarray]]:
    """
    Calculates de similarity between two images using the SSIM algorithm
    
    Returns:
      tuple[bool, float]: A tuple containing a boolean indicating if the images
        are similar and the average similarity score.
    """

    # Convert images to grayscale
    first_gray = cv.cvtColor(self.cv_base_image, cv.COLOR_BGR2GRAY)
    secon_gray = cv.cvtColor(self.cv_compare_image, cv.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(first_gray, secon_gray, full=True)
    
    if self.verbose > 0:
      print("Image similarity (SSIM): {:.4f}".format(score))
    
    if not self.show_images:
      return self.similarity <= score, score

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1] 
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv.threshold(diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    contours = cv.findContours(
      thresh.copy(),
      cv.RETR_EXTERNAL,
      cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(self.cv_base_image.shape, dtype='uint8')
    filled_after = self.cv_compare_image.copy()

    for c in contours:
      area = cv.contourArea(c)
      if area > 40:
        x,y,w,h = cv.boundingRect(c)
        cv.rectangle(self.cv_base_image, (x, y), (x + w, y + h), (36,255,12), 2)
        cv.rectangle(self.cv_compare_image, (x, y), (x + w, y + h), (36,255,12), 2)
        cv.drawContours(mask, [c], 0, (0,255,0), -1)
        cv.drawContours(filled_after, [c], 0, (0,255,0), -1)
    
    return self.similarity <= score, score, (diff, mask, filled_after)
