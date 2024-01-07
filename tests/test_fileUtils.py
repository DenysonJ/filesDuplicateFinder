import unittest

import include.files as files


class TestFileUtils(unittest.TestCase):
  def test_get_file_size(self):
    self.assertEqual(files.return_file_size('fixtures/test1.txt'), 13)
    self.assertEqual(files.return_file_size('fixtures/test2.txt'), 13)
    self.assertEqual(files.return_file_size('fixtures/test3.txt'), 12)

  def test_get_file_create_time(self):
    self.assertEqual(files.return_file_create_time('fixtures/test1.txt'), 1704582745.2046244)
    self.assertEqual(files.return_file_create_time('fixtures/test2.txt'), 1704582745.2126243)
    self.assertEqual(files.return_file_create_time('fixtures/sample_960x400_ocean_with_audio.mov'), 1704582745.0025537)

  def test_get_files(self):
    allFiles = files.get_files('fixtures')
    fixtures = ['fixtures/test1.txt', 
                  'fixtures/test2.txt', 
                  'fixtures/test3.txt', 
                  'fixtures/sample_960x400_ocean_with_audio.mov',
                  'fixtures/594_900x900.jpg',
                  'fixtures/sample_640x360.mp4',
                  'fixtures/sample_960x540.mp4',
                  'fixtures/sample_640x426.bmp',
                  'fixtures/sample_1280x853.bmp']
    for file in fixtures:
      with self.subTest(file=file):
        self.assertIn(file, allFiles)

  def test_get_files_recursive(self):
    allFiles = files.get_recursive_files('fixtures')
    fixtures = ['fixtures/test1.txt', 
                  'fixtures/test2.txt', 
                  'fixtures/test3.txt', 
                  'fixtures/sample_960x400_ocean_with_audio.mov',
                  'fixtures/594_900x900.jpg',
                  'fixtures/sample_640x360.mp4',
                  'fixtures/sample_960x540.mp4',
                  'fixtures/sample_640x426.bmp',
                  'fixtures/sample_1280x853.bmp',
                  'fixtures/images_sizes/sample-images-05.jpeg',
                  'fixtures/images_sizes/R.jpg']
    for file in fixtures:
      with self.subTest(file=file):
        self.assertIn(file, allFiles)