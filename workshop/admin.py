from django.contrib import admin
from .models import Workshop, WorkshopRegistration, Question, AnswerOption, RegistrationAnswer, Location
from django.http import HttpResponse
import csv
from django.db import models
from django.forms import TextInput
from django import forms
import nested_admin
import datetime


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
    model = AnswerOption
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 80})},
    }


class QuestionInLine(nested_admin.NestedTabularInline):
    model = Question
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 80})},
    }
    exclude = ['active']
    inlines = [DefaultAnswerInLine]


class AddWorkshopModelForm(forms.ModelForm):
    date = forms.DateField(widget=admin.widgets.AdminDateWidget)
    start = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timepicker'}))
    end = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timepicker'}))

    def save(self, commit=True):
        form = super(AddWorkshopModelForm, self).save(commit=False)

        date = self.cleaned_data.get('date', None)
        start = self.cleaned_data.get('start', None)
        end = self.cleaned_data.get('end', None)

        form.start_date = datetime.datetime.combine(date, start)
        form.end_date = datetime.datetime.combine(date, end)

        if commit:
            form.save()
        return form

    class Media:
        css = {
            'all': (
                'http://cdnjs.cloudflare.com/ajax/libs/timepicker/1.3.5/jquery.timepicker.min.css',
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css',
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
            )
        }
        js = (
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'http://cdnjs.cloudflare.com/ajax/libs/timepicker/1.3.5/jquery.timepicker.min.js',
            'js/time_picker.js',
        )

    class Meta:
        model = Workshop
        fields = '__all__'
        exclude = ('end_date', 'start_date')


class ChangeWorkshopModelForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = '__all__'


class WorkshopAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInLine]

    def add_view(self, request):
        self.form = AddWorkshopModelForm
        return super(WorkshopAdmin, self).add_view(request)

    def change_view(self, request, object_id):
        self.form = ChangeWorkshopModelForm
        return super(WorkshopAdmin, self).change_view(request, object_id)


admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(WorkshopRegistration, WorkshposRegistrationsAdmin)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(RegistrationAnswer)
admin.site.register(Location)
