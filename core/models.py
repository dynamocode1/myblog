from django.db import models
from django.urls import reverse
class Profile(models.Model):
	user = models.OneToOneField('auth.User',on_delete = models.CASCADE,related_name = 'profile')
	bio = models.CharField(max_length = 1220)
	address = models.CharField(max_length = 1220)
	roles = models.ForeignKey('Role',on_delete = models.CASCADE,related_name= 'profiles',null = True)
	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.user.username
	def edit_url(self):
		return reverse('editprofile',kwargs = {'id':self.user.id})

class Post(models.Model):
	profile = models.ForeignKey(Profile,on_delete = models.CASCADE,related_name= 'posts')
	title = models.CharField(max_length = 2030)
	body = models.CharField(max_length = 237898)
	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.title
	def readmore_url(self):
		return reverse('readmore',kwargs = {'id':self.id})
	def delete_url(self):
		return reverse('deleteposts',kwargs = {'id':self.id})
	def edit_url(self):
		return reverse('editpost',kwargs = {'id':self.id})
	



class Role(models.Model):
	name =  models.CharField(max_length = 2030)
	date = models.DateTimeField(auto_now_add = True,null= True)
