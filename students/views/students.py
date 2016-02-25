
from datetime import datetime

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

from PIL import Image

from ..models import Student, Group
from ..util import paginate, get_current_group

# Views for Students
def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()
# order student_list
    order_by = request.GET.get('order_by', 'last_name')
    
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
# paginate students

    context = paginate(students, 3, request, {}, var_name='students')
#    paginator = Paginator(students, 3)
#    page = request.GET.get('page')
#    try:
#        students = paginator.page(page)
#    except PageNotAnInteger:
        # If page is not an integer, deliver first page
#        students = paginator.page(1)
#    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
#        students = paginator.page(paginator.num_pages)

    
    return render(request, 'students/students_list.html',
        context)

@login_required
def students_add(request):

    if request.method == "POST":
      # if button was pressed
        if request.POST.get('add_button') is not None:
       # grab errors
            errors = {}
        # data for student object
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}
        # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _(u"First Name field is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = _(u"Last Name field is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _(u"Birthday field is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    _(u'Please, add correct data (ex. 1991-02-21)')
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required")
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u'Choose student group')
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = _(u'Please, choose correct group')
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo', '')
            if not photo:
                errors['photo'] = _(u'Please, upload photo')
            else:
                    im = Image.open(photo)
                    if im.format not in ('JPEG', 'PNG'):
                        errors['photo'] = _(u'Please, upload .png or .jpeg file')
                    if photo.size > 3145728:
                        errors['photo'] = _(u'Max photo size - 3 Mb')
                    else:
                        data['photo'] = photo
       #save student
            if not errors:
                student = Student(**data)
                student.save()
                # status message
                #redirect to student_list
                messages.success(request, _(u'Student created successfully!'))
                return HttpResponseRedirect(reverse('home'))
            else:
# template with errors
                messages.error(request, _(u'Please correct the following errors'))
                return render(request, 'students/students_add.html', 
                {'groups': Group.objects.all().order_by('title'),
                'errors': errors})

        elif request.POST.get('cancel_button') is not None:
# redirect to home page on cancel button
            messages.error(request, _(u'Adding the Student canceled'))
            return HttpResponseRedirect(reverse('home'))
    else:
# redirect on start
        return render(request, 'students/students_add.html',
        {'groups': Group.objects.all().order_by('title')})
# class for student update form

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'student_group', 'birthday', 'photo', 'ticket', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-6'
        self.helper.add_input(Submit('submit', _(u'Save'), css_class='btn btn-success'))
        self.helper.add_input(Submit('cancel_button', _(u'Cancel'), css_class='btn btn-danger'))

        # add buttons
        self.helper.layout[-1] = Layout(FormActions())



# class for update student

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), _(u"Student updated successfully!"))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('home'), _(u"Student updated canceled!")))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)
        
        



#def students_edit(request, sid):
#    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message%s' % (reverse('home'), _(u"Student delete successfully!"))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)
#def students_delete(request, sid):
#    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
