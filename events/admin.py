from django.contrib import admin
from .models import Event, Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['organizer', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created']
    prepopulated_fields = {'slug': ('title',)}
