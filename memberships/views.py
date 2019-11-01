from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse

from .models import Membership, UserMembership, Subscription

import stripe

def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

@login_required
def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    return render(request, "memberships/profile.html", context)


class MembershipSelectView(LoginRequiredMixin, ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_type = request.POST.get('membership_type')

        selected_membership = Membership.objects.get(
            membership_type=selected_membership_type)

        if user_membership.membership == selected_membership:
            if user_subscription is not None:
                messages.info(request, """You already have this membership. Your
                              next payment is due {}""".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))

@login_required
def PaymentView(request):
    user = request.user
    try:
        address = profile.address.get(address_type="home")
    except:
        address = None
    user_membership = get_user_membership(request)
    try:
        selected_membership = get_selected_membership(request)
    except:
        return redirect(reverse("memberships:select"))
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        # try:
        source = request.POST.get('stripeSource', "")
        amend = request.POST.get('amend', '')

        '''
        First we need to add the source for the customer
        '''
        if amend == "true":
            customer = stripe.Customer.modify(
                user_membership.stripe_customer_id,
                source=source,
            )
            customer.save()
        else:
            customer = stripe.Customer.retrieve(
                user_membership.stripe_customer_id)

            try:
                customer.source = source  # 4242424242424242
                customer.save()
            except:
                messages.warning(
                    request, "Your card has been failed or declined, Please try a different card")
                context = {
                    'publishKey': publishKey,
                    'selected_membership': selected_membership,
                    'address': address,
                    'profile': profile,
                    'amend': "true"
                }
                return render(request, "membership/membership_payment.html", context)

        '''
        before we make any subscriptions, we need to make sure there isn't any current active subscriptions for the customer.
        Without this, we could get duplicates payment
        We first fetch the customer to make sure we have the latest update
        '''
        customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
        if customer.subscriptions.total_count > 0:
            for i in customer.subscriptions.data:
                if i.plan['id'] == selected_membership.stripe_plan_id and i.plan['active'] == True:
                    messages.info(
                        request, "Your have already subscribed to this plan")
                    return redirect(reverse('memberships:update-transactions',
                                            kwargs={
                                                'subscription_id': i.id
                                            }))
                else:
                    pass  # Maybe we can check if users have a subscription that needs renewing
        else:
            '''
            Now we can create the subscription using only the customer as we don't need to pass their
            credit card source anymore
            '''

            stripe_subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {"plan": selected_membership.stripe_plan_id},
                ],
                # billing="charge_automatically", #billing is depricated
                collection_method="charge_automatically",
                # idempotency_key='FXZMav7BbtEui1Z3', # we can add a random idempotency key too
            )
            '''
            Here we check three different status of the subscription object according to API and if
            secure 3D payment is required, we redirect them for the necessary payments.
            '''
            if stripe_subscription.status == "active":
                return redirect(reverse('memberships:update-transactions',
                                        kwargs={
                                            'subscription_id': stripe_subscription.id
                                        }))
            elif stripe_subscription.status == "incomplete":
                payment_intent = stripe_subscription.latest_invoice.payment_intent
                if payment_intent.status == "requires_action":
                    messages.info(
                        request, "Your bank requires extra authentication")
                    context = {
                        "client_secret": payment_intent.client_secret,
                        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY,
                        "subscription_id": stripe_subscription.id
                    }
                    return render(request, "memberships/3d-secure-checkout.html", context)
                elif payment_intent.status == "requires_payment_method":
                    messages.warning(
                        request, "Your card has been failed or declined, Please try a different card")
                    context = {
                        'publishKey': publishKey,
                        'selected_membership': selected_membership,
                        # 'client_secret': client_secret,
                        'address': address,
                        'profile': profile,
                        'amend': "true"
                    }
                    return render(request, "memberships/membership_payment.html", context)
                else:
                    messages.info(
                        request, "Something went wrong. Please report to the website admin.")

    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership,
        # 'client_secret': client_secret,
        'address': address,
        'user': user,
        'amend': "false"
    }

    return render(request, "memberships/membership_payment.html", context)

@login_required
def updateTransactionRecords(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, 'Successfully created {} membership'.format(
        selected_membership))
    return redirect(reverse('memberships:select'))

@login_required
def cancelSubscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.get(membership_type='Free')
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()

    messages.info(
        request, "Successfully cancelled membership. We have sent an email")
    # sending an email here

    return redirect(reverse('memberships:select'))
