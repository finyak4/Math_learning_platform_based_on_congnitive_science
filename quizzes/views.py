from django.shortcuts import render
from .models import Quiz

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})
