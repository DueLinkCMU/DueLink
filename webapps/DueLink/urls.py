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
    url(r'^home$', 'DueLink.views.home', name='home'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'duelink/login.html'}, name='login'),
    url(r'^register$', 'DueLink.views.register', name='register'),

    url(r'^friend_list$', 'DueLink.views.get_friend_list', name='friend_list'),
    url(r'^friend_stream', 'DueLink.views.get_friend_stream', name='friend_stream'),

    url(r'^profile/(?P<id>\d+)$', 'DueLink.views.get_profile', name='profile'),

    url(r'^profile_image/(?P<id>\d+)$', 'DueLink.views.get_user_image', name="profile_image"),

    url(r'^add_event$', 'DueLink.views.add_event', name='add_event'),

    url(r'^add_task$', 'DueLink.views.add_task', name='add_task'),
    url(r'^tasks/(?P<event_id>\d+)$', 'DueLink.views.display_tasks', name='tasks'),
    url(r'^get_tasks/(?P<event_id>\d+)$', 'DueLink.views.get_tasks', name='get_tasks'),
    url(r'^update_task/(?P<task_id>\d+)$', 'DueLink.views.update_task', name='update_task'),
    url(r'^delete_task/(?P<task_id>\d+)$', 'DueLink.views.delete_task', name='delete_task'),
    url(r'^add_school$', 'DueLink.views.add_school', name='add_school'),
    url(r'^get_schedule', 'DueLink.views_schedule.get_schedule', name='get_schedule'),

    url(r'^display_user_course', 'DueLink.views.display_user_course', name='display_user_course'),
    url(r'^subscribe_course', 'DueLink.views.subscribe_course', name='subscribe_course'),
    url(r'^unsubscribe_course', 'DueLink.views.unsubscribe_course', name='unsubscribe_course'),

    # # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'edit-profile$', 'DueLink.views.edit_profile', name='edit_profile'),
    # url(r'manage-course$', 'DueLink.views.manage_course', name='manage_course'),

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

    url(r'^link/(?P<user_id>\d+)$', 'DueLink.views.link', name='link'),
    url(r'^unlink/(?P<user_id>\d+)$', 'DueLink.views.unlink', name='unlink'),
    url(r'^search_people$', 'DueLink.views.search_people', name='search_people'),
    url(r'^search_course$', 'DueLink.views.search_course', name='search_course'),
    # Admin pages for user with special permissions
        url(r'^admin/publish_deadline$', 'DueLink.views_admin.publish_deadline', name='publish_deadline'),
    url(r'^admin/delete_course$', 'DueLink.views_admin.delete_course', name='delete_course'),
    url(r'^admin/add_course$', 'DueLink.views_admin.add_course', name='add_course'),
    url(r'^admin/add_section$', 'DueLink.views_admin.add_section', name='add_section'),
    url(r'^admin/manage_course$', 'DueLink.views_admin.manage_course', name='manage_course'),

    url(r'^admin/add_school$', 'DueLink.views_admin.add_school', name='add_school'),
    # url(r'^admin/delete_school$', 'DueLink.views_admin.delete_school', name='delete_school'),

    url(r'^admin/admin_get$', 'DueLink.views_admin.admin_get'),
     url(r'^add_team$', 'DueLink.views.add_team', name="add_team"),
    url(r'^add_member/(?P<team_id>\d+)$', 'DueLink.views.add_member', name='add_member'),
    url(r'^remove_member/(?P<team_id>\d+)$', 'DueLink.views.remove_member', name='remove_member'),
    url(r'^get_team_list$', 'DueLink.views.get_team_list', name='get_team_list'),
    url(r'^get_team_stream$', 'DueLink.views.get_team_stream', name='get_team_stream'),
    url(r'^get_team_stream/(?P<team_id>\d+)$','DueLink.views.get_team_stream_by_id', name='get_team_stream_by_id'),
    url(r'^add_event_team/(?P<team_id>\d+)$','DueLink.views.add_event_team', name = 'add_event_team')
]
