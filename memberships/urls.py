from django.urls import path

from .views import (
	MembershipSelectView, 
	PaymentView, 
	updateTransactionRecords,
	profile_view)

app_name = 'memberships'

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/', updateTransactionRecords, name='update-transactions'),
    path('profile/', profile_view, name='profile')
]
