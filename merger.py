import argparse
from pypdf import PdfWriter, PdfReader


FINAL_FILE_NAME = "final_file.pdf"


def get_pages(args_):
    final_list = {}
    for file in " ".join(args_).split(";"):
        pages_to_add = []
        file_pages = file.strip().split(" ")
        filename_ = file_pages.pop(0)
        if len(file_pages) > 1:
            for page in file_pages:
                if "-" in page:
                    pages_to_add.append([*range(*map(int, page.split("-")))])
                else:
                    pages_to_add.append(int(page) - 1)
        else:
            pages_to_add.append(int(file_pages[0]) - 1)
        final_list[filename_] = pages_to_add
    return final_list


parser = argparse.ArgumentParser(prog='PDF Page Editor', description='PDF files page remover/merger')

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
