from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from .utils import send_email

class MyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_username, user_email, user_field

        data = form.initial_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user


    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        host = str(request.get_host()).split(":", 1)[0]
        if 'api' in host:
            host = host.replace("api", "www")
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            "request": request,
            "host": host,
            "is_secure": request.is_secure()
        }

        if signup:
            email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)


    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed on the db
        """
        email_address.verified = True
        email_address.set_as_primary(conditional=True)
        email_address.save()

        # Inform admins that a new email was verified (a new user just registered)
        admin_users = User.objects.filter(is_superuser = True).values('email')
        admin_users_list = list(admin_users)
        admin_email_list = [d['email'] for d in admin_users_list]
        if 'admin@example.com' in admin_email_list: admin_email_list.remove('admin@example.com')

        emaildata = {
            'newuser': email_address.user,
            'mailing_list': admin_email_list,
            'subject': 'New user registered'
        }

        send_email(emaildata, 'newregistration_email')
