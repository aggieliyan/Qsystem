'''
Created on 2015-2-3

@author: liyan
'''
import models
import datetime
from django.http import HttpResponse

def my_scheduled_job(request):
    chart_pro = models.project_statistics.objects.filter(is_graph=1)
    results = []
    for item in chart_pro:
        try:
            int(item.total)
            results.append(models.project_statistics_result(project_id=item.project_id, sql_id=item.id,
                                                        date=datetime.datetime.now(), 
                                                        statistical_result=item.total, isactived=1))
            print item.is_editable
            if item.is_editable == 1:
                item.is_editable = 0
                item.save()
                print item.is_editable
        except:
            ps = models.project_statistics.objects.get(id=item.id)
            ps.is_graph = 0
            ps.save()
    models.project_statistics_result.objects.bulk_create(results)
    return HttpResponse("123")
