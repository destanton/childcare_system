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
        return Time.objects.all()


class Child(models.Model):
    parent = models.ForeignKey('auth.User')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    pin = models.CharField(unique=True, max_length=4)

    def __str__(self):
        return self.first_name

    @property
    def onsite(self):
        return Time.objects.filter(child=self)


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
    def rename(self):
        if not self.on_premise == True:
            return str("Not In Facility")
        else:
            return str("In Facility")

    @property
    def get_time(self):
        return self.check_out - self.check_in
