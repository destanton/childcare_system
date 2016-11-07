from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

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

    @property
    def is_parent(self):
        return self.access_level == 'p'

    @property
    def child_list(self):
        if self.access_level == 'p':
            return Child.objects.filter(parent=self.user)
        return Child.objects.all()

    @property
    def time_list(self):
        if self.access_level == 'p':
            child_list = self.child_list
            for child in child_list:
                return child.all_checkin

    @property
    def child_bill(self):
        child_list = self.child_list
        bill = round(sum(child.profile_bill for child in child_list), 2)
        return str("{} {}").format('$', bill)


class Child(models.Model):
    parent = models.ForeignKey('auth.User')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    pin = models.CharField(unique=True, max_length=4)

    def __str__(self):
        return self.first_name

    @property
    def all_checkin(self):
        return Time.objects.filter(child=self)

    @property
    def total_time(self):
        total_time = self.all_checkin
        new_time = sum(time.get_time.seconds for time in total_time)
        # for time in total_time:
        #     return time.get_time.seconds
        return float(new_time / 3600)

    @property
    def total_bill(self):
        total_time = self.total_time
        cost = 12.00
        new_cost = round(float(total_time * cost), 2)
        return str("{} {}").format('$', new_cost)

    @property
    def profile_bill(self):
        total_time = self.total_time
        cost = 12.00
        new_cost = round(float(total_time * cost), 2)
        return new_cost

    @property
    def is_onsite(self):
        total_time = self.all_checkin
        for time in total_time:
            return time.onsite_rename


class Time(models.Model):
    child = models.ForeignKey(Child)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(auto_now=False, null=True)
    on_premise = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-id',)

    @property
    def onsite_rename(self):
        if not self.on_premise == True:
            return str("Not In Facility")
        else:
            return str("In Facility")

    @property
    def get_time(self):
        return self.check_out - self.check_in
