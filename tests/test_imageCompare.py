import unittest

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