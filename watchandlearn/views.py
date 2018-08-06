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
from my_secrets import secrets
import re, requests, json, urllib
from django.template import *

HIGHEST_SCORE = 6

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
        'watchandlearn/assessment.html',
        context={},
    ) 

# @login_required
def recommended(request):
    series = Series.objects.all()
    topics = Topic.objects.all()
    return render(
        request, 
        "watchandlearn/recommended.html", 
        context={'series':series, 'topics': topics}
    )

# @login_required
def episodes(request, pk):
  series = get_object_or_404(Series, pk=pk)
  episodes = Episode.objects.all().filter(series__pk=pk)
  return render(request, 'watchandlearn/episodes.html', context={'series': series, "episodes": episodes},)

# @login_required
def quiz(request, pk):
  quiz = get_object_or_404(Quiz, pk=pk)
  questions = Question.objects.all().filter(quiz__pk=pk)
  return render( request, 'watchandlearn/quiz.html', context={'quiz': quiz, 'questions': questions},)

def episode_watch(request, pk):

    episode = get_object_or_404(Episode, pk=pk)
    
    return render(request, 'watchandlearn/episode_watch.html', context={'episode': episode})


# @login_required
class EpisodeDetailView(generic.DetailView):
  model = Episode

  # HELPER METHODS

  # inclusive range function
  def irange(self, x, y):
    return range(x, y+1)

  # turns the content of an srt file into a list of unique words
  def strip_captions(self, caption):
    # remove non-word characters (except for ' )
    caption = re.sub('[\d:,->!"?^]', ' ', caption)

    # remove new lines
    caption = caption.replace('\n', ' ')

    # remove tabs
    caption = caption.replace('\t', ' ')

    caption = caption.replace('\r', ' ')

    # remove extra spaces
    caption = re.sub(' +',' ', caption)

    # to lower case
    caption = caption.lower()

    # split into a set of unique words, delimited by spaces
    return set(caption.split(" "))
  
  # find timestamp where search_term was said
  def find_timestamp(self, arr, search_term):
    line = 1
    captions = {}
    chunk = []
    timestamp = ''
    i = 0

    while i < len(arr):
      item = arr[i]
      # if it gets to the next line
      if item == str(line):
        i+=1
        timestamp = arr[i]
      elif item == '':
        word = " ". join(chunk)
        captions[timestamp] = word
        chunk = []
        timestamp = ''
        line += 1
      else:
        chunk.append(item)
      i += 1
    word = " ". join(chunk)
    captions[timestamp] = word

    # reverse dict
    captions = {y:x for x,y in captions.items()}

    for line, timestamp in captions.items():
      if search_term in line:
        return timestamp
    return 'Not Found'

  # use WordAPI to find definitions for search_term
  def find_definition(self, search_term):
    app_id = secrets.OXFORD_ID
    app_key = secrets.OXFORD_KEY

    language = 'en'
    search_term = search_term.replace(" ", "_")
    word_id = urllib.parse.quote_plus(search_term)

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key}).json()
    defn = r['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    return defn

  def get_context_data(self, **kwargs):
    
    # context is a dict of info available in the view
    context = super(EpisodeDetailView, self).get_context_data(**kwargs)
    
    # list of vocab to eventually put into the context dict
    vocab_list = []
    
    # selected episode 
    episode = context['episode']
    
    # compare words to user's vocab score
    u = self.request.user.profile
    vocab = u.vocabulary
    
    # create list of unique words
    script_list = self.strip_captions(episode.subtitle)
    for diff_lvl in reversed(self.irange(vocab, HIGHEST_SCORE)):
      if len(vocab_list) >= 5:
        break
      word_list = Word.objects.filter(difficulty__gte=diff_lvl)
      for word_obj in word_list:
        # word_list is a list of word objects, but we just want the word itself
        word = word_obj.name
        if(len(word) < 5):
          continue
        if word in script_list:
          vocab_list.append(word)
          if len(vocab_list) >= 5:
            break

    terms = []
    arr = episode.subtitle.splitlines()
    for search_term in vocab_list:
      timestamp = self.find_timestamp(arr, search_term)
      definition = self.find_definition(search_term)
      terms.append({'timestamp': timestamp, 'word': search_term.capitalize(), 'definition': definition})
    context['terms'] = terms
    return context
    
# @login_required
def lvlup(request):
    profile = request.user.profile
    return render(
        request,
        'watchandlearn/lvlup.html',
        context={'profile': profile},
      )

# @login_required
def feedback(request, pk):
  if request.method == 'POST':
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = list(Question.objects.all().filter(quiz__pk=pk))
    answers = []
    i=1
    for i in range(len(questions)):
      submitted_answer = request.POST.get('question' + str(i))
      question = questions[i]
      answers.append(str(question.answer) == submitted_answer)
    print(answers)
  return render(request, 'watchandlearn/feedback.html', context={'questions': questions, 'answers': answers},)


