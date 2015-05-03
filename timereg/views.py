from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from timereg.models import Shift, ShiftFragment, ObLevel
from datetime import time, datetime,timedelta
from django.template import RequestContext, loader
from django.db.models import Avg, Sum
from collections import OrderedDict



def index(request):
    return HttpResponse("Hello, world. You're at the index page.")



def entershifts(request):
    return HttpResponse("Hello, here you can enter your shifts")

def showreport(request, user, year, month):
    shift_list = Shift.objects.all().filter(worker__exact=user,start_time__year=year,start_time__month=month) # Only checks start_date.
    shiftfragment_list = ShiftFragment.objects.all().filter(worker__exact=user,start_time__year=year,start_time__month=month) # Only checks start_date.
    oblevels = ObLevel.objects.order_by('modification')
    
    ob_sums = OrderedDict.fromkeys(oblevels,(timedelta(0)))
    
    for o in shiftfragment_list:
        curdelta = ob_sums[o.oblevel] 
        ob_sums[o.oblevel] = curdelta + o.length()
    
    
    
    
    template = loader.get_template('timereg/showreport.html')
    context = RequestContext(request, {'shift_list' : shift_list, 'ob_sums' : ob_sums, 'oblevels' : oblevels})
    return HttpResponse(template.render(context))

