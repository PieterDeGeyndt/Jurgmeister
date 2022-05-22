from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import homepage.views
import cocktails.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage.views.home, name='home'),
    path('services/',include('services.urls')),
    path('cocktails/',include('cocktails.urls')),
    path('accounts/', include('allauth.urls')),
    path('instagram/',homepage.views.instagram, name='instagram'),
    path('info/',homepage.views.info, name='info'),
    path('accounts/profile/', cocktails.views.your_account, name='account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
