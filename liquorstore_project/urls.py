from django.contrib import admin
from django.urls import path
from shop import views  # import your app views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),          # ✅ This is the fix
    path('home/', views.home, name='home'),
]

# Static and media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
