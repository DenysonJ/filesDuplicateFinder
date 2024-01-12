import unittest
import sys

from numpy import ndarray

from include.imageCompare import ImageCompare


class TestImageCompare(unittest.TestCase):
  def test_image_compare_hard(self):
    self.assertFalse(ImageCompare(
                      'fixtures/sample_640x426.bmp',
                      'fixtures/sample_1280x853.bmp').image_pixel_differences())
    self.assertTrue(ImageCompare(
                      'fixtures/sample_640x426.bmp',
                      'fixtures/sample_640x426.bmp').image_pixel_differences())
    
  def test_image_compare_soft_equal(self):
    result = ImageCompare(
        'fixtures/sample_640x426.bmp',
        'fixtures/sample_640x426.bmp').image_similarity()
    self.assertTrue(result[0])
    self.assertEqual(result[1], 1.0)
    
  def test_image_compare_soft_similar(self):
    result = ImageCompare(
        'fixtures/sample_640x426.bmp',
        'fixtures/sample_1280x853.bmp').image_similarity()
    self.assertTrue(result[0])
    self.assertGreaterEqual(result[1], 0.85)
    
  def test_image_compare_soft_different(self):
    result = ImageCompare(
              'fixtures/sample_640x426.bmp',
              'fixtures/594_900x900.jpg').image_similarity()
    self.assertFalse(result[0])
    self.assertLess(result[1], 0.85)

  def test_image_compare_verbose(self):
    ImageCompare(
      'fixtures/sample_640x426.bmp',
      'fixtures/594_900x900.jpg',
      verbose=1).image_similarity()
    output = sys.stdout.getvalue().strip()
    self.assertEqual(output, 'Image similarity (SSIM): 0.1777')

  def test_image_reverse_resolution(self):
    result = ImageCompare(
      'fixtures/images_sizes/sample-images-05.jpeg',
      'fixtures/images_sizes/R.jpg').image_similarity()
    self.assertFalse(result[0])

  def test_show_images(self):
    result = ImageCompare(
      'fixtures/sample_640x426.bmp',
      'fixtures/594_900x900.jpg',
      show_images=True).image_similarity()
    
    self.assertIsInstance(result[2][0], ndarray)
    self.assertIsInstance(result[2][1], ndarray)
    self.assertIsInstance(result[2][2], ndarray)
    self.assertEqual(result[2][0].shape, (426, 640))
    self.assertEqual(result[2][1].shape, (426, 640, 3))
    self.assertEqual(result[2][2].shape, (426, 640, 3))