from sys import argv
from PIL import Image
from PIL import ImageChops
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity
import cv2 as cv
import numpy as np

class ImageCompare:
  """
  Class to compare images
  """
  def __init__(self, base_image, compare_image):
    self.base_image = base_image
    self.compare_image = compare_image
    self.cv_base_image = cv.imread(base_image)
    self.cv_compare_image = cv.imread(compare_image)
  
  def image_pixel_differences(self):
    """
    Calculates the bounding box of the non-zero regions in the image.
    :param base_image: target image to find
    :param compare_image:  set of images containing the target image
    :return: The bounding box is returned as a 4-tuple defining the
            left, upper, right, and lower pixel coordinate. If the image
            is completely empty, this method returns None.
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

  def image_similarity_histogram(self):
    """
    Calculates de similarity between two images using the histogram algorithm
    """
    
    color = ('b','g','r')
    hist_img1 = []
    hist_img2 = []
    for i,col in enumerate(color):
      histr = cv.calcHist([self.cv_base_image],[i],None,[256],[0,256])
      plt.plot(histr,color = col)
      plt.xlim([0,256])
      hist_img1.append(histr)
    plt.show()
    
    for i,col in enumerate(color):
      histr = cv.calcHist([self.cv_compare_image],[i],None,[256],[0,256])
      plt.plot(histr,color = col)
      plt.xlim([0,256])
      hist_img2.append(histr)
    plt.show()

    # Compare the histograms
    
  def image_similarity(self):
    """
    Calculates de similarity between two images using the SSIM algorithm
    """

    # Convert images to grayscale
    first_gray = cv.cvtColor(self.cv_base_image, cv.COLOR_BGR2GRAY)
    secon_gray = cv.cvtColor(self.cv_compare_image, cv.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(first_gray, secon_gray, full=True)
    print("Image similarity", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1] 
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv.threshold(diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    contours = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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

    cv.imshow('base img', self.cv_base_image)
    cv.imshow('cmp img', self.cv_compare_image)
    cv.imshow('diff', diff)
    cv.imshow('mask', mask)
    cv.imshow('filled after', filled_after)
    cv.waitKey(0)
    
    return score

if __name__ == '__main__':
  img_cmp = ImageCompare(argv[1], argv[2])
  
  img_cmp.image_similarity()
  if img_cmp.image_pixel_differences():
    print("Images are the same")
    exit(0)
  print("Images are different")
  