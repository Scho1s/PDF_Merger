import argparse
from argparse import RawDescriptionHelpFormatter
from pypdf import PdfWriter, PdfReader


FINAL_FILE_NAME = "final_file.pdf"
PROGRAM_NAME = 'PDF Page Editor'
DESCRIPTION = """
PDF files page remover/merger.
The program can accept list of files, which should be separated by semicolon (;).
Pages can also be listed in two different ways - one by one or as a range.

Examples:

merger -m file1.pdf 2-6                     - Get pages 2 to 6 from file1.
merger -m file2.pdf 2 6 10; file3.pdf 8     - Get pages 2, 6 and 10 from fil2 and page 8 from file3.
merger -m file1; file2 3-10                 - Get all pages from file1 and pages 3 to 10 from file2.
"""


def get_pages(args_):
    final_list = {}
    for file in " ".join(args_).split(";"):
        pages_to_add = []
        file_pages = file.strip().split(" ")
        filename_ = file_pages.pop(0)
        num_of_pages = len(file_pages)

        match num_of_pages:
            case num_of_pages if num_of_pages > 1:
                for page in file_pages:
                    if "-" in page:
                        pages_to_add.append([*range(*map(int, page.split("-")))])
                    else:
                        pages_to_add.append(int(page) - 1)
            case 1:
                pages_to_add.append(int(file_pages[0]) - 1)
        final_list[filename_] = pages_to_add
    return final_list


parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=DESCRIPTION, formatter_class=RawDescriptionHelpFormatter)

parser.add_argument('-m', '--merge',
                    help='select pages from a first file. If no pages specified, selects all pages',
                    action='store_true')

parser.add_argument('pages',
                    nargs='+',
                    help='select pages from a first file. If no pages specified, selects all pages')

args = parser.parse_args()

try:
    outfile = PdfWriter()
    if args.merge:
        for filename, pages in get_pages(args.pages).items():
            print(filename, pages)
            if len(pages) == 0:
                outfile.append(fileobj=PdfReader(filename, strict=False))
            else:
                outfile.append(fileobj=PdfReader(filename, strict=False), pages=pages)
            outfile.write(FINAL_FILE_NAME)
    else:
        print("No argument supplied (-m). Nothing has been processed.")
except IndexError as e:
    print(f"Page not found. Check the page range.\n{e}")
except PermissionError as e:
    print(f"Final file is open. Close it and try again.\n{e}")
except ValueError as e:
    print(f"Unable to read one or more pdf files.\n{e}")
