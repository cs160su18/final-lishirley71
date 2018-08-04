from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assessment/', views.assessment, name='assessment'),
    path('recommended/', views.recommended, name='recommended'),
    path('episodes/', views.episodes, name='episodes'),
    path('episode/<int:pk>/watch', views.episode_watch, name='episode-watch'),
    path('quiz/', views.quiz, name='quiz'),
    path('episode/<int:pk>/vocab/', views.EpisodeDetailView.as_view(), name='episode-detail'),
    path('lvlup/', views.lvlup, name='lvlup'),
    path('feedback/', views.feedback, name='feedback'),
    

]