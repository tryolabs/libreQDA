from django import template

register = template.Library()


@register.filter
def get_permission_text(user_permission):
    map = {'a': 'Administrador',
           'e': 'Editor',
           'g': 'Invitado'}

    return map[user_permission.permissions]
