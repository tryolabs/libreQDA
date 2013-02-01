from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User)
    version = models.PositiveIntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)


def get_new_document_path(instance, filename):
    return '/'.join(['documents',
                     instance.project.id,
                     filename])


class Document(models.Model):
    project = models.ForeignKey(Project, related_name='projects')
    name = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User)
    file = models.FileField(upload_to=get_new_document_path)


class Annotation(models.Model):
    document = models.ForeignKey(Document, related_name='annotations')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    text = models.TextField(null=True, blank=True)


class Citation(models.Model):
    document = models.ForeignKey(Document, related_name='citations')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    comment = models.TextField(null=True, blank=True)


class Code(models.Model):
    project = models.ForeignKey(Project, related_name='codes')
    weight = models.IntegerField()
    created_by = models.ForeignKey(User)
    comment = models.TextField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    citations = models.ManyToManyField(Citation, related_name='codes')


class Category(models.Model):
    name = models.TextField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, related_name='categories')
    codes = models.ManyToManyField(Code, related_name='categories')
    citations = models.ManyToManyField(Citation, related_name='categories')
    documents = models.ManyToManyField(Document, related_name='categories')
    annotations = models.ManyToManyField(Annotation, related_name='categories')


class UserProyectPermissions(models.Model):
    PROJECT_PERMISSIONS = (('a', 'Administrator'),
                          ('e', 'Editor'),
                          ('g', 'Guest'))
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    permissions = models.CharField(max_length=1, choices=PROJECT_PERMISSIONS)

    class Meta:
        unique_together = ('user', 'project')
