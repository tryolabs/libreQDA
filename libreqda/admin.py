from django.contrib import admin

from models import Code, Document, Project, DocumentInstance

admin.site.register(Code)
admin.site.register(Project)
admin.site.register(Document)
admin.site.register(DocumentInstance)
