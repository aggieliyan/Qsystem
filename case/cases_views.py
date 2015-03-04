from django.shortcuts import render_to_response, redirect

def case_list(request):
	return render_to_response("case/case_list.html")