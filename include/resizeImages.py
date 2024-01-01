import cv2 as cv
import numpy as np


class ImageResize:
  def __init__(self, image, verbose=0, show_images=False):
    self.image = image
    self.verbose = verbose
    self.show_images = show_images
    if type(image) != np.ndarray:
      self.cv_image = cv.imread(image)
      return
    
    self.cv_image = image
  
  def __pading_calc(self, aspect: float, sh: int, sw: int) -> tuple[int, int, int, int, int, int]:  
    # compute scaling and pad sizing
    # horizontal image
    if aspect > 1: 
      new_w = sw
      new_h = np.round(new_w/aspect).astype(int)
      pad_vert = (sh-new_h)/2
      pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
      pad_left, pad_right = 0, 0
      
      return pad_left, pad_right, pad_top, pad_bot, new_h, new_w
    
    # vertical image
    if aspect < 1: 
      new_h = sh
      new_w = np.round(new_h*aspect).astype(int)
      pad_horz = (sw-new_w)/2
      pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
      pad_top, pad_bot = 0, 0
      
      return pad_left, pad_right, pad_top, pad_bot, new_h, new_w
    
    # square image
    new_h, new_w = sh, sw
    pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0
    
    return pad_left, pad_right, pad_top, pad_bot, new_h, new_w
  
  def resize_and_pad(self, size: tuple[int, int], padColor: int = 0) -> np.ndarray:

    h, w = self.cv_image.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
      interp = cv.INTER_AREA
    else: # stretching image
      interp = cv.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h

    pad_left, pad_right, pad_top, pad_bot, new_h, new_w = self.__pading_calc(aspect, sh, sw)

    # set pad color
    if len(self.cv_image.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
      padColor = [padColor]*3

    # scale and pad
    scaled_img = cv.resize(self.cv_image, (new_w, new_h), interpolation=interp)
    scaled_img = cv.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv.BORDER_CONSTANT, value=padColor)

    return scaled_img