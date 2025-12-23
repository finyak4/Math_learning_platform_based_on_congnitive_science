from django.shortcuts import render

def notes_index(request):
    return render(request, 'notes/base_notes.html')

def calc1_derivatives(request):
    return render(request, 'notes/calculus1/derivatives.html')

def calc1_limits(request):
    return render(request, 'notes/calculus1/limits.html')

def calc1_applications(request):
    return render(request, 'notes/calculus1/applications.html')
