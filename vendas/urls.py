from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib import admin

from vendas.users import views
from vendas.core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vendas.core.urls', namespace='core')),
    path('account/',include('vendas.users.urls')),
    path('cadastro/',include('vendas.cadastro.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
