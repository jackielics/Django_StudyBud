from django.db import models
from django.contrib.auth.models import User # 直接使用内置User类

class Topic(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return str(self.name)

class Room(models.Model):
	'''
    
	'''
	host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
	name = models.CharField(max_length=200)
	description = models.TextField(null = True, blank = True) # CAN be blank

	participants = models.ManyToManyField(
		User, related_name = 'participants', blank = True) # many-to-many relationship
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True) # only record the first time called

	class Meta:
		ordering = ['-updated', '-created'] # - dash 

	def __str__(self):
		return str(self.name)
	
class Message(models.Model):
	# one-to-many relationship
	user = models.ForeignKey(User, on_delete=models.CASCADE) # if the user is deleted, delete the message
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	body = models.TextField() # mainbody of message
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True) # only record the first time called

	class Meta:
		ordering = ['-updated', '-created']


	def __str__(self):
		return self.body[:50]