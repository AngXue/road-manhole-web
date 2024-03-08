from django.contrib import admin
from django.urls import path
from views import *

urlpatterns = [
    path('models/getAvailableNames', get_available_names),
    path('models/selectModel', select_model),
    path('models/getModelOverview', get_model_overview),
    path('models/getModelPerfor', get_model_perfor),
    path('data/selectDataPath', select_data_path),
    path('data/preAnalysis', pre_analysis),
    path('data/startDetect', start_detect),
    path('detect/status', get_detect_status),
    path('dectect/result', get_detect_result),
    path('dectect/samplesPath', get_samples_path),
    path('dectect/getModelPerfor', get_detect_model_perfor),
]
