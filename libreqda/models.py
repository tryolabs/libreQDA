from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=250, blank=False, verbose_name="Nombre")
    owner = models.ForeignKey(User, related_name='projects')
    version = models.PositiveIntegerField(default=1)
    comment = models.TextField(null=True, blank=True, verbose_name="Comentario")
    modified_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Project %d-%s" % (self.id, self.name)


def get_new_document_path(instance, filename):
    return '/'.join(['documents',
                     instance.project.id,
                     filename])


class Document(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    comment = models.CharField(blank=True, null=True, max_length=250)
    file = models.FileField(upload_to=get_new_document_path)
    uploaded_by = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Document: %s" % (self.name)


class DocumentInstance(models.Model):
    project = models.ForeignKey(Project, related_name='documents')
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    comment = models.CharField(blank=True, null=True, max_length=250)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User)

    def __unicode__(self):
        return "DocumentInstance: %s" % (self.name)


class Annotation(models.Model):
    project = models.ForeignKey(Project, related_name='annotations')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    text = models.TextField(null=True, blank=True)
    documents = models.ManyToManyField(Document, related_name='annotations')


class Citation(models.Model):
    document = models.ForeignKey(Document, related_name='citations')
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User)


class Code(models.Model):
    project = models.ForeignKey(Project, related_name='codes')
    name = models.TextField(max_length=250)
    weight = models.IntegerField()
    created_by = models.ForeignKey(User)
    color = models.TextField(max_length=6)
    comment = models.TextField(null=True, blank=True)
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


class UserProjectPermissions(models.Model):
    PROJECT_PERMISSIONS = (('a', 'Administrator'),
                          ('e', 'Editor'),
                          ('g', 'Guest'))
    user = models.ForeignKey(User, related_name='permissions')
    project = models.ForeignKey(Project, related_name='permissions')
    modified_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    permissions = models.CharField(max_length=1, choices=PROJECT_PERMISSIONS)

    class Meta:
        unique_together = ('user', 'project')
