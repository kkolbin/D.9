from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls', namespace='news')),
    path('articles/', include('news.urls', namespace='articles')),
    path('accounts/', include('allauth.urls')),

]
