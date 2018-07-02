from django.db import models


from memberships.models import Membership


class Course(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=120)
	description = models.TextField()
	allowed_memberships = models.ManyToManyField(Membership)

	def __str__(self):
		return self.title


class Lesson(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=120)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
	position = models.IntegerField()
	video_url = models.CharField(max_length=200)
	thumbnail = models.ImageField()

	def __str__(self):
		return self.title