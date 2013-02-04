from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from libreqda.models import Project


@login_required
def browse_projects(request, template='browse_projects.html'):
    user = request.user
    projects = user.projects

    return render(request, template, {'projects': projects})
