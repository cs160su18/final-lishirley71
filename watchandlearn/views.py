from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .forms import *
from watchandlearn.models import *


def index(request):
    return render(
        request,
        'watchandlearn/index.html',
        context={},
    ) 

# @login_required