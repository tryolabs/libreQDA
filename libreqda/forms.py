from django import forms
from django.contrib.auth.models import User

from libreqda.models import Document, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'version', 'creation_date', 'modified_date')


class AddUserToProjectForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
                        queryset=User.objects.all(),
                        label='Usuarios')


class NewDocumentForm(forms.Form):
    document = forms.ModelChoiceField(
                        queryset=Document.objects.all(),
                        label="Documento")
    name = forms.CharField(max_length=250, label='Nombre')
    comment = forms.CharField(required=False,
                              widget=forms.Textarea,
                              label='Comentario')


class UploadDocumentForm(forms.Form):
    document = forms.FileField(label="Documento")
    name = forms.CharField(max_length=250, label='Nombre')
    comment = forms.CharField(required=False,
                              widget=forms.Textarea,
                              label='Comentario')
