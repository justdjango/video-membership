from django.shortcuts import render

from django.views.generic import ListView

from .models import Membership



class MembershipSelectView(ListView):
	model = Membership

	
