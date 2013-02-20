import slate

from docx import opendocx, getdocumenttext


def txt(f):
    with open(f, 'r') as f:
        return '\r\n'.join(f.readlines())


def pdf(f):
    with open(f, 'r') as f:
        pdf = slate.PDF(f)
        return '\r\n'.join(pdf)


def docx(f):
    try:
        doc = opendocx(f)
        return '\r\n'.join(getdocumenttext(doc))
    except Exception as e:
        print e
