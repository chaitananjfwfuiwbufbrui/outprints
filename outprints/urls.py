from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from authentications import views
from django.contrib import admin
from django.urls import path
admin.autodiscover()
admin.site.enable_nav_sidebar = False

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from authentications.views import *


schema_view = get_schema_view(
  openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
  ),
  public=True,
  permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('Auth/GoogleRedirect/', RedirectSocial.as_view()),
    path('swagger/s.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('superuser/', superuser.as_view(), name='superuser'),
    path('admin/', admin.site.urls),
    path('main/', include('home.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    # path('auth/login/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('superuser/', views.superuser.as_view(), name='token_obtain_pair'),
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+ static(settings.IMAGES_URL,document_root=settings.IMAGES_ROOT)
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]