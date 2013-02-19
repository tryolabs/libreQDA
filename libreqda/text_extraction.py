def txt(f):
    with open(f, 'r') as f:
        return '\r\n'.join(f.readlines())
