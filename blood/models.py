from django.db import models
from django.contrib.auth.models import User


class Recepient(models.Model):
	user = models.ManyToManyField(User)
   	name=models.CharField(max_length=200)
	address=models.CharField(max_length=200)
	contact=models.CharField(max_length=10)
	bggroup=models.CharField(max_length=2)
	email=models.CharField(max_length=100)
	bgunits=models.IntegerField(blank=True)
	age=models.IntegerField(blank=True)
	lat1=models.FloatField(blank=True,null=True)
	long1=models.FloatField(blank=True,null=True)

class Donor(models.Model):
	user = models.ManyToManyField(User)
	name=models.CharField(max_length=200)
	address=models.CharField(max_length=200)
	contact=models.CharField(max_length=10)
	bggroup=models.CharField(max_length=2)
	email=models.CharField(max_length=100)
	bgunits=models.IntegerField(blank=True)
	age=models.IntegerField(blank=True)
	lat1=models.FloatField(blank=True,null=True)
	long1=models.FloatField(blank=True,null=True)

class Hospital(models.Model):
	contact=models.CharField(max_length=10)
	address=models.CharField(max_length=200)
	name=models.CharField(max_length=200)
	abgroup=models.CharField(max_length=200)

class Camp(models.Model):
	name=models.CharField(max_length=200)
	email=models.CharField(max_length=100)
	contact=models.CharField(max_length=10)
	address=models.CharField(max_length=200)	
	uid=models.IntegerField()
	cdate = models.CharField(max_length=200)
	sdate=models.CharField(max_length=200)
	edate=models.CharField(max_length=200)
	lat1=models.FloatField(blank=True,null=True)
	long1=models.FloatField(blank=True,null=True)

class Link(models.Model):
	uid=models.IntegerField()
	cid=models.IntegerField()
	guser=models.CharField(max_length=200)
	flag=models.IntegerField(blank=True)

class Post(models.Model):
	uid = models.IntegerField()
	#user=models.ForeignKey(User)
	comment=models.CharField(max_length=200)
	campid=models.CharField(max_length=200)

class Story(models.Model):
	suser = models.ManyToManyField(User)
	story=models.CharField(max_length=200)
	tag=models.CharField(max_length=200)
	#pic=models.ImageField(upload_to="static",blank=True)

class Notification(models.Model):
	did = models.ManyToManyField(User)
	#did=models.ForeignKey(User)
	rid=models.CharField(max_length=200)
	flag=models.IntegerField(blank=True)

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

class Choice(models.Model):
	question = models.ManyToManyField(Question)
    	#question = models.ForeignKey(Question)
    	choice_text = models.CharField(max_length=200)
    	votes = models.IntegerField(default=0)

