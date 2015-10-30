#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import os
import io
from PyPDF2 import PdfFileReader, PdfFileMerger
import img2pdf
import StringIO
import logging

result_dir = 'pdf'
extensions = ('pdf', 'jpg', 'tiff')
page_separators = ('-', '_')

logger = logging.getLogger('pdfmerger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(message)s')
fh = logging.FileHandler('pdfmerger.log')
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.info("PDFMerger v0.1")

books = {}
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.rpartition('.')[2] in extensions ]

for f in files:
    file_name=f.rpartition('.')[0] 
    if len(file_name) > 0:     
        for sep in page_separators:
            try:
                en = file_name.rpartition(sep)
                en_name = en[0]
                en_page = int(en[2])
                if len(en_name) > 0 and en_page:
                    if not books.has_key(en_name):
                        books[en_name] = {}                    
                    books[en_name][en_page] = f
                    break
            except Exception as e:
                pass

for book_name in books:
    book = books[book_name]
    logger.info("Book name: " + book_name)

    pages = sorted(book, key=lambda key: book[key])
    
    merger = PdfFileMerger()
    
    for page in pages:
        page_filename = book[page]
        page_ext = page_filename.rpartition('.')[2]
        logger.info("+ page: %s", page_filename)
        if page_ext == 'pdf':
           merger.append(PdfFileReader(os.path.join(".", page_filename), "rb"))
        else:
           merger.append(io.BytesIO(img2pdf.convert([os.path.join(".", page_filename)])))

    if not os.path.exists(result_dir):
        logger.info("* Making directory %s", result_dir)
        os.makedirs(result_dir)    

    result_book_name = os.path.join(result_dir, book_name+".pdf")
    logger.info("* Merging to %s", result_book_name)
    merger.write(result_book_name)
    merger.close()
