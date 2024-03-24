from django.urls import path

from .views import *
from Statistika.views import *

urlpatterns = [
    path('photo/', PhotoList.as_view(), name='photo'),
    path('photoedit/<int:id>/', PhotoEditView.as_view(), name='photo_edit'),
    path('ish_turi/', Ish_TuriView.as_view(), name='ish_turi'),
    path('ish_turi/<int:id>/', Ish_TuriDetail.as_view(), name='ish_turi_detail'),
    path('bulim/', BolimView.as_view(), name='bulim'),
    path('bulim/<int:id>/', BolimDetail.as_view(), name='bulim_detail'),
    path('mahsulot/', MaxsulotView.as_view(), name='mahsulot'),
    path('mahsulot/<int:id>/', MaxsulotDetail.as_view(), name='mahsulot_detail'),
    path('xatolar/', ProblemView.as_view(), name='xatolar'),
    path('xatolar/<int:id>/', ProblemDetail.as_view(), name='xatolar_detail'),
    path('missed/', HisobotView.as_view(), name='missed'),
    path('missed/<int:id>/', HisobotDetail.as_view(), name='missed_detail'),

    path('statistics/', XodimStatistic.as_view(), name='statistics'),
]