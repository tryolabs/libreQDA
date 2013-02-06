from django import forms

from libreqda.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'version', 'creation_date', 'modified_date')


class CopyProjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CopyProjectForm, self).__init__(*args, **kwargs)
        self.fields['new_name'].label = "Nuevo nombre"

    new_name = forms.CharField(max_length=250)
