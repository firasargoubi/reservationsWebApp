from django.db import models
from django.contrib.auth.models import User

class Units(models.Model) :
    name = models.TextField()

class Garage(models.Model) :
    
    number = models.IntegerField()
    code = models.IntegerField()
  
class Client(models.Model) :
    
    def get_default_garage_num():
        return Garage.objects.first().number  
        
    username = models.TextField()
    email = models.TextField()
    start_date = models.TextField(null = True)
    end_date= models.TextField(null = True)
    unit = models.TextField(null = True)
    garage_num = models.IntegerField(null = True)
    invalid = models.BooleanField(null = True)




    
    