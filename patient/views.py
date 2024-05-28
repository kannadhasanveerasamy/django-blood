from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels
from donor import models as dmodels
import geocoder
def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'patient/patientsignup.html',context=mydict)

def patient_dashboard_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    current_location=geocoder.ip('me')
    city=str(current_location.city).capitalize()
    donor_list=dmodels.Donor.objects.filter(address=city).exclude(status='Unavailable')
    
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),
        'current_location':city,
        'current_lattitude':current_location.lat,
        'current_longitude':current_location.lng,
        'A1':bmodels.Stock.objects.get(bloodgroup="A+"),
        'A2':bmodels.Stock.objects.get(bloodgroup="A-"),
        'B1':bmodels.Stock.objects.get(bloodgroup="B+"),
        'B2':bmodels.Stock.objects.get(bloodgroup="B-"),
        'AB1':bmodels.Stock.objects.get(bloodgroup="AB+"),
        'AB2':bmodels.Stock.objects.get(bloodgroup="AB-"),
        'O1':bmodels.Stock.objects.get(bloodgroup="O+"),
        'O2':bmodels.Stock.objects.get(bloodgroup="O-"),

    }
    print(dict['A1'].unit)
    return render(request,'patient/patient_dashboard.html',context=dict)
def patient_search_donor(request):
    return render(request,'patient/patient-searchdonor.html')
def donor_list(request):
    data=request.POST['bloodgroup']
    #donor_list=dmodels.Donor.objects.all().filter(bloodgroup=data).values()
    donor_list=dmodels.Donor.objects.filter(bloodgroup=data).exclude(status="Unavailable")
    return render(request,'patient/donor-list.html',{"donor_list":donor_list})

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            patient= models.Patient.objects.get(user_id=request.user.id)
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'patient/makerequest.html',{'request_form':request_form})

def my_request_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})
def update_patient_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=patient.user_id)
    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            return HttpResponseRedirect('patientlogin')
    return render(request,'patient/update_patient.html',context=mydict)