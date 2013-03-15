# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from libreqda.models import Annotation, BooleanQuery, Category, Code, \
    Document, Project, SemanticQuery, SetQuery, ProximityQuery
from libreqda.validators import DocumentValidator


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'version', 'creation_date', 'modified_date')


class AddUserToProjectForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
                        queryset=User.objects.all(),
                        label=_('Usuarios'))


class AddCodeToCitationForm(forms.Form):
    codes = forms.ModelMultipleChoiceField(
                        queryset=Code.objects.all(),
                        label=_('Códigos'))


class AddAnnotationToCitationForm(forms.Form):
    annotations = forms.ModelMultipleChoiceField(
                        queryset=Annotation.objects.all(),
                        label=_('Anotaciones'))


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


class CodeForm(forms.ModelForm):
    class Meta:
        WEIGHTS = [(i, i) for i in range(-100, 101)][::-1]

        model = Code
        exclude = ('citations', 'created_by', 'creation_date',
                   'modified_date', 'project')
        widgets = {'name': forms.TextInput(),
                   'weight': forms.Select(choices=WEIGHTS)}


class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        exclude = ('codes', 'created_by', 'creation_date',
                   'modified_date', 'project')


class AddCodeToAnnotation(forms.Form):
    codes = forms.ModelMultipleChoiceField(queryset=Code.objects.none(),
                                           label=_('Códigos'))


class BooleanQueryForm(forms.ModelForm):
    class Meta:
        model = BooleanQuery
        exclude = ('project')


class SetQueryForm(forms.ModelForm):
    class Meta:
        model = SetQuery
        exclude = ('project')

    def clean(self):
        cleaned_data = super(SetQueryForm, self).clean()

        if not (cleaned_data['boolean_queries'] or
                cleaned_data['proximity_queries'] or
                cleaned_data['semantic_queries']):
            raise forms.ValidationError(
                            _('* Se debe seleccionar al menos una consulta.'))

        return cleaned_data


class SemanticQueryForm(forms.ModelForm):
    class Meta:
        model = SemanticQuery
        exclude = ('project')


class ProximityQueryForm(forms.ModelForm):
    class Meta:
        model = ProximityQuery
        exclude = ('project')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('annotations', 'citations', 'codes', 'documents',
                   'created_by', 'creation_date', 'modified_date', 'project')
        widgets = {'name': forms.TextInput()}
