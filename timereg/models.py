from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta,time,date
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from calendar import weekday
# Create your models here.

class ObLevel(models.Model):
    name = models.CharField(max_length=255)
    modification = models.DecimalField(max_digits=3,decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class ObTimes(models.Model):    
    name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField()
    oblevel = models.ForeignKey(ObLevel)
    
    def __str__(self):
        return self.name

class ObSpecials(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    oblevel = models.ForeignKey(ObLevel)
    
    def __str__(self):
        return self.name
  
  

class MonthlyReport(models.Model):
    month = models.DateField()
    user = models.ForeignKey(User)
    
    def __str__(self):
        return str(self.month)
    
    class Meta:
        unique_together = ("month","user")

    
class Shift(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    length = models.DurationField(blank=True, editable = False  )
    monthly_report = models.ForeignKey(MonthlyReport,default=1)
    
    def __str__(self):
        return  str(self.monthly_report.user) + ' - ' + str(self.start_time) + ' - ' + str(self.end_time)
      
    def save(self,* args, **kwargs):
        self.length = self.end_time - self.start_time
        super(Shift, self).save(*args, **kwargs)
        splitShift(self)
      
    
class ShiftFragment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    oblevel = models.ForeignKey(ObLevel)
    main_shift = models.ForeignKey(Shift)
    length = models.DurationField(blank = True, editable = False )
    
    def __str__(self):
        return str(self.main_shift.monthly_report.user) + ': ' + str(self.start_time) + ' - ' + str(self.end_time)
    
    def save(self,* args, **kwargs):
        self.length = self.end_time - self.start_time
        super(ShiftFragment, self).save()
    
    
class Day(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=10)    
    
    def __str__(self):
        return self.name
    
    # Needs to be renamed -.-'
class ShiftDefault(models.Model): # TODO Needs system to determine what kind of shift is possible.
    name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time   = models.TimeField()
    length = models.DurationField(blank = True, editable = False)
    possible_days = models.ManyToManyField(Day)
    def __str__(self):
        return self.name+ ': ' + str(self.start_time) + ' - ' + str(self.length)
    
    
    def save(self,* args, **kwargs):
        
        if self.end_time < self.start_time:
            self.length = datetime.combine(date.today() + timedelta(days=1), self.end_time) - datetime.combine(date.today(), self.start_time)
        else:
            self.length = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
            print(self.length)
        super(ShiftDefault, self).save()
    
def splitShift(shift):
        
    start_date = shift.start_time.date()
    ob = findObTime(shift.start_time)
    if hasattr(ob,'day'): # Regular OB time
        ob_end_datetime = datetime.combine(start_date,ob.end_time)
    else: # We found a super weekend
        ob_end_datetime = min(shift.end_time,ob.end_time)
        
    if ob.end_time == time(23,59,59):
        ob_end_datetime += timedelta(seconds=1)
    
    if shift.end_time <= ob_end_datetime: # Whole shift contained in obTime - End of recursion
        fragment = ShiftFragment(start_time = shift.start_time, end_time = shift.end_time, oblevel = ob.oblevel, main_shift=shift)
        fragment.save()
        return [fragment]
    else:
        fragment_end_time = ob_end_datetime
        fragment = ShiftFragment(start_time = shift.start_time, end_time = fragment_end_time, oblevel = ob.oblevel, main_shift=shift)
        fragment.save()
        shift.start_time= fragment_end_time
        return [fragment, splitShift(shift)]
        
        

    
def findObTime(start_date):
    
    try:
        specialDay = ObSpecials.objects.get(start_time__lte=start_date, end_time__gt=start_date)
        return specialDay
    except (ObjectDoesNotExist,MultipleObjectsReturned) as e:
        print("Matched no special day or multiple")
    
    start_time = start_date.time()
    weekday = start_date.weekday()
    if weekday < 5:
        weekday = -1
    return ObTimes.objects.get(day__exact=weekday, start_time__lte=start_time, end_time__gt=start_time) # Could be abstraced to using a range
    
    

        
    
    
    
    
    
    
    
    
    
    
    
    
    