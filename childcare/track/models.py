from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

ACCESS_LEVEL = [
    ("s", "staff"),
    ("p", "parent"),
]


@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance, access_level='p')


class Profile(models.Model):
    user = models.OneToOneField('auth.user')
    access_level = models.CharField(max_length=1, choices=ACCESS_LEVEL)

    def __str__(self):
        return self.user.username

    @property
    def is_staff(self):
        return self.access_level == 's'


class Child(models.Model):
    parent = models.ForeignKey('auth.User')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    pin = models.CharField(unique=True, max_length=4)

    def __str__(self):
        return str(self.id)

    @property
    def onsite(self):
        return Time.objects.filter(child=self)


class Time(models.Model):
    child = models.ForeignKey(Child)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(auto_now_add=True)
    on_premise = models.BooleanField(default=False)
