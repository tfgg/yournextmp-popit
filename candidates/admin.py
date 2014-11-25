from django.conf import settings
from django.contrib import admin
from django.forms import ModelForm

from .models import LoggedAction
# Register your models here.

class LoggedActionAdminForm(ModelForm):
    pass

class LoggedActionAdmin(admin.ModelAdmin):
    form = LoggedActionAdminForm
    list_display = ['user', 'action_type', 'popit_person_version_search_link',
                    'popit_person_link', 'created', 'updated', 'source']
    ordering = ('-created',)

    def popit_person_link(self, o):
        return '<a href="{0}persons/{1}">{2}</a>'.format(
            settings.POPIT_API_BASE_URL,
            o.popit_person_id,
            o.popit_person_id,
        )
    popit_person_link.allow_tags = True

    def popit_person_version_search_link(self, o):
        return '<a href="{0}search/persons?q=versions.version_id:{1}">{2}</a>'.format(
            settings.POPIT_API_BASE_URL,
            o.popit_person_new_version,
            o.popit_person_new_version,
        )
    popit_person_version_search_link.allow_tags = True

admin.site.register(LoggedAction, LoggedActionAdmin)
