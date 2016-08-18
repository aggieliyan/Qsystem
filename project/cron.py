'''
Created on 2015-2-3

@author: liyan
'''   
import models
import datetime
#from django.http import HttpResponse
from django.db import connections

def my_scheduled_job():
    allsql = models.project_statistics.objects.all()
    for c in allsql: 
        sql = c.sql
        db = c.db
        try:
            cursor = connections[db].cursor()
            cursor.execute(sql)
            total = cursor.fetchall()
            total_list = ''       
            for a in total:         #for style, more lines need '\r'
                    if len(total) == 1:         
                        total_list = str(a[0])
                    else:
                        total_list = total_list + str(a[0]) + '\r'
                  
            c.total = total_list
            c.save()
            cursor.close()
            
        except Exception, e:
            print e
            pass
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
#    return HttpResponse("123")
