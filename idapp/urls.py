from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

import views

urlpatterns = [url(r'^$',views.mainpage,name='Main'),
				url(r'^studentHome$',views.studentHome,name='studentHome'),
				url(r'^facultyHome$',views.facultyHome,name='facultyHome'),
				url(r'^studentRegistration/$',views.studentRegistration,name='studentRegistration'),
				url(r'^facultyRegistration/$',views.facultyRegistration,name='facultyRegistration'),
				url(r'^studentPdf/$',views.studentPdf,name='studentPdf'),
				url(r'^studentListSave/$',views.studentListSave,name='studentListSave'),
				url(r'^studentSave/$',views.studentSave,name='studentSave'),
				url(r'^facultySave/$',views.facultySave,name='facultySave'),
				url(r'^studentDelete/$',views.studentDelete,name='studentDelete'),
				url(r'^facultyDelete/$',views.facultyDelete,name='facultyDelete'),
				url(r'^studentTemplateInput/$', views.studentTemplateInput, name='studentTemplateInput'),
				url(r'^studentTemplate/$', views.studentTemplate, name='studentTemplate'),
				url(r'^facultyTemplateInput/$', views.facultyTemplateInput, name='facultyTemplateInput'),
				url(r'^facultyTemplate/$', views.facultyTemplate, name='facultyTemplate'),
				url(r'^studentPdfPreview/$', views.studentPdfPreview, name='studentPdfPreview'),
				url(r'^facultyPdfPreview/$', views.facultyPdfPreview, name='facultyPdfPreview'),
				url(r'^facultyPdf/$',views.facultyPdf,name='facultyPdf'),
				url(r'^studentList/$',views.studentList,name='studentList'),
				url(r'^facultyList/$',views.facultyList,name='facultyList'),
				url(r'^login/$',views.login1,name='login'),
				url(r'^logout/$',views.logout1,name='logout'),
				url(r'^singleStudent/$',views.singleStudent,name='singleStudent'),
				url(r'^studentEdit/(?P<id>\d+)/$',views.studentEdit,name='studentEdit'),
				url(r'^facultyEdit/(?P<id>\d+)/$',views.facultyEdit,name='facultyEdit'),
				url(r'^studentPdfHome/$',views.studentPdfHome,name='studentPdfHome'),
				url(r'^report/$',views.report,name='report'),
				
				]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
