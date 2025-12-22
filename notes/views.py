from django.shortcuts import render

def notes_index(request):
    return render(request, 'notes/base_notes.html')

def calc1_derivatives(request):
    return render(request, 'notes/calculus1/derivatives.html')
