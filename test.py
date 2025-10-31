import unittest
import os
from pdf import ArgParser, PdfParser


class TestCaseBase(unittest.TestCase):

    def assertIsFile(self, path):
        if not os.path.exists(os.path.join(os.path.curdir, path)):
            raise AssertionError(f"File does not exist: {path}")


class TestArgParser(unittest.TestCase):

    def test_argument_parser(self):
        args = "file1.pdf 1,2 , 5-10,12; file11.pdf 10-15"
        prs = ArgParser()
        prs.split_arguments(args)
        self.assertDictEqual(prs.portions, {'file1.pdf': ['1', '2', '5', '6', '7', '8', '9', '10', '12']})

    def test_argument_parser_duplicates(self):
        args = "file1.pdf 1,2 , 5-10,12; file1.pdf 10-15"
        prs = ArgParser()
        prs.split_arguments(args)
        self.assertDictEqual(prs.portions, {'file1.pdf': ['1', '2', '5', '6', '7', '8', '9', '10', '12']})

    def test_file_exists(self):
        prs = ArgParser()
        self.assertTrue(prs.file_exists('file1.pdf'))

    def test_wrong_page_range(self):
        args = "file1.pdf 1-b"
        prs = ArgParser()
        prs.split_arguments(args)
        self.assertFalse('file1.pdf' in prs.portions)

    def test_filename_with_spaces(self):
        args = "file parser.pdf 1-10"
        prs = ArgParser()
        prs.split_arguments(args)
        self.assertTrue('file parser.pdf' in prs.portions.keys())

    def test_page_overflow(self):
        args = "file1.pdf 1-1000"
        prs = ArgParser()
        prs.split_arguments(args)
        self.assertTrue('file1.pdf' not in prs.portions.keys())


class TestPdfParser(unittest.TestCase):
    FILE = 'file1.pdf'

    def test_total_pages(self):
        prs = PdfParser(self.FILE)
        self.assertEqual(prs.count_pages(), 314)

    def test_page_numbering(self):
        prs = PdfParser(self.FILE)
        self.assertEqual(prs.page_numbering['xiv'], 15)

    def test_final_name(self):
        prs = PdfParser(self.FILE, final_filename='iamnotfinalname')
        self.assertEqual(prs.final_filename, 'iamnotfinalname.pdf')


class TestFilePath(TestCaseBase):
    FILE = 'file1.pdf'

    def test_export(self):
        file_writer = PdfParser(self.FILE, final_filename='test')
        prs = ArgParser()
        prs.split_arguments(f"{self.FILE} 73 - 75")
        for key, value in prs.portions.items():
            file_writer.append_writer(key, value)
        file_writer.export()
        self.assertIsFile(file_writer.final_filename)
        os.remove(file_writer.final_filename)


if __name__ == "__main__":
    unittest.main()
