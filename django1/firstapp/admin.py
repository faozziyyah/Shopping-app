from django.contrib import admin
from .models import Venue
from .models import Userlist
from .models import Event
#from django.contrib.auth.models import Group

# remove groups
#admin.site.unregister(Group)

# Register your models here.
#admin.site.register(Venue)
admin.site.register(Userlist)
#admin.site.register(Event)

#admin.site.register(Venue, VenueAdmin)
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address', 'phone')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'venue', 'event_date', 'description', 'manager', 'approved')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)
    search_fields = ('name', 'event_date')