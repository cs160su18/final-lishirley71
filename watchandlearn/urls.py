from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assessment/', views.assessment, name='assessment'),
    path('recommended/', views.recommended, name='recommended'),
    path('episodes/', views.episodes, name='episodes'),
    path('quiz/', views.quiz, name='quiz'),
    path('vocab/', views.vocab, name='vocab'),
    path('lvlup/', views.lvlup, name='lvlup'),
    path('feedback/', views.feedback, name='feedback'),
    

]