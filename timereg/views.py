from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from timereg.models import Shift, ShiftFragment
from datetime import time, datetime
from django.template import RequestContext, loader



def index(request):
    return HttpResponse("Hello, world. You're at the index page.")



def entershifts(request):
    return HttpResponse("Hello, here you can enter your shifts")

def showreport(request, user, year, month):
    shift_list = Shift.objects.all().filter(worker__exact=user,start_time__year=year,start_time__month=month) # Only checks start_date.
    
    template = loader.get_template('timereg/showreport.html')
    context = RequestContext(request, {'shift_list' : shift_list})
    return HttpResponse(template.render(context))

