import os
from calendar import weekday
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timez.settings')

import django
django.setup()

from timereg.models import Day, ObLevel, ObTimes, ObSpecials, ShiftDefault
from datetime import time,datetime

def populate():
    mon = add_Day(0, 'Monday')
    tue = add_Day(1, 'Tuesday')
    wed = add_Day(2, 'Wednesday')
    thu = add_Day(3, 'Thursday')
    fri = add_Day(4, 'Friday')
    sat = add_Day(5, 'Saturday')
    sun = add_Day(6, 'Sunday')
    
    dayob = add_ObLevel('Day', 1, 'Regular weekday ob.')
    eveningob = add_ObLevel('Evening', 1.28, 'Regular weekday evening ob.')
    nightob = add_ObLevel('Night', 1.42, 'Regular weekday night ob.')
    weekendob = add_ObLevel('Weekend',1.56 , 'Regular weekend ob.')
    suprweekendob = add_ObLevel('Super Weekend', 2.12, 'Holiday ob.')

    midnight = datetime.strptime("00:00", "%H:%M").time()
    onetomidning = datetime.strptime("23:59:59", "%H:%M:%S").time()
    morning = datetime.strptime("07:00", "%H:%M").time()
    evening = datetime.strptime("18:00", "%H:%M").time()
    
    weekend1 = add_ObTimes('Weekend', midnight, onetomidning, [sat,sun],weekendob)
    weekday_morning = add_ObTimes('Weekday Morning', midnight, morning, [mon,tue,wed,thu,fri], nightob)
    weekday_day = add_ObTimes('Weekday Day', morning, evening, [mon,tue,wed,thu,fri], dayob)
    weekday_evening = add_ObTimes('Weekday Evening', evening, onetomidning, [mon,tue,wed,thu,fri], eveningob)



    evening_start = datetime.strptime("16:45", "%H:%M").time()
    night_start = datetime.strptime("23:30", "%H:%M").time()
    weekend_day_start = datetime.strptime("11:30", "%H:%M").time()
    
    evening_end = datetime.strptime("23:45", "%H:%M").time()
    morning_end = datetime.strptime("08:20", "%H:%M").time()
    weekend_day_end = datetime.strptime("11:45", "%H:%M").time()
     
    add_DefaultShift('Weekday Night', night_start, morning_end, [sun,mon,tue,wed,thu])
    add_DefaultShift('Weekday Evening', evening_start, evening_end, [mon,tue,wed,thu,fri])
    add_DefaultShift('Weekend Day', weekend_day_start, evening_end, [sat,sun])
    add_DefaultShift('Weekend Night', night_start, weekend_day_end, [fri, sat])
     
def add_ObLevel(name,mod,desc):
    obl = ObLevel.objects.get_or_create(name=name,modification=mod,description=desc)[0]
    return obl

def add_ObTimes(name,start,end,days,oblevel):
    obt = ObTimes.objects.get_or_create(name=name,start_time=start,end_time=end,oblevel=oblevel)[0]
    print (days)
    for d in days:
        obt.days.add(d)
    obt.save()
    return obt
    
def add_Day(number,name):
    day = Day.objects.get_or_create(number=number, name=name)[0]
    return day

def add_DefaultShift(name, start, end, days):
    shift = ShiftDefault.objects.get_or_create(name=name,start_time=start, end_time=end)[0]
    for d in days:
        shift.possible_days.add(d)
    shift.save()
    return shift
    
# Start execution here!
if __name__ == '__main__':
    print ("Starting Timez population script...")
    populate()