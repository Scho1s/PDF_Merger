from pypdf import PdfWriter, PdfReader
from enum import Enum
import os


# TODO: Create a checker for duplicate values (both filename and pages)
# TODO: Add input(), asking user what they want to do with the duplicates. (r) Rewrite, (s) Skip
# TODO: Create a fully functional controller with argparse module.
#  It should check first the string for duplicates before processing.


class Enums(Enum):
    INDEX = 0
    PAGE = 1


class ArgParser:
    FILE_FORMAT = ".pdf"

    def __init__(self):
        self.portions = dict()

    def split_arguments(self, args: str):
        portions = list(map(str.strip, args.split(";")))

        for portion in portions:
            filename, pages = portion.split(self.FILE_FORMAT)
            filename += self.FILE_FORMAT
            pages_list = self.extract_pages(pages)
            if self._validate(filename, pages_list):
                self.portions[filename] = pages_list

    def _validate(self, filename: str, pages: list):
        try:
            return all([
                self.file_exists(filename),
                self._check_duplicate(filename),
                self._check_valid_pages(filename, pages),
                self._check_page_extremes(filename, pages),
            ])
        except AttributeError:
            print(f"Validation failed - {filename} does not exist.")
        return False

    def _check_duplicate(self, filename: str) -> bool:
        return filename not in self.portions.keys()

    @staticmethod
    def _check_valid_pages(filename: str, pages: list) -> bool:
        """ Returns True only if all pages are in the dictionary of page numbers found in a file. """
        prs = PdfParser(filename=filename)
        return all([page in prs.page_numbering.keys() for page in pages])

    @staticmethod
    def _check_page_extremes(filename: str, pages: list):
        """ None is treated as "all pages".
        False if page index is outside the limit (negative, zero, or higher than actual page number in a file. """
        if pages:
            prs = PdfParser(filename=filename)
            last_pdf_page = int(prs.page_labels[-1])
            int_pages = list(map(int, pages))
            return all([min(int_pages) > 0, max(int_pages) <= last_pdf_page])

    @staticmethod
    def file_exists(filename: str) -> bool:
        if filename.endswith(".pdf"):
            full_path = os.path.join(os.path.curdir, filename)
            return os.path.exists(full_path)
        else:
            print(f"Not a pdf file - {filename}")
        return False

    def extract_pages(self, page_string: str) -> list:
        """ Parse string with pages into a single list with all pages that must be copied over. """
        pages = list(map(str.strip, page_string.split(",")))
        page_list = []
        for page in pages:
            if "-" in page:
                page_list += self._split_range(page)
            elif page.isnumeric():
                page_list.append(page)
        return page_list

    def _split_range(self, page_range: str) -> list:
        """ Split range. 5-10 becomes [5, 6, 7, 8, 9, 10] """
        if self._verify_range(page_range):
            first, last = list(map(int, page_range.split("-")))
            final_range = list(range(first, last + 1))
            return list(map(str, final_range))
        return []

    @staticmethod
    def _verify_range(page_range: str) -> bool:
        """ Returns True if range is in a valid format (N-M), not N-M-L or alike  """
        page_rng = list(map(str.strip, page_range.split("-")))
        return all([len(page_rng) == 2, *[page.isnumeric() for page in page_rng]])


class PdfParser(PdfReader):
    FORMAT = '.pdf'

    def __init__(self, filename, final_filename="result"):
        if self.file_exists(filename):
            super().__init__(filename)
            self.writer = PdfWriter()
            self.page_numbering = self.create_page_numbering()
            self.final_filename = final_filename + self.FORMAT

    def append_writer(self, file: str, pages=None):
        """ If pages is None, the whole file will be processed. """
        pdf_file = PdfReader(file, strict=False)
        self.writer.append(fileobj=pdf_file, pages=self._get_indices(pages))

    def create_page_numbering(self):
        """ Create a dict with page number/page index pairs """
        pages = {index[Enums.PAGE.value]: int(index[Enums.INDEX.value]) for index in enumerate(self.page_labels)}
        return pages

    @staticmethod
    def _get_indices(pages: list):
        if pages:
            indices = list(map(int, pages))
            return indices
        return None

    def count_pages(self):
        return self.get_num_pages()

    def export(self):
        self.writer.write(self.final_filename)

    @staticmethod
    def file_exists(filename: str) -> bool:
        if filename.endswith(".pdf"):
            full_path = os.path.join(os.path.curdir, filename)
            return os.path.exists(full_path)
        else:
            print(f"Not a pdf file - {filename}")
        return False


if __name__ == "__main__":
    pass
