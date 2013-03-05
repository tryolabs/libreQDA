# -*- coding: utf-8 -*-
import slate

from docx import opendocx, getdocumenttext
from pyth.plugins.rtf15.reader import Rtf15Reader


def txt(f):
    with open(f, 'r') as f:
        return '\r\n'.join(f.readlines())


def pdf(f):
    with open(f, 'r') as f:
        pdf = slate.PDF(f)
        return '\r\n'.join(pdf)


def docx(f):
    doc = opendocx(f)
    return '\r\n'.join(getdocumenttext(doc))


def rtf(f):
    doc = Rtf15Reader.read(open(f, "rb"))
    result = []
    for element in doc.content:
        for text in element.content:
            result.append(''.join(text.content))
    return ''.join(result)
