# A simple video membership website built with Django.

This project shows how to create a video membership website using Django and Stripe billing.

## Getting Started

Create a stripe account and put your stripe publishable key and secret key inside `settings.py` as well as your publishable key inside `checkout.js` in the static folder. Follow the [tutorial](https://youtu.be/zu2PBUHMEew) for guidance.

**Note** that you will need to create your own Stripe plans in your dashboard and link those plan ID's in your Django admin.

[![alt text](https://github.com/justdjango/video-membership/blob/master/thumbnail.png "Logo")](https://youtu.be/zu2PBUHMEew)

## Latest update of the code

Stripe changed their API to no longer allow a source being passed into a subscription. The code has been updated to now correctly bill a customer.

## Where to find us

Like us on [Facebook](https://www.facebook.com/justdjangocode/)

Follow us on [Instagram](https://www.instagram.com/justdjangocode/)

Subscribe to our [YouTube](https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ) Channel

Or visit our [Website](https://www.justdjango.com)