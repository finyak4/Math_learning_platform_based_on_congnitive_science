from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from quizzes.models import QuizAttempt

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def profile_view(request):
    attempts = QuizAttempt.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', {'attempts': attempts})
