import csv
import datetime

import nested_admin
from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .mail import send_workshop_confirmation, send_workshop_rejected, send_workshop_waiting_list
from .models import Workshop, WorkshopRegistration, Question, AnswerOption, RegistrationAnswer, Location


class RegistrationAnswerInLine(admin.TabularInline):
    model = RegistrationAnswer
    extra = 0
    fields = ('question', 'text')
    readonly_fields = fields


class ActiveStatusFilter(admin.SimpleListFilter):
    title = _('Activity')
    parameter_name = "active"

    def lookups(self, request, model_admin):
        return (
            (True, _("Active")),
            (False, _("Inactive")),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(active=self.value())


class AutoResponseFilter(admin.SimpleListFilter):
    title = _('Auto Response')
    parameter_name = "auto_response"

    def lookups(self, request, model_admin):
        return (
            (True, _("Yes")),
            (False, _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(workshop__auto_response=self.value())


def workshop_free_seats(workshop):
    slots = workshop.slots
    accepted = WorkshopRegistration.objects.filter(workshop=workshop, accepted='AC', active=True).count()
    return slots - accepted


class FreeSeatsFilter(admin.SimpleListFilter):
    title = _('Free slots available')
    parameter_name = "auto_response"

    def lookups(self, request, model_admin):
        return (
            (True, _("Yes")),
            (False, _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        result = []
        for q in queryset:
            if workshop_free_seats(q) > 0:
                result.append(q)
        return result


class WorkshopRegistrationAdmin(admin.ModelAdmin):
    actions = ['accept', 'reject', 'waiting_list', "export_as_csv"]

    def accept(self, request, queryset):
        for obj in queryset:
            obj.accepted = WorkshopRegistration.Status.ACCEPTED
            obj.save()
            send_workshop_confirmation(obj.workshop, obj.participant, request)

    accept.short_description = 'Accept selected'

    def reject(self, request, queryset):
        for obj in queryset:
            obj.accepted = WorkshopRegistration.Status.REJECTED
            obj.save()
            send_workshop_rejected(obj.workshop, obj.participant, request)

    reject.short_description = 'Reject selected'

    def waiting_list(self, request, queryset):
        for obj in queryset:
            obj.accepted = WorkshopRegistration.Status.WAITING_LIST
            obj.save()
            send_workshop_waiting_list(obj.workshop, obj.participant, request)

    waiting_list.short_description = 'Waiting List'

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

    inlines = [RegistrationAnswerInLine, ]
    list_display = ['workshop', 'participant', 'active', 'accepted', 'date', 'list_answers', 'free_seats']
    list_filter = ('workshop', ActiveStatusFilter, 'accepted', AutoResponseFilter, FreeSeatsFilter)

    def list_answers(self, obj):
        to_return = '<ul>'
        to_return += '\n'.join(
            '<li>{}</li>'.format(ans.question.text + ' ' + ans.text) for ans in obj.answers.all())
        to_return += '</ul>'
        return mark_safe(to_return)

    def free_seats(self, obj):
        slots = obj.workshop.slots
        free_seats = workshop_free_seats(obj.workshop)
        waiting_list = WorkshopRegistration.objects.filter(workshop=obj.workshop, accepted='WL', active=True).count()
        res = '<ul>'
        res += '<li>{}</li>'.format('Free slots available: ' + str(free_seats))
        res += '\n<li>{}</li>'.format('Waiting list: ' + str(waiting_list))
        res += '\n<li>{}</li>'.format('Slots: ' + str(slots))
        res += '</ul>'
        return mark_safe(res)


class AnswerOptionInLine(nested_admin.NestedTabularInline):
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
    inlines = [AnswerOptionInLine]


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
admin.site.register(WorkshopRegistration, WorkshopRegistrationAdmin)
admin.site.register(Location)
admin.site.unregister(Group)
