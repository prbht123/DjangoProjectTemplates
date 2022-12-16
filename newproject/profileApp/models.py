from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	gender = models.CharField(max_length=100)
	address = models.CharField(max_length=500)
	dob = models.DateField(null=True)
	profile_image = models.ImageField(upload_to='images', null=True)

	def __str__(self):
		return 'Profile of user: {}'.format(self.user.username)

@receiver(post_save, sender=User)
def create_and_save_userprofile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()

