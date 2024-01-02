import unittest
import sys

from include.videoCompare import VideoCompare


class TestVideoCompare(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.similar = VideoCompare(
                      'fixtures/sample_640x360.mp4',
                      'fixtures/sample_960x540.mp4')
    self.equal = VideoCompare(
                      'fixtures/sample_640x360.mp4',
                      'fixtures/sample_640x360.mp4')
    self.different = VideoCompare(
                      'fixtures/sample_640x360.mp4',
                      'fixtures/sample_960x400_ocean_with_audio.mov')
      
  def test_image_compare_hard(self):
    self.assertFalse(self.similar.compare_videos_hard())
    self.assertTrue(self.equal.compare_videos_hard())
    
  def test_image_compare_soft_equal(self):
    result = self.equal.compare_videos_soft()
    self.assertTrue(result[0])
    self.assertEqual(result[1], 1.0)
    
  def test_image_compare_soft_similar(self):
    result = self.similar.compare_videos_soft()
    self.assertTrue(result[0])
    self.assertGreaterEqual(result[1], 0.85)
    
  def test_image_compare_soft_different(self):
    result = self.different.compare_videos_soft()
    self.assertFalse(result[0])
    self.assertLess(result[1], 0.85)

  def test_image_compare_verbose(self):
    message = "Videos have different lengths\n"
    m1 = "Video 1: 13.7931 seconds\n"
    m2 = "Video 2: 48.5217 seconds"
    message += m1 + m2
    self.different.verbose = 1
    self.different.compare_videos_soft()
    output = sys.stdout.getvalue().strip()
    self.assertEqual(output, message)
  
  def test_image_compare_verbose_similar(self):
    message = "Video similarity (SSIM): 0.9791"
    self.similar.verbose = 1
    self.similar.compare_videos_soft()
    output = sys.stdout.getvalue().strip()
    self.assertEqual(output, message)