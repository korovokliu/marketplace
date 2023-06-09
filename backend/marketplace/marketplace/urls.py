from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls', namespace='products'))
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
