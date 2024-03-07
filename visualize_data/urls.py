from django.contrib import admin
from django.urls import path
from views import YolovModel, DataDetect, DetectResult

urlpatterns = [
    path('models/getModelOverview', ),
    path('models/getModelPerfor', ),
    path('data/selectDataPath', ),
    path('data/preAnalysis', ),
    path('data/startDetect', ),
    path('detect/status', ),
    path('dectect/result', ),
    path('dectect/samplesPath', ),
    path('dectect/getModelPerfor', ),
]
