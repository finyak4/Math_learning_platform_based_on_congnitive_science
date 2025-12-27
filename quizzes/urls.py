from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
]
