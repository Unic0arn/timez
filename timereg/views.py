from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from timereg.models import Shift, ShiftFragment, ObLevel, ShiftDefault, Day
from datetime import time, datetime,timedelta, date
from django.template import RequestContext, loader
from django.db.models import Avg, Sum
from collections import OrderedDict
from django.contrib.auth.models import User
from calendar import monthrange,Calendar
from django.core.urlresolvers import reverse
from timereg.forms import MonthSelectorForm
def index(request):
    
    return HttpResponse("Hello, world. You're at the index page.")


def addreport(request):
    
    defaultshift_list = ShiftDefault.objects.all()
    cal = Calendar()
    year = int(request.POST['year'])
    month = int(request.POST['month'])
    monthdays = cal.itermonthdates(year, month)
    shifts = []
    
    userobj = User.objects.all().get(pk=request.POST['user'])
    for x in monthdays:
        try:
            start_time = request.POST[str(x.toordinal())+'-start_time']
            end_time = request.POST[str(x.toordinal())+'-end_time']
            if start_time is '' or end_time is '':
                continue 
            
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
            
            new_start_time = datetime.combine(x,start)
            if end_time < start_time: #Overnight
                new_end_time = datetime.combine(x + timedelta(days=1), end)
            else:
                new_end_time = datetime.combine(x, end)
                
            newshift = Shift(start_time = new_start_time, end_time = new_end_time, worker = userobj)
            newshift.save()
        except KeyError:
            pass
    
    return HttpResponseRedirect(reverse('timereg:showreport', args=(userobj.pk,year,month)))

def entershifts(request):
    if request.method == 'POST':
        print(request.POST)
    try:
        newdate = datetime.strptime(request.POST['month'],"%Y-%m-%d")
        year = newdate.year
        month = newdate.month
    except KeyError:
        today = date.today()
        year = today.year
        month = today.month
            
    defaultshift_list = ShiftDefault.objects.all()
    cal = Calendar()
    monthdays = cal.itermonthdates(year, month)
    weekdays = cal.itermonthdays2(year, month)
    
    monthform = MonthSelectorForm()
    
    monthdays3 = []
    for w in weekdays:
        if w[0] != 0:
            monthdays3.append((datetime(year,month,w[0]), Day.objects.get(number = w[1])))

    template = loader.get_template('timereg/entershifts.html')
    context = RequestContext(request, {'monthform' : monthform, 'year':  year, 'month' : month, 'monthdays' : monthdays3, 'defaultshift_list' : defaultshift_list})
    return HttpResponse(template.render(context))



def showreport(request, user, year, month):
    shift_list = Shift.objects.all().filter(worker__exact=user,start_time__year=year,start_time__month=month) # Only checks start_date.
    shiftfragment_list = ShiftFragment.objects.all().filter(worker__exact=user,start_time__year=year,start_time__month=month) # Only checks start_date.
    oblevels = ObLevel.objects.order_by('modification')
    userobj = User.objects.all().get(pk=user)
    ob_sums = OrderedDict.fromkeys(oblevels,(timedelta(0)))
    total_time = timedelta(0)
    for o in shiftfragment_list:
        curdelta = ob_sums[o.oblevel] 
        ob_sums[o.oblevel] = curdelta + o.length
        total_time += o.length
    
    
    for k, v in ob_sums.items():
        ob_sums[k] = hours_minutes_seconds(v)
    
    template = loader.get_template('timereg/showreport.html')
    context = RequestContext(request, {'shift_list' : shift_list, 
                                       'ob_sums' : ob_sums, 
                                       'oblevels' : oblevels, 
                                       'user' : userobj, 
                                       'total_time':hours_minutes_seconds(total_time)})
    return HttpResponse(template.render(context))


    
def hours_minutes_seconds(td):
    seconds = td.total_seconds()
    return (int(seconds//(60*60)), int((seconds%3600)/60), int(seconds%60)) 