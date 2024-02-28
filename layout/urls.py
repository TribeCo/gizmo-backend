from django.urls import path
from .views import CreateBannerAPIView,DeleteBannerAPIView,UpdateBannerAPIView,ReadBannerBySlugAPIView,CreateFAQGroupAPIView,ReadFAQGroupAPIView,UpdateFAQGroupAPIView,DeleteFAQGroupAPIView,CreateFAQAPIView,ReadFAQAPIView,UpdateFAQAPIView,DeleteFAQAPIView
from .views import *
#---------------------------
urlpatterns = [
    path('banners/create/', CreateBannerAPIView.as_view(), name='create_banner'),
    path('banners/delete/<int:banner_id>/', DeleteBannerAPIView.as_view(), name='delete_banner'),
    path('banners/update/<int:banner_id>/', UpdateBannerAPIView.as_view(), name='update_banner'),
    path('banners/read/<slug:slug>/', ReadBannerBySlugAPIView.as_view(), name='read_banner'),
    path('picture/', PictureCreateAPIView.as_view(),name="picture_create"),
    path('picture/<int:pk>/', PictureDetailView.as_view(),name="picture_read"),
    path('picture/all/', PictureAllListAPIView.as_view(),name="picture_read_all"),
    path('picture/update/<int:pk>/', PictureUpdateView.as_view(),name="picture_update"),
    path('picture/delete/<int:pk>/', PictureDeleteView.as_view(),name="picture_delete"),
    path('faq_groups/create/', CreateFAQGroupAPIView.as_view(), name='create_faq_group'),
    path('faq_groups/read/', ReadFAQGroupAPIView.as_view(), name='read_faq_groups'),
    path('faq_groups/update/<int:pk>/', UpdateFAQGroupAPIView.as_view(), name='update_faq_group'),
    path('faq_groups/delete/<int:pk>/', DeleteFAQGroupAPIView.as_view(), name='update_faq_group'),
    path('faqs/create/', CreateFAQAPIView.as_view(), name='create_faq'),
    path('faqs/read/', ReadFAQAPIView.as_view(), name='read_faqs'),
    path('faqs/update/<int:pk>/', UpdateFAQAPIView.as_view(), name='update_faq'),
    path('faqs/delete/<int:pk>/', DeleteFAQAPIView.as_view(), name='delete_faq'),
]

