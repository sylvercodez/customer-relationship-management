from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import Customers

def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='customers')
		instance.groups.add(group)
		Customers.objects.create(
			user=instance,
			Name=instance.username,
			)
		print('Profile created sucessfully!!')

post_save.connect(customer_profile, sender=User)