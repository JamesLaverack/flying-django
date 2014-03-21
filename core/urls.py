from django.conf.urls import *
from django.conf import settings
from core import views

urlpatterns = patterns('',
#                       url(r'^$', views.hello_world, name='hello-world'),
                       url(r'testlogin/$', views.googlelogin),
                       url(r'^$', views.BlogPostListView.as_view(), name='list-posts'),
                       url(r'new/$', views.BlogPostCreateView.as_view(), name='new-post'),
                       url(r'^(?P<slug>[-_\w]+)/$', views.BlogPostDetailView.as_view(), name='view-post'),
                       url(r'^(?P<slug>[-_\w]+)/edit$', views.BlogPostUpdateView.as_view(), name='edit-post'),
                       url(r'^(?P<slug>[-_\w]+)/delete$', views.BlogPostDeleteView.as_view(), name='delete-post'),
                       url(r'comment/(?P<slug>[-_\w]+)/edit$', views.CommentUpdateView.as_view(), name='edit-comment'),
                       url(r'comment/(?P<slug>[-_\w]+)/delete$', views.CommentDeleteView.as_view(), name='delete-comment'),

)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )
