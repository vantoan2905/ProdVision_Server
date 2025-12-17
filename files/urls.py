from django.urls import path
from files.views import (
    ImageProcessingView,
    HistoryFilesView,
    ProcessPDFView,
)

urlpatterns = [
    path('process-image/', ImageProcessingView.as_view(), name='process-image'),
    path('process-pdf/', ProcessPDFView.as_view(), name='process-pdf'),
    path('load-files/', HistoryFilesView.as_view(), name='load-files'),

]
