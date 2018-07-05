from django.urls import path

from .views import MembershipSelectView, PaymentView

app_name = 'memberships'

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment', PaymentView, name='payment')
]
