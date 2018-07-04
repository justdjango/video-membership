from django.urls import path

from .views import MembershipSelectView

app_name = 'memberships'

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
]
