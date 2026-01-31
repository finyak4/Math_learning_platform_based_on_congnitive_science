from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('<str:subject_slug>/', views.quiz_list, name='quiz_list_subject'),
    path('', views.quiz_list, {'subject_slug': 'calculus'}, name='quiz_list'),
]
