from unittest.mock import patch
import unittest
import os
import shutil

from duplicateFinder import DuplicateFinder


class TestDuplicate(unittest.TestCase):
  @classmethod
  def setUpClass(self) -> None:
    shutil.copytree('fixtures', 'fixtures_copy')

  @classmethod
  def tearDownClass(self) -> None:
    shutil.rmtree('fixtures_copy', ignore_errors=True)
    shutil.rmtree('duplicated', ignore_errors=True)

  def test_get_all_files_include(self) -> None:
    duplicateFinder = DuplicateFinder(['-d', 'fixtures', '-i', '.mp4'])
    allFiles = duplicateFinder.get_all_files()

    for file in allFiles:
      fileExtension = os.path.splitext(file)[1]
      self.assertEqual(fileExtension, '.mp4')

    self.assertEqual(allFiles, ['fixtures/sample_640x360.mp4', 'fixtures/sample_960x540.mp4'])

  def test_get_all_files_exclude(self) -> None:
    duplicateFinder = DuplicateFinder(['-d', 'fixtures', '-e', '.mp4'])
    allFiles = duplicateFinder.get_all_files()

    for file in allFiles:
      fileExtension = os.path.splitext(file)[1]
      self.assertNotEqual(fileExtension, '.mp4')

    self.assertEqual(set(allFiles), set([
      'fixtures/copy_sample.bmp',
      'fixtures/594_900x900.jpg',
      'fixtures/sample_640x426.bmp',
      'fixtures/sample_960x400_ocean_with_audio.mov',
      'fixtures/sample_1280x853.bmp',
      'fixtures/test1.txt',
      'fixtures/test2.txt',
      'fixtures/test3.txt']))

  def test_get_all_files_recursive(self) -> None:
    duplicateFinder = DuplicateFinder(['-d', 'fixtures', '-r'])
    allFiles = duplicateFinder.get_all_files()

    self.assertEqual(set(allFiles), set([
      'fixtures/copy_sample.bmp',
      'fixtures/sample_960x540.mp4',
      'fixtures/sample_640x360.mp4',
      'fixtures/594_900x900.jpg',
      'fixtures/sample_640x426.bmp',
      'fixtures/sample_960x400_ocean_with_audio.mov',
      'fixtures/sample_1280x853.bmp',
      'fixtures/test1.txt',
      'fixtures/test2.txt',
      'fixtures/test3.txt',
      'fixtures/images_sizes/R.jpg',
      'fixtures/images_sizes/sample-images-05.jpeg']))

  def test_search_duplicates_hard(self) -> None:
    duplicateFinder = DuplicateFinder(['-d', 'fixtures', '-v'])
    duplicateFinder.search()

    duplicated = duplicateFinder.duplicates

    self.assertEqual(duplicated, {
      'fixtures/copy_sample.bmp': set(['fixtures/sample_640x426.bmp']),
      'fixtures/test1.txt': set(['fixtures/test2.txt'])
    })

  def test_search_duplicates_soft_best(self) -> None:
    duplicateFinder = DuplicateFinder(['-d', 'fixtures', '-t', 'soft', '-f', 'best'])
    duplicateFinder.search()
    duplicated = duplicateFinder.choose_duplicate()

    self.assertEqual(duplicated, {
      'fixtures/sample_1280x853.bmp': set(['fixtures/copy_sample.bmp', 'fixtures/sample_640x426.bmp']),
      'fixtures/sample_960x540.mp4': set(['fixtures/sample_640x360.mp4'])
    })

  @patch('builtins.input', lambda *args: 'y')
  def test_search_duplicates_delete(self) -> None:  
    duplicateFinder = DuplicateFinder(['-d', 'fixtures_copy', '-t', 'soft', '-f', 'best', '-i', '.bmp', '-b'])
    duplicateFinder.main()

    self.assertFalse(os.path.exists('fixtures_copy/copy_sample.bmp'))
    self.assertFalse(os.path.exists('fixtures_copy/sample_640x426.bmp'))

  @patch('builtins.input', lambda *args: 'y')
  def test_search_duplicates_move(self) -> None:  
    duplicateFinder = DuplicateFinder(['-d', 'fixtures_copy', '-t', 'soft', '-f', 'best', '-i', '.mp4', '-a', 'move'])
    duplicateFinder.main()

    self.assertFalse(os.path.exists('fixtures_copy/sample_640x360.mp4'))
    self.assertTrue(os.path.exists('duplicated/sample_640x360.mp4'))
    self.assertFalse(os.path.islink('duplicated/sample_640x360.mp4'))

  @patch('builtins.input', lambda *args: 'y')
  def test_search_duplicates_link(self) -> None:
    duplicateFinder = DuplicateFinder(['-d', 'fixtures', '-t', 'soft', '-f', 'best', '-i', '.mp4', '-a', 'link'])
    duplicateFinder.main()

    self.assertTrue(os.path.exists('duplicated/sample_640x360.mp4'))
    self.assertTrue(os.path.islink('duplicated/sample_640x360.mp4'))