# coding=utf-8

from django.shortcuts import render_to_response, redirect, RequestContext, HttpResponseRedirect
from models import category   

def product_category(request):
    #if not request.user.is_authenticated():
		#return HttpResponseRedirect("/nologin")

    #查询出parent_id = 0 的一级产品模块
    first_secounts = {}
    second_thicounts = {}
    second_ids = {}
    second_names = {}
    third_ids = {}
    third_names = {}
    procate_firsts = category.objects.filter(parent_id = '0', isactived = '1')
    fircount = procate_firsts.count()
    if fircount > 0:
        for procate_first in procate_firsts:
            procate_seconds = category.objects.filter(parent_id = procate_first.id, isactived = '1')
            if procate_seconds.count() > 0:
                first_secounts[procate_first.id] = 1
                for procate_second in procate_seconds:
                    second_ids[procate_second.id] = procate_first.id
                    second_names[procate_second.id] = procate_second.name
                    procate_thirds = category.objects.filter(parent_id = procate_second.id, isactived = '1')
                    if procate_thirds .count() > 0:
                        second_thicounts[procate_second.id] = 1
                        for procate_third in procate_thirds:
                            third_ids[procate_third.id] = procate_second.id
                            third_names[procate_third.id] = procate_third.name 
      
    return render_to_response("case/product_category.html",RequestContext(request, \
    {'procate_firsts':procate_firsts, 'second_ids':second_ids.items(), 'second_names':second_names.items(), \
     'third_ids':third_ids.items(), 'third_names':third_names.items(), 'first_secounts':first_secounts.items(), \
     'second_thicounts':second_thicounts.items()}))
    
def add_firstprocate(request, url):
    if request.method == 'POST':
        None
#        form = add_firstprocateForm(request.POST)
#        if form.is_valid():
#            None           
#    return HttpResponseRedirect(url)

