from django.shortcuts import render_to_response, redirect

def product_category(request):
	return render_to_response("case/product_category.html")