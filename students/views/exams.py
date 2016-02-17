# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, DeleteView, CreateView
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML
from crispy_forms.bootstrap import FormActions

from ..models import Exam

# Views for Exams
def exams_list(request):
    exams = Exam.objects.all()

# order exams_list
    order_by = request.GET.get('order_by', '')
    if request.GET.get('order_by', '') == '':
        request.GET.order_by = 'exam_name'
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'exam_name', 'teacher_name', 'exam_day'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()
# paginate exams
    paginator = Paginator(exams, 3)
    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        exams = paginator.page(paginator.num_pages)


    return render(request, 'students/exams_list.html',
        {'exams': exams})


#class for groups form

class ExamCreateForm(ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_name', 'exam_day', 'teacher_name', 'exam_group']

    def __init__(self, *args, **kwargs):
        super(ExamCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('exams_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helperrender_unmentioned_fields = True
    #    self.helper.add_input(Submit('submit', u'Зберегти', css_class='btn btn-success'))
    #    self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-danger'))

        # add buttons
        self.helper.layout.append(FormActions(
            Div(css_class = self.helper.label_class),
            Submit('add_button', u'Зберегти', css_class="btn btn-success"),
            HTML(u"<a class='btn btn-danger' name='cancel_button' href='{% url 'exams' %}?status_message=Додавання іспиту скасовано!'>Скасувати</a>"),
        ))

#class for add group
class ExamCreateView(CreateView):
    model = Exam
    template_name = 'students/exams_add.html'
    form_class = ExamCreateForm
    

    def get_success_url(self):
        return u'%s?status_message=Іспит успішно створено' % reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Створення іспиту відмінено' % reverse('home'))
        else:
            return super(ExamCreateView, self).post(request, *args, **kwargs)



# class for exam update form

class ExamUpdateForm(ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_name', 'exam_day', 'teacher_name', 'exam_group']

    def __init__(self, *args, **kwargs):
        super(ExamUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('exams_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', u'Зберегти', css_class='btn btn-success'))
        self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-danger'))

        # add buttons
        self.helper.layout[-1] = Layout(FormActions())
 #       self.helper.layout[-1] = FormActions(
 #           Submit('add_button', u'Зберегти', css_class="btn btn-success"),
 #           Submit('cancel_button', u'Скасувати', css_class="btn btn-danger"),
 #       )


# class for update student
class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'students/exams_edit.html'
    form_class = ExamUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Іспит успішно відредаговано' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування іспиту відмінено' % reverse('home'))
        else:
            return super(ExamUpdateView, self).post(request, *args, **kwargs)


# delete group
class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message= Іспит успішно видалено!' % reverse('home')