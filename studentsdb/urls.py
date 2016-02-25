from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.groups import GroupDeleteView, GroupUpdateView, GroupCreateView, groups_list
from students.views.exams import ExamDeleteView, ExamUpdateView, ExamCreateView, exams_list
from students.views.journal import JournalView


js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studentsdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # My Student urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$', 'students.views.students.students_add',
        name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        login_required(StudentUpdateView.as_view()),
        name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$',
        login_required(StudentDeleteView.as_view()),
        name='students_delete'),


    # My Groups urls
    url(r'^groups/$', login_required(groups_list), name='groups'),
    url(r'^groups/add/$', login_required(GroupCreateView.as_view()),
        name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$',
        login_required(GroupUpdateView.as_view()),
        name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$',
        login_required(GroupDeleteView.as_view()),
        name='groups_delete'),

    # My Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', login_required(JournalView.as_view()), name='journal'),
  #  url(r'^journal/(?P<sid>\d+)/update/$',    'students.views.journal.journal_update',
 #       name='journal_update'),

  # My Exam urls
    url(r'^exams/$', login_required(exams_list), name='exams'),
    url(r'^exams/add/$', login_required(ExamCreateView.as_view()),
        name='exams_add'),
    url(r'^exams/(?P<pk>\d+)/edit/$',
        login_required(ExamUpdateView.as_view()),
        name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/delete/$',
        login_required(ExamDeleteView.as_view()),
        name='exams_delete'),
   # Contact Admin Form
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),
    # url for javascript translation
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # User Related urls
    url(r'^users/profile/$', login_required(TemplateView.as_view(template_name='registration/profile.html')),
     name='profile'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    # Social Auth Related urls
    url('^social/', include('social.apps.django_app.urls', namespace='social')),


    url(r'^admin/', include(admin.site.urls)),
)

from .settings import MEDIA_ROOT, DEBUG

if DEBUG:
# serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))