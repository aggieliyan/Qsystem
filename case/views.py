from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def login(request):
	return render_to_response("case/login.html")
