from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='PSDApp/index.html')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('celery_progress/', include('celery_progress.urls'))

]
