from django.contrib import admin
from .models import Profile, Skill, Message

# Register your models here.
#admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.urls import path
from .models import Profile
from django.utils.html import format_html



class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('material_icons_link',)

    def material_icons_link(self, obj):
        return format_html('<a href="https://fonts.google.com/icons?icon.set=Material+Icons" target="_blank">Material Icons</a>')

    material_icons_link.allow_tags = True
    material_icons_link.short_description = 'Material Icons Link'

admin.site.register(Profile, ProfileAdmin)
