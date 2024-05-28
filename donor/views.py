from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import *
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels

def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST,request.FILES)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('donorlogin')
    return render(request,'donor/donorsignup.html',context=mydict)


def donor_dashboard_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    print(donor.id)

    dict={
        'requestpending': models.BloodDonate.objects.all().filter(id=donor.id).filter(status='Pending').count(),
        'requestapproved': models.BloodDonate.objects.all().filter(id=donor.id).filter(status='Approved').count(),
        'requestmade': models.BloodDonate.objects.all().filter(id=donor.id).count(),
        'requestrejected': models.BloodDonate.objects.all().filter(id=donor.id).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)


def donate_blood_view(request):
    try:
        donor=models.Donor.objects.get(user_id=request.user.id)
        donated=models.BloodDonate.objects.all().filter(donor=donor)
        for x in donated:
            a=x.after_donate_blood
        b=datetime.now().date()
        print(type(b))    
        if  b >= a:
            donation_form=forms.DonationForm()
            if request.method=='POST':
                donation_form=forms.DonationForm(request.POST)
                if donation_form.is_valid():
                    blood_donate=donation_form.save(commit=False)
                    blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
                    donor= models.Donor.objects.get(user_id=request.user.id)
                    blood_donate.donor=donor
                    blood_donate.save()
                    return HttpResponseRedirect('donation-history')  
            return render(request,'donor/donate_blood.html',{'donation_form':donation_form})
        else:
            return HttpResponseRedirect('donation-history')
    except:
        donation_form=forms.DonationForm()
        if request.method=='POST':
            donation_form=forms.DonationForm(request.POST)  
            if donation_form.is_valid():
                blood_donate=donation_form.save(commit=False)
                blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
                donor=models.Donor.objects.get(user_id=request.user.id)
                blood_donate.donor=donor
                blood_donate.save()
                return HttpResponseRedirect('donation-history')
        return render(request,'donor/donate_blood.html',{'donation_form':donation_form})
def update_donor_view(request):
    donor=models.Donor.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=donor.user_id)
    userForm=forms.DonorUserForm(instance=user)
    donorForm=forms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST,instance=user)
        donorForm=forms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.status=donorForm.cleaned_data['status']
            donor.save()
        return HttpResponseRedirect('donorlogin')
    return render(request,'donor/update_donor.html',context=mydict)
def donation_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})
"""
def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_request.request_by_donor=donor
            blood_request.save()
            return HttpResponseRedirect('request-history')  
    return render(request,'donor/makerequest.html',{'request_form':request_form})

def request_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})
"""