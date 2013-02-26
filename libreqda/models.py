# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=250, blank=False, verbose_name=_("Nombre"))
    owner = models.ForeignKey(User, related_name='projects')
    version = models.PositiveIntegerField(default=1)
    comment = models.TextField(null=True, blank=True, verbose_name=_("Comentario"))
    modified_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Project %d-%s" % (self.id, self.name)

    def admin_users(self):
        '''
        Return a list of users that have administration
        privileges for the project.
        '''
        admin_perms = self.permissions.filter(permissions='a')
        admins = User.objects.filter(permissions__in=admin_perms)
        return set(list(admins) + [self.owner])


def get_new_document_path(instance, filename):
    return '/'.join(['documents',
                     #instance.project.id,
                     filename])


class Document(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    text = models.TextField(blank=True)
    comment = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=get_new_document_path)
    uploaded_by = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Document: %s" % (self.name)


class DocumentInstance(models.Model):
    document = models.ForeignKey(Document, related_name='instances')
    project = models.ForeignKey(Project, related_name='documents')
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    comment = models.TextField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    annotations = models.ManyToManyField('Annotation', related_name='documents')

    def __unicode__(self):
        return "DocumentInstance: %s" % (self.name)


class Annotation(models.Model):
    project = models.ForeignKey(Project, related_name='annotations')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    text = models.TextField()
    codes = models.ManyToManyField('Code', related_name='annotations')


class Citation(models.Model):
    # TODO: Document instances are no longer needed, should we remove them ?
    document = models.ForeignKey(DocumentInstance, related_name='citations')
    created_by = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    start_paragraph = models.PositiveIntegerField()
    end_paragraph = models.PositiveIntegerField()
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    serialized = models.TextField(null=True, blank=True)


class Code(models.Model):
    CODE_COLORS = (('d', _('Grey')),
                   ('e', _('Red')),
                   ('w', _('Yellow')),
                   ('s', _('Green')),
                   ('i', _('Blue')),
                   ('b', _('Black')),)
    project = models.ForeignKey(Project, related_name='codes')
    name = models.TextField(max_length=250, verbose_name=_('Nombre'))
    weight = models.IntegerField(validators=[MinValueValidator(-100),
                                             MaxValueValidator(100)],
                                 verbose_name=_('Peso'))
    created_by = models.ForeignKey(User)
    color = models.CharField(max_length=1,
                             choices=CODE_COLORS,
                             verbose_name=_('Color'))
    comment = models.TextField(null=True,
                               blank=True,
                               verbose_name=_('Comentario'))
    modified_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    citations = models.ManyToManyField(Citation, related_name='codes')
    parent_code = models.ForeignKey('self', null=True, related_name='sub_codes')


class Category(models.Model):
    name = models.TextField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    comment = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, related_name='categories')
    codes = models.ManyToManyField(Code, related_name='categories')
    citations = models.ManyToManyField(Citation, related_name='categories')
    documents = models.ManyToManyField(Document, related_name='categories')
    annotations = models.ManyToManyField(Annotation, related_name='categories')


class UserProjectPermission(models.Model):
    PROJECT_PERMISSIONS = (('a', _('Administrator')),
                          ('e', _('Editor')),
                          ('g', _('Guest')),)
    user = models.ForeignKey(User, related_name='permissions')
    project = models.ForeignKey(Project, related_name='permissions')
    modified_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    permissions = models.CharField(max_length=1, choices=PROJECT_PERMISSIONS)

    class Meta:
        unique_together = ('user', 'project')

    def is_admin_permission(self):
        return self.permissions == 'a'
