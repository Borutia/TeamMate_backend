from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework_extensions.routers import NestedRouterMixin

from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework.routers import DefaultRouter

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


schema_view = get_schema_view(
   openapi.Info(
      title="TeamMateAPI",
      default_version='v1',
      description="API TeamMate",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('apiauth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
