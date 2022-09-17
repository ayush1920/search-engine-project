from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
	class Meta:
		verbose_name_plural = "Histories"
	search_query = models.CharField(max_length=120)
	selected_disk = models.CharField(max_length=30)
	result = models.TextField(blank=True)
	file_extension = models.CharField(max_length=30, default="invalid")
	timestamp = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	def __str__(self):
		return self.search_query

class Log(models.Model):
	search_query = models.CharField(max_length=120)
	selected_disk = models.CharField(max_length=30)
	result = models.TextField(blank=True)
	file_extension = models.CharField(max_length=30, default="invalid")
	timestamp = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.search_query

class AuthToken(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=500)