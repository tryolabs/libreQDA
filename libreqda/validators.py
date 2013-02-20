from os.path import splitext

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class DocumentValidator():
    SUPPORTED_FILETYPES = ('.doc', '.docx', '.pdf', '.rtf', '.txt')

    def __call__(self, f):
        #TODO: python-magic
        if splitext(f.name)[1].lower() not in self.SUPPORTED_FILETYPES:
            raise ValidationError(_("Tipo de archivo no soportado."))
