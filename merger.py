import argparse
from pypdf import PdfWriter, PdfReader


def get_pages(args_):
    final_list = {}
    files = " ".join(args_).split(";")
    for file in files:
        pages_list = []
        file_pages = file.strip().split(" ")
        filename = file_pages[0]
        for page in file_pages[1:]:
            if "-" in page:
                first, second = map(int, page.split("-"))
                for index in range(first, second + 1):
                    pages_list.append(index - 1)
            else:
                pages_list.append(int(page) - 1)
        final_list[filename] = pages_list
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
    get_pages(args.pages)
    for filename, pages in get_pages(args.pages).items():
        if len(pages) == 0:
            outfile.append(fileobj=PdfReader(filename, strict=False))
        else:
            outfile.append(fileobj=PdfReader(filename, strict=False), pages=pages)
        outfile.write("final_file.pdf")
except IndexError as e:
    print(f"Page not found. Check the page range.\n{e}")
except PermissionError as e:
    print(f"Final file is open. Please close it and try again.\n{e}")
except ValueError as e:
    print(f"Unable to read one or both pdf files.\n{e}")
