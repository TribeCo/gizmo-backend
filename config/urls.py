from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation for Gizmo",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="Taham8000@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('layout.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('inquiry.urls')),
    path('api/', include('cart.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
