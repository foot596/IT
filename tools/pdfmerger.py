#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import os
import io
from PyPDF2 import PdfFileReader, PdfFileMerger
import img2pdf
import StringIO
import logging
import re

result_dir = 'pdf'
extensions = ('pdf', 'jpg', 'tiff')
page_separators = ('-')

logger = logging.getLogger('pdfmerger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
fh = logging.FileHandler('pdfmerger.log')
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.info("PDFMerger v0.1")

books = {}
current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.rpartition('.')[2] in extensions ]

for f in files:
    file_name=f.rpartition('.')[0] 
    if len(file_name) > 0:     
        for sep in page_separators:
            try:
                logger.debug("Filename: %s", file_name)  
                m1 = re.match(r"^(.*)-(\d+.*)$", file_name)
                m2 = re.match(r"^(\d+.*)$", file_name)         
                if m1:
                    logger.debug("m1.groups(): %s", m1.groups())
                    en_name = m1.group(1).replace (" ", "_")
                    en_page = m1.group(2).replace (" ", "_")
                elif m2:
                    logger.debug("m1.groups(): %s", m2.groups())
                    en_name = current_dir.replace (" ", "_")
                    en_page = m2.group(1).replace (" ", "_")
                else:
                    raise ValueError("Can't parse filename: %s", file_name) 

                if not books.has_key(en_name):
                    books[en_name] = {}                    
                books[en_name][en_page] = f
                break
       
            except ValueError as e:
                logger.error("%s: %s", type(e).__name__, e.args)
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
