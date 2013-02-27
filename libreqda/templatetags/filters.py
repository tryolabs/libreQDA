from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter
def get_permission_text(user_permission):
    key_map = {'a': _('Administrador'),
           'e': _('Editor'),
           'g': _('Invitado')}

    return key_map[user_permission.permissions]


@register.filter
def pretty_print_code_name(code):
    class_map = {'i': 'badge-info',
                 's': 'badge-success',
                 'w': 'badge-warning',
                 'e': 'badge-important',
                 'b': 'badge-inverse',
                 'd': ''}

    if code.color:
        return '<span class="badge %s">%s</span>' % (class_map[code.color],
                                                     code.name)
    else:
        return code.name
