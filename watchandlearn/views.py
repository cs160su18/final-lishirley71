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
def assessment(request):
    return render(
        request,
        'watchandlearn/assessment-final.html',
        context={},
    ) 

# @login_required
def recommended(request):
	return render(
				request,
				'watchandlearn/recommended.html',
				context={},
			)

# @login_required
def episodes(request):
	return render(
				request,
				'watchandlearn/episodes.html',
				context={},
			)

# @login_required
def quiz(request):
	return render(
				request,
				'watchandlearn/quiz.html',
				context={},
			)

# @login_required
def vocab(request):
	return render(
				request,
				'watchandlearn/vocab.html',
				context={},
			)

# @login_required
def lvlup(request):
	return render(
				request,
				'watchandlearn/lvlup.html',
				context={},
			)

# @login_required
def feedback(request):
	return render(
				request,
				'watchandlearn/feedback.html',
				context={},
			)