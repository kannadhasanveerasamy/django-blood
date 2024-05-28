from django.urls import path

from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html'),name='patientlogin'),
    path('patientsignup', views.patient_signup_view,name='patientsignup'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient/patient-dashboard'),
    path('patient-searchdonor',views.patient_search_donor,name='patient/patient-searchdonor'),
    path('donor-list',views.donor_list,name='patient/donor-list'),
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
    path('update-patient',views.update_patient_view,name='update-patient'),
]   