# -*- coding: utf-8 -*-
import cStringIO
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from docx import opendocx, getdocumenttext
from pyth.plugins.rtf15.reader import Rtf15Reader


def txt(f):
    with open(f, 'r') as f:
        return '\r\n'.join(f.readlines())


def pdf(f):
    rsrcmgr = PDFResourceManager()
    retstr = cStringIO.StringIO()
    codec = 'utf-8'

    laparams = LAParams()
    laparams.all_texts = True

    device = TextConverter(
        rsrcmgr, retstr, codec=codec, laparams=laparams
    )

    fp = file(f, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()

    str = retstr.getvalue()
    retstr.close()
    return str


def docx(f):
    doc = opendocx(f)
    return '\r\n'.join(getdocumenttext(doc))


def rtf(f):
    with open(f, "rb") as f:
        doc = Rtf15Reader.read(f)
    result = []
    for element in doc.content:
        for text in element.content:
            result.append(''.join(text.content))
    return '\r\n'.join(result)

