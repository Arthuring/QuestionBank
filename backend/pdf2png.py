# -- coding: utf-8 --
import pdf2image
import os


def pdf2jpg(pdf_path, output_dir):
    pdf2image.convert_from_path(pdf_path, first_page=0, output_folder=output_dir,fmt="png")


pdf2jpg(os.path.join('test_pdf','test.pdf'), 'test_pdf')
