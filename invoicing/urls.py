from django.urls import path, include

urlpatterns = [
    path('v1/', include('invoicing.api.v1.urls')),
]
