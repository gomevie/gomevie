import unittest
from main import read_file, tokenize, calculate_similarity, write_output
from unittest.mock import patch, mock_open
import numpy as np

class TestPlagiarismDetector(unittest.TestCase):
    def test_read_file(self):
        content = read_file('orig.txt')
        self.assertIsInstance(content, str)
        self.assertTrue(content)

    def test_read_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file('nonexistent.txt')

    def test_calculate_similarity_identical(self):
        similarity = calculate_similarity('orig.txt', 'orig.txt')
        self.assertAlmostEqual(similarity, 100.0, places=5)

    def test_calculate_similarity_different(self):
        similarity = calculate_similarity('orig.txt', 'orig_0.8_add.txt')
        self.assertLess(similarity, 100.0)

    def test_calculate_similarity_empty_files(self):
        similarity = calculate_similarity('empty.txt', 'empty.txt')
        self.assertEqual(similarity, 100.0)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_output(self, mock_file):
        similarity = 75.0
        output_file = 'test.txt'
        write_output(output_file, similarity)
        mock_file().write.assert_called_once_with('75.00\n')

    def test_write_output_invalid_path(self):
        with self.assertRaises(OSError):
            write_output('invalid_dir/invalid_file.txt', 75.0)

    def test_calculate_similarity_invalid_value(self):
        with patch('main.cosine_similarity', return_value=np.array([[1.0]])):
            similarity = calculate_similarity('orig.txt', 'orig.txt')
            self.assertEqual(similarity, 100.0)

if __name__ == '__main__':
    unittest.main()