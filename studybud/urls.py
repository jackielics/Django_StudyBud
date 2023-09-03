from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('base.urls')), # take caer of all routing
	path('api/', include('base.api.urls')), # take caer of all routing
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)