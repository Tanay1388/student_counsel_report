from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

from django.db.models.deletion import CASCADE

# Room going to be child of Topic so create Topic first
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Room going to be child of Class so create Topic first
class Class(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Room going to be child of India_Abroad so create Topic first
class India_Abroad(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



# Create your models here.
# Class name is table name.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    Class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    India_Abroad = models.ForeignKey(India_Abroad, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=800, null=True, blank=True)# so this field can be left blank
    summary = models.TextField(max_length=600, null=True, blank=True)# so this field can be left blank
    recoTest = models.TextField(max_length=100, null=True, blank=True)# so this field can be left blank
    recoUniv = models.TextField(max_length=100, null=True, blank=True)# so this field can be left blank
    subjects = models.TextField(max_length=100, null=True, blank=True)# so this field can be left blank
    dreamCareer = models.TextField(max_length=100, null=True, blank=True)# so this field can be left blank
    majorPlan = models.TextField(max_length=100, null=True, blank=True)# so this field can be left blank
    emailID = models.TextField(max_length=50, null=True, blank=False)
    contactID = models.TextField(max_length=30, null=True, blank=False)
    counsellors = models.ManyToManyField(User, related_name='counsellors', blank=True)
    # here we can't use simply User as relation as it is used before
    # in this model so we need to mention the relation.
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)#Auto_now saves every time but Auto_now_add is created once 

    class Meta:
        # For Ascending order
        ordering = ['-updated', '-created']
        # for descending order
        # ordering = ['updated', 'created']
        # also try
        #  ordering = ['-created', '-updated']


    def __str__(self):
        return self.name
    # str(self.attribute) when concatinate integer or something else

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    # WHen parent deleted data also deleted
    # room = models.ForeignKey(Room, on_delete=models.SET_NULL) #(For when the parents dataset deleted the daughter dataset remains)
    # here models.ForeignKey(Room,..) Room is for 
    # one to many so for one room many messages 
    body = models.TextField()
    updates = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)#Auto_now saves every time but Auto_now_add is created once 
    
    class Meta:

        ordering = ['-created']

    
    def __str_(self):
        return self.body[0:50]


