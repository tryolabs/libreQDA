# -*- coding: utf-8 -*-
import pdfminer
import cStringIO

from docx import opendocx, getdocumenttext
from pyth.plugins.rtf15.reader import Rtf15Reader


def txt(f):
    with open(f, 'r') as f:
        return '\r\n'.join(f.readlines())


def pdf(f):
    rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
    retstr = cStringIO.StringIO()
    codec = 'utf-8'
    laparams = pdfminer.layout.LAParams()
    device = pdfminer.converter.TextConverter(
        rsrcmgr, retstr, codec=codec, laparams=laparams
    )

    fp = file(f, 'rb')
    pdfminer.pdfinterp.process_pdf(rsrcmgr, device, fp)
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

