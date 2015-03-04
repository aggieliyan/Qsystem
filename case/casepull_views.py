from django.shortcuts import render_to_response, redirect

def case_pull(request):
    return render_to_response("case/case_pull.html")