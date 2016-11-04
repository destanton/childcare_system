from django.contrib import admin
from track.models import Child, Profile, Time

admin.site.register([Child, Profile, Time])
