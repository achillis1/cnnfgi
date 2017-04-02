from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from cnnfgiapp import views

urlpatterns = [
    url(r'^$',          views.main.index,              name='index'),
    url(r'^login/',     auth_views.login,              name='login'),
    url(r'^logout/',    auth_views.logout_then_login,  name='logout'),

    url(r'^user-account/password/reset/$', views.miscellaneous.password_reset,
            {'extra_context': {'base_url': settings.BASE_URL},
             'post_reset_redirect': '/user-account/password/reset/done/',
             'html_email_template_name': 'registration/password_reset_email.html'},
            name="password_reset"),
    url(r'^user-account/password/reset/done/$', auth_views.password_reset_done),
    url(r'^user-account/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm,
            {'post_reset_redirect' : '/user-account/password/done/'}, name='password_reset_confirm'),
    url(r'^user-account/password/done/$', auth_views.password_reset_complete),

    # fgi index

]

