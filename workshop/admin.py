from django.contrib import admin
from .models import Workshop, WorkshopRegistration, Question, DefaultAnswer, RegistrationAnswer, Location
from django.http import HttpResponse
import csv
from django.db import models
from django.forms import TextInput, Textarea
import nested_admin


class WorkshposRegistrationsAdmin(admin.ModelAdmin):
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class DefaultAnswerInLine(nested_admin.NestedTabularInline):
    model = DefaultAnswer
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 80})},
    }


class QuestionInLine(nested_admin.NestedTabularInline):
    model = Question
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 80})},
    }
    exclude = ['active']
    inlines = [DefaultAnswerInLine]


class WorkshopAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInLine]


admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(WorkshopRegistration, WorkshposRegistrationsAdmin)
admin.site.register(Question)
admin.site.register(DefaultAnswer)
admin.site.register(RegistrationAnswer)
admin.site.register(Location)
