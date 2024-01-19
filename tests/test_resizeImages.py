import unittest

from numpy import ndarray

from include.resizeImages import ImageResize


class TestImageResize(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.img1 = ImageResize('fixtures/images_sizes/R.jpg')
    self.img2 = ImageResize('fixtures/images_sizes/sample-images-05.jpeg')
  
  def test_stretch_image(self):
    size = (1300, 1700)
    result = self.img1.resize_and_pad(size)
    
    self.assertEqual(result.shape[:2], size)
    self.assertIsInstance(result, ndarray)
  
  def test_shrink_image(self):
    size = (800, 1200)
    result = self.img2.resize_and_pad(size)
    
    self.assertEqual(result.shape[:2], size)
    self.assertIsInstance(result, ndarray)