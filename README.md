<p align="center">
  <p align="center">
    <a href="https://justdjango.com/?utm_source=github&utm_medium=logo" target="_blank">
      <img src="https://assets.justdjango.com/static/branding/logo.svg" alt="JustDjango" height="72">
    </a>
  </p>
  <p align="center">
    The Definitive Django Learning Platform.
  </p>
</p>

### *** Deprecation Warning ***

This project is over two years old and is outdated. You can find the new version of this project [here](https://github.com/justdjango/dj-video-membership)

# Video Membership Website

This project shows how to create a video membership website using Django and Stripe billing.

## Getting Started

Create a stripe account and put your stripe publishable key and secret key inside `settings.py` as well as your publishable key inside `checkout.js` in the static folder. Follow the [tutorial](https://youtu.be/zu2PBUHMEew) for guidance.

**Note** that you will need to create your own Stripe plans in your dashboard and link those plan ID's in your Django admin.

<p align="center">
  <a href="https://youtu.be/zu2PBUHMEew"><img src="https://github.com/justdjango/video-membership/blob/master/thumbnail.png" width="290"></a>
</p>

## Latest update of the code

Stripe changed their API to no longer allow a source being passed into a subscription. The code has been updated to now correctly bill a customer.

---

<div align="center">

<i>Other places you can find us:</i><br>

<a href="https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ" target="_blank"><img src="https://img.shields.io/badge/YouTube-%23E4405F.svg?&style=flat-square&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.twitter.com/justdjangocode" target="_blank"><img src="https://img.shields.io/badge/Twitter-%231877F2.svg?&style=flat-square&logo=twitter&logoColor=white" alt="Twitter"></a>

</div>
