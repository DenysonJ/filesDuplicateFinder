import unittest

from include.imageCompare import ImageCompare


class TestImageCompare(unittest.TestCase):
  def test_image_compare_hard(self):
    self.assertFalse(ImageCompare('fixtures/sample_640x426.bmp', 'fixtures/sample_1280x853.bmp').image_pixel_differences())
    self.assertTrue(ImageCompare('fixtures/sample_640x426.bmp', 'fixtures/sample_640x426.bmp').image_pixel_differences())
    
  def test_image_compare_soft(self):
    result = []
    result.append(ImageCompare('fixtures/sample_640x426.bmp', 'fixtures/sample_1280x853.bmp').image_similarity())
    result.append(ImageCompare('fixtures/sample_640x426.bmp', 'fixtures/sample_640x426.bmp').image_similarity())
    self.assertTrue(result[0][0])
    self.assertTrue(result[1][0])
    self.assertGreaterEqual(result[0][1], 0.85)
    self.assertEqual(result[1][1], 1.0)