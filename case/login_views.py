from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.contrib.sessions.models import Session

def logout(request):
	try:
		response = HttpResponseRedirect("/case/login")
		response.delete_cookie("username")
		response.delete_cookie("password")

		session_key = request.session.session_key
		Session.objects.get(session_key=session_key).delete()
		return response
	except:
		pass
	return HttpResponseRedirect("/case/login/")