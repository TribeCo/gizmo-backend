from django.urls import path
from .views import CreateBannerAPIView,DeleteBannerAPIView,UpdateBannerAPIView,ReadBannerBySlugAPIView
#---------------------------
urlpatterns = [
    path('banners/create/', CreateBannerAPIView.as_view(), name='create_banner'),
    path('banners/delete/<int:banner_id>/', DeleteBannerAPIView.as_view(), name='delete_banner'),
    path('banners/update/<int:banner_id>/', UpdateBannerAPIView.as_view(), name='update_banner'),
    path('banners/read/<slug:slug>/', ReadBannerBySlugAPIView.as_view(), name='read_banner'),

]

