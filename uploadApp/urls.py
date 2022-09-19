from django.urls import path

from .views import HomePageView, report, comment, upload, pdf_report
from .import  views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('upload/', upload, name='upload'),
    path('report/', report, name='report'),
    path('pdf_report/', pdf_report, name='pdf_report'),
    path('about/', views.About, name='about'),
    path('<int:id>/comment', comment, name='comment'),
    path('single_report/<int:id>', views.single_report, name='single_report'),
    path('pdfsingle_report/<int:id>', views.pdfsingle_report, name='pdfsingle_report'),
]
