# coding=utf-8
"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete

urlpatterns = [
    url(r'^$', 'DueLink.views.home', name='home'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'duelink/login.html'}, name='login'),
    url(r'^register$', 'DueLink.views.register', name='register'),

    url(r'^friend_list$', 'DueLink.views.get_friend_list', name='friend_list'),
    url(r'^friend_stream', 'DueLink.views.get_friend_stream', name='friend_stream'),

    url(r'^profile/(?P<id>\d+)$', 'DueLink.views.get_profile', name='profile'),

    url(r'^profile_image/(?P<id>\d+)$', 'DueLink.views.get_user_image', name="profile_image"),

    url(r'^add_course$', 'DueLink.views.add_course', name='add_course'),
    url(r'^add_deadline$', 'DueLink.views.add_deadline', name='add_deadline'),
    url(r'^add_school$', 'DueLink.views.add_school', name='add_school'),


    # # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'edit-profile$', 'DueLink.views.edit_profile', name='edit_profile'),

    url(r'^password_reset$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'duelink/password_reset.html',
         'email_template_name': 'duelink/password_reset_email.html',
         'subject_template_name': 'duelink/password_reset_subject',
         }, name='password_reset'),
    # The page shown after a user has been emailed a link to reset their password.
    url(r'^password_reset_done$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'duelink/password_reset_done.html'
         }, name='password_reset_done'),
    # Presents a form for entering a new password.
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'duelink/password_reset_confirm.html',
         'post_reset_redirect': 'password_reset_complete',
         }, name='password_reset_confirm'),
    # Presents a view which informs the user that the password has been successfully changed.
    url(r'^password_reset_complete$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'duelink/password_reset_complete.html'
         }, name='password_reset_complete'),
]
