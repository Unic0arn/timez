from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import modelformset_factory
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from timereg.forms import ShiftForm
from timereg.models import Shift,ObLevel, ShiftDefault, Day, MonthlyReport
from datetime import datetime,timedelta, date
from django.template import RequestContext, loader
from collections import OrderedDict
from calendar import Calendar
import calendar
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

@login_required
def index(request):
    template = loader.get_template('timereg/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

@login_required
def savereport(request):
    cal = Calendar()
    year = request.POST['year']
    month = request.POST['month']


    monthdate = date(int(year),int(month),1)
    userobj = request.user
    try:
        report = MonthlyReport.objects.get(user=userobj,month=monthdate)
        old_shifts = report.shift_set.all().delete() #Ugly solution will work for now.
        newreport = False
    except ObjectDoesNotExist:
        month_field = datetime.strptime(year +":"+ month, "%Y:%m")
        report = MonthlyReport.objects.get_or_create(month = month_field, user = userobj)[0]
        newreport = True
        report.save()


    monthdays = cal.itermonthdates(int(year), int(month))
    for x in monthdays:
        try:
            start_time = request.POST[str(x.toordinal())+'-start_time']
            end_time = request.POST[str(x.toordinal())+'-end_time']
            try:
                start = datetime.strptime(start_time, "%H:%M").time()
                end = datetime.strptime(end_time, "%H:%M").time()
            except ValueError:
                continue
            new_start_time = datetime.combine(x,start)
            if end_time < start_time: #Overnight

                end_date = x + timedelta(days=1)
                if end_date.month != x.month: #Shift at end of the month. Split shift into two shifts. Causes problem if you want to edit a shift stretching past month.

                    midnight = datetime.strptime('00:00', "%H:%M").time()
                    new_end_time = datetime.combine(end_date, midnight)
                    newshift = Shift(start_date = new_start_time.date(), start_time = new_start_time, end_time = new_end_time,monthly_report = report)
                    newshift.save()

                    new_start_time = new_end_time
                    new_end_time = datetime.combine(end_date, end)
                    next_report = MonthlyReport.objects.get_or_create(month = end_date.replace(day = 1), user = userobj)[0] # Might be unnesecary to replace the day to one, but i'm considering really long shifts...
                    newshift2 = Shift(start_date = new_start_time.date(), start_time = new_start_time, end_time = new_end_time, monthly_report = next_report)
                    newshift2.save()
                    continue

                new_end_time = datetime.combine(end_date, end)
            else:
                new_end_time = datetime.combine(x, end)
                
            newshift = Shift(start_date = new_start_time.date(), start_time = new_start_time, end_time = new_end_time,monthly_report = report)
            newshift.save()
        except KeyError:
            pass
    
    
    
    return HttpResponseRedirect(reverse('timereg:showreport', args=(year, month)))

@login_required
def entershifts(request):
    if request.method == 'POST':
        print(request.POST)
    try:
        month = int(request.POST['month'])
        year = int(request.POST['year'])
    except KeyError as e:
        newdate = date.today()
        year = newdate.year
        month = newdate.month

    template = loader.get_template('timereg/entershifts.html')
    context = RequestContext(request, {'month':month,'year':year})
    return HttpResponse(template.render(context))

@login_required
def getmonthentry(request):
    if request.method == 'POST':
        print(request.POST)
    try:
        month = int(request.GET['month'])
        year = int(request.GET['year'])
    except KeyError:
        newdate = date.today()
        year = newdate.year
        month = newdate.month
    
    defaultshift_list = ShiftDefault.objects.all()
    cal = Calendar()
    weekdays = cal.itermonthdays2(year, month)
    monthname = calendar.month_name[month]

    monthdate = date(year,month,1)
    userobj = request.user
    try:
        prevreport = MonthlyReport.objects.get(user=userobj,month=monthdate)
        shifts = prevreport.shift_set
        newreport = False
    except ObjectDoesNotExist:
        shifts = Shift.objects.none()
        newreport = True


    monthdays = []
    for w in weekdays:
        if w[0] != 0:
            monthdays.append((datetime(year,month,w[0]), Day.objects.get(number = w[1])))

    context = RequestContext(request, {'year':  year, 'month' : month, 'monthname' : monthname, 'monthdays' : monthdays, 'defaultshift_list' : defaultshift_list, 'newreport' : newreport, 'shifts' : shifts})

    template = loader.get_template('timereg/entershiftform.html')
    return HttpResponse(template.render(context))
    

@login_required
def showreport(request, year, month):
    userobj = request.user
    month_field = datetime.strptime(year +":"+ month, "%Y:%m")
    monthly_report = MonthlyReport.objects.get(month = month_field, user = userobj)
    
    shift_list = monthly_report.shift_set.all()
    shiftfragment_list = []
    for shift in shift_list:
        for fragment in shift.shiftfragment_set.all():
            shiftfragment_list.append(fragment)
    oblevels = ObLevel.objects.order_by('modification')
    ob_sums = OrderedDict.fromkeys(oblevels,(timedelta(0)))
    total_time = timedelta(0)
    for o in shiftfragment_list:
        curdelta = ob_sums[o.oblevel] 
        ob_sums[o.oblevel] = curdelta + o.length
        total_time += o.length
    
    moneyz = {}
    total_moneyz = 0
    for k, v in ob_sums.items():
        tmp_money = v.total_seconds() * float(k.modification) * 120/3600
        ob_sums[k] = (hours_minutes_seconds(v),tmp_money)
        total_moneyz += tmp_money
    
    
    new_shift_list = [(shift, shift.getObTimes()) for shift in shift_list]
    print (new_shift_list)
    total_total_moneyz = total_moneyz * 1.12
    template = loader.get_template('timereg/showreport.html')
    context = RequestContext(request, {'shift_list' : new_shift_list, 
                                       'ob_sums' : ob_sums, 
                                       'oblevels' : oblevels,
                                       'total_moneyz' : total_moneyz,
                                       'total_total_moneyz' : total_total_moneyz, 
                                       'user' : userobj, 
                                       'total_time':hours_minutes_seconds(total_time)})
    return HttpResponse(template.render(context))

@login_required
def list_reports(request):
    
    userobj = request.user
    reports = userobj.monthlyreport_set.all()
    template = loader.get_template('timereg/listreports.html')
    context = RequestContext(request, {'reports' : reports})
    return HttpResponse(template.render(context))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/timereg/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'auth/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/timereg/')

def hours_minutes_seconds(td):
    seconds = td.total_seconds()
    return (int(seconds//(60*60)), int((seconds%3600)/60), int(seconds%60)) 