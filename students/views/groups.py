# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView, CreateView
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML
from crispy_forms.bootstrap import FormActions

from ..models import Group
from ..util import paginate


# Views for Groups
def groups_list(request):
    groups = Group.objects.all()
# try order groups_list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
# paginate groups
#    paginator = Paginator(groups, 3)
#    page = request.GET.get('page')
#    try:
#        groups = paginator.page(page)
#    except PageNotAnInteger:
        # If page is not an integer, deliver first page
#        groups = paginator.page(1)
#    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
#        groups = paginator.page(paginator.num_pages)
    context = paginate(groups, 3, request, {}, var_name='groups')

    return render(request, 'students/groups_list.html', context)

#class for groups form

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-6 control-label'
        self.helper.field_class = 'col-sm-6'
        self.helperrender_unmentioned_fields = True
    #    self.helper.add_input(Submit('submit', u'Зберегти', css_class='btn btn-success'))
    #    self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-danger'))

        # add buttons
        self.helper.layout.append(FormActions(
            Div(css_class = self.helper.label_class),
            Submit('add_button', u'Зберегти', css_class="btn btn-success"),
            HTML(u"<a class='btn btn-danger' name='cancel_button' href='{% url 'groups' %}?status_message=Додавання групи скасовано!'>Скасувати</a>"),
        ))

#class for add group
class GroupCreateView(CreateView):
    model = Group
    template_name = 'students/groups_add.html'
    form_class = GroupCreateForm
    

    def get_success_url(self):
        return u'%s?status_message=Групу успішно створено' % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Створення групи відмінено' % reverse('home'))
        else:
            return super(GroupCreateView, self).post(request, *args, **kwargs)

#def groups_add(request):
#    return HttpResponse('<h1>Group Add Form</h1>')

##def groups_edit(request, sid):
 #   return HttpResponse('<h1>Edit Group %s</h1>' % sid)

# class for group update form

class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_edit',
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
class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Групу успішно відредаговано' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування групи відмінено' % reverse('home'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


# delete group
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message= Групу успішно видалено!' % reverse('home')
#def groups_delete(request, sid):
#    return HttpResponse('<h1>Delete Group %s</h1>' % sid)
