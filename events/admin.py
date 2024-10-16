from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Booking

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # Inherit default fieldsets
        (
            'Additional Information',
            {
                'fields': (
                    'is_organizer',
                )
            }
        ),
    )

admin.site.register(CustomUser, UserAdmin)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'venue', 'date', 'time', 'category')
    list_filter = ('category', 'organizer')
    search_fields = ('title', 'venue')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee', 'booking_date', 'payment_method', 'confirmation_sent')
    list_filter = ('event', 'payment_method', 'confirmation_sent')
    search_fields = ('event__title', 'attendee__username')