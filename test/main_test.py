import unittest
import src.main

class MyTestCase(unittest.TestCase):
    def test_file_fmt_1(self):
        self.assertEqual(src.main.file_fmt(''), 'none')

    def test_file_fmt_2(self):
        self.assertEqual(src.main.file_fmt('hfdk'), 'none')

    def test_file_fmt_3(self):
        self.assertEqual(src.main.file_fmt('fdks.fdhsj'), 'none')

    def test_file_fmt_4(self):
        self.assertEqual(src.main.file_fmt('fdks.docx'), 'doc')

    def test_file_fmt_5(self):
        self.assertEqual(src.main.file_fmt('fd.f,sdf.ds..pdf'), 'pdf')

    def test_file_fmt_6(self):
        self.assertEqual(src.main.file_fmt('fd.f,sdf.ds..doc'), 'doc')

    def test_file_fmt_7(self):
        self.assertEqual(src.main.file_fmt('fd.f,sdf.ds..'), 'none')

if __name__ == '__main__':
    unittest.main()
