from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# these url patterns point to the different apps loaded on this set
urlpatterns = [
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    url(r'', include('cnnfgiapp.urls')),

]

