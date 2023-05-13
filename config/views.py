from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

def welcome_page(request):
    return render(request, 'first_page.html')