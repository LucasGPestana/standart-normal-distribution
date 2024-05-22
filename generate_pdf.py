import PyPDF2

from typing import Tuple, List
import os
import argparse

def load_base_pdf(filepath: str, num_pages: Tuple | List) -> None:

  pdf_reader = PyPDF2.PdfReader(open(filepath, "rb"))

  # Transforma os números das páginas para a contagem real (ou seja, a partir da capa)
  num_pages = list(map(lambda x: x + 14, num_pages))

  for pos, num_page in enumerate(num_pages):

    create_new_pdf(pdf_reader, num_page, pos+1)


def create_new_pdf(pdf_reader: PyPDF2.PdfReader, num_page: int, part_number: int=1) -> None:

  BASE_DIR = os.path.dirname(os.path.abspath(__file__))

  pdf_writer = PyPDF2.PdfWriter()

  pdf_writer.merge(0, pdf_reader, pages=(num_page, num_page + 1))

  with open(os.path.join(BASE_DIR, "files", f"z-table-part-{part_number}.pdf"), "wb") as file_stream:

    pdf_writer.write(file_stream)

if __name__ == "__main__":

  parser = argparse.ArgumentParser(prog="One Page", description="Programa que pega uma página específica em um arquivo PDF.")

  parser.add_argument("filepath", action="store", type=str, help="Caminho absoluto do PDF no sistema.")
  parser.add_argument("num_pages", action="store", type=int, nargs="+", help="Números das páginas que serão separadas em um arquivo PDF cada.")

  namespace = parser.parse_args()

  load_base_pdf(namespace.filepath, namespace.num_pages)
  