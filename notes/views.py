from django.shortcuts import render

def notes_index(request):
    return render(request, 'notes/index.html')

def calc1_derivatives(request):
    return render(request, 'notes/calculus1/derivatives.html')

def calc1_limits(request):
    return render(request, 'notes/calculus1/limits.html')

def calc1_applications(request):
    return render(request, 'notes/calculus1/applications.html')

def calc2_integrals(request):
    return render(request, 'notes/calculus2/integrals.html')

def calc2_integration_techniques(request):
    return render(request, 'notes/calculus2/integration_techniques.html')

def calc2_sequences_series(request):
    return render(request, 'notes/calculus2/sequences_series.html')
