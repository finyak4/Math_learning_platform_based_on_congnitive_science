from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_index, name='notes_index'),
    path('calculus-1/derivatives/', views.calc1_derivatives, name='notes_calc1_derivatives'),
    path('calculus-1/limits/', views.calc1_limits, name='notes_calc1_limits'),
    path('calculus-1/applications/', views.calc1_applications, name='notes_calc1_applications'),
]
