from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter
def get_permission_text(user_permission):
    key_map = {'a': _('Administrador'),
           'e': _('Editor'),
           'g': _('Invitado')}

    return key_map[user_permission.permissions]
