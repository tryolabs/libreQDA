from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from libreqda.models import Document, Project
from libreqda.validators import DocumentValidator


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'version', 'creation_date', 'modified_date')


class AddUserToProjectForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
                        queryset=User.objects.all(),
                        label=_('Usuarios'))


class NewDocumentForm(forms.Form):
    document = forms.ModelChoiceField(
                        queryset=Document.objects.all(),
                        label="Documento")
    name = forms.CharField(max_length=250, label='Nombre')
    comment = forms.CharField(required=False,
                              widget=forms.Textarea,
                              label='Comentario')


class UploadDocumentForm(forms.Form):
    document = forms.FileField(label="Documento",
                               validators=[DocumentValidator()])
    name = forms.CharField(max_length=250, label='Nombre')
    comment = forms.CharField(required=False,
                              widget=forms.Textarea,
                              label='Comentario')
