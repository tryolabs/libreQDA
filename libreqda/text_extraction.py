import slate


def txt(f):
    with open(f, 'r') as f:
        return '\r\n'.join(f.readlines())


def pdf(f):
    with open(f, 'r') as f:
        pdf = slate.PDF(f)
        return '\r\n'.join(pdf)
