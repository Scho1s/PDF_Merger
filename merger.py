import argparse
from PyPDF2 import PdfWriter, PdfReader


def get_pages(args_):
    final_list = []
    if len(args_) > 1:
        for page in args_[1:]:
            if "-" in page:
                first, second = map(int, page.split("-"))
                for index in range(first, second + 1):
                    final_list.append(index - 1)
            else:
                final_list.append(int(page) - 1)
    else:
        final_list = [page for page in range(len(PdfReader(args_[0]).pages))]
    return final_list


parser = argparse.ArgumentParser(prog='PDF Page Editor', description='PDF files page remover/merger')

parser.add_argument('-f', '--first',
                    dest='first',
                    nargs="+",
                    help="select pages from a first file. If no pages specified, selects all pages")
parser.add_argument('-s',
                    '--second',
                    dest='second',
                    nargs="+",
                    help="select pages from a second file. If no pages specified, selects all pages")

args = parser.parse_args()

try:
    outfile = PdfWriter()

    if args.first:
        outfile.append(fileobj=PdfReader(args.first[0], strict=False), pages=get_pages(args.first))
    if args.second:
        outfile.append(fileobj=PdfReader(args.second[0], strict=False), pages=get_pages(args.second))
    outfile.write('final_file.pdf')
except IndexError:
    print("Page not found. Check the page range.")
except PermissionError:
    print("Final file is open. Please close it and try again.")
except ValueError:
    print("Unable to read one or both pdf files.")
