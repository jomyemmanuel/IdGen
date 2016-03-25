from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

import views

urlpatterns = [url(r'^$',views.mainpage,name='Main'),
				url(r'^1$',views.mainstu,name='Mainstu'),
				url(r'^2$',views.mainfac,name='Mainfac'),
				url(r'^student/$',views.student,name='student'),
				url(r'^faculty/$',views.faculty1,name='faculty'),
				url(r'^genpdf/$',views.generatepdf,name='genpdf'),
				url(r'^editpagestud/$',views.editstud,name='editpagestud'),
				url(r'^studsave/$',views.studsave,name='studsave'),
				url(r'^editpagefac/$',views.editfac,name='editpagefac'),
				url(r'^facsave/$',views.facsave,name='facsave'),
				url(r'^studel/$',views.delstud,name='studel'),
				url(r'^facdel/$',views.delfac,name='facdel'),
				url(r'^siddesign/$', views.siddesign, name='siddesign'),
				url(r'^pdfsdesign/$', views.pdfsdesign, name='pdfsdesign'),
				url(r'^fiddesign/$', views.fiddesign, name='fiddesign'),
				url(r'^pdffdesign/$', views.pdffdesign, name='pdffdesign'),
				url(r'^rlab/$', views.rlab, name='rlab'),
				url(r'^flab/$', views.flab, name='flab'),
				url(r'^genpdf1/$',views.genpdf1,name='genpdf1'),
				url(r'^liststud/$',views.liststud,name='liststud'),
				url(r'^listfac/$',views.listfac,name='listfac'),
				url(r'^login/$',views.login1,name='login'),
				url(r'^logout/$',views.logout1,name='logout'),
				url(r'^singlestud/$',views.singlestud,name='singlestud'),
				url(r'^studentEdit/(?P<id>\d+)/$',views.studentEdit,name='studentEdit'),
				url(r'^facultyEdit/(?P<id>\d+)/$',views.facultyEdit,name='facultyEdit'),
				url(r'^studentpdfhome/$',views.studentpdfhome,name='studentpdfhome')
				
				]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
