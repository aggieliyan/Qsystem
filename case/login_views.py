from django.shortcuts import render_to_response, redirect

def login(request):
	return render_to_response("case/login.html")