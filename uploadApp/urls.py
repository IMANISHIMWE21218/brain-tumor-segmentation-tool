from django.urls import path

from .views import HomePageView, report, comment, upload

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('upload/', upload, name='upload'),
    path('report/', report, name='report'),
    path('<int:id>/comment', comment, name='comment'),
]
