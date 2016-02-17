# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models import Student, Group, Exam, MonthJournal

class StudentFormAdmin(ModelForm):
# get group where current student is a leader
	def clean_student_group(self):
		groups = Group.object.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
		    raise ValidationError(u'Студент є старостою іншої групи', code='invalid')

		return self.cleaned_data['student_group']
		
		

class StudentAdmin(admin.ModelAdmin):
	list_display = ['last_name', 'first_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['last_name']
	list_filter = ['last_name', 'first_name', 'middle_name', 'ticket']
	list_per_page = 10
	search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
	form = StudentFormAdmin

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk': obj.id})


class GroupAdmin(admin.ModelAdmin):
	list_display = ['title', 'leader']
	list_display_links = ['title', 'leader']
	ordering = ['title']
	list_filter = ['title', 'leader']
	list_per_page = 10
	search_fields = ['title', 'leader', 'notes']

	def view_on_site(self, obj):
		return reverse('groups_edit', kwargs={'pk': obj.id})

class ExamAdmin(admin.ModelAdmin):
	list_display = ['exam_name', 'exam_day', 'teacher_name', 'exam_group']
	list_display_links = ['exam_name', 'exam_day', 'teacher_name', 'exam_group']
	ordering = ['exam_name']
	list_filter = ['exam_name', 'exam_day', 'teacher_name']
	list_per_page = 10
	search_fields = ['exam_name', 'exam_day', 'teacher_name', 'exam_group']

	def view_on_site(self, obj):
		return reverse('exams_edit', kwargs={'pk': obj.id})


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(MonthJournal)
