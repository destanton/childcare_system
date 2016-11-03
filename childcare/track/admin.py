from django.contrib import admin
from track.models import Child, Profile

admin.site.register([Child, Profile])
