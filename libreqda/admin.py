# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Code, Document, Project, DocumentInstance, Citation

admin.site.register(Code)
admin.site.register(Project)
admin.site.register(Citation)
admin.site.register(Document)
admin.site.register(DocumentInstance)
