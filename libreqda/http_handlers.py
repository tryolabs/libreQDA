# -*- coding: utf-8 -*-
from django.shortcuts import render


def handle_404(request, template='404.html'):
        return render(request, template, {})
