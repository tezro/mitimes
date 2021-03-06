from django.contrib.auth.models import User
from django.db import models

from annoying.fields import AutoOneToOneField
from south.modelsinspector import add_introspection_rules


class ChargeRate(models.Model):
    profile = models.ForeignKey("Profile",)
    is_default = models.BooleanField(default=False,)
    description = models.CharField(max_length=100,)
    per_hour = models.DecimalField(max_digits=10, decimal_places=2,)
    
    def __unicode__(self):
        return "%s, $%s per hour" % (self.description, self.per_hour)

    @staticmethod
    def get_rate_per_unit():
        """
        Returns rate per one unit according to global units per hour setting.
        """
        pass

class Client(models.Model):
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50,)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class ContactPhone(models.Model):
    contact = models.ForeignKey("Contact", related_name='phones')
    phone = models.CharField(max_length=20,)

    def __unicode__(self):
        return self.phone

class ContactEmail(models.Model):
    contact = models.ForeignKey("Contact", related_name='emails')
    email = models.EmailField(max_length=300,)

    def __unicode__(self):
        return self.email

class Contact(models.Model):
    profile = models.ForeignKey("Profile",)
    is_active = models.BooleanField(default=True,)
    charge_rate = models.ForeignKey(ChargeRate,)
    default_name = models.CharField(max_length=200,)
    first_name = models.CharField(max_length=50, blank=True,)
    last_name = models.CharField(max_length=50, blank=True,)
    
    def __unicode__(self):
        if self.first_name or self.last_name:
            if self.last_name:
                return "%s %s" % (self.first_name, self.last_name)
            return self.first_name
        return self.default_name
    
    @staticmethod
    def get_active_for_user(user):
        """
        Returns all active contacts for user.
        """
        return Contact.objects.filter(profile__user=user, is_active=True,)
    
    @staticmethod
    def get_inactive_for_user(user):
        """
        Returns all inactive contacts for user.
        """
        return Contact.objects.filter(profile__user=user, is_active=False,)

TIME_ZONES = (
    ('Adelaide', 'Adelaide'),
    ('Melbourne', 'Melbourne'),
    ('Lord_Howe', 'Lord Howe'),
    ('Perth', 'Perth'),
    ('Currie', 'Currie'),
    ('Broken_Hill', 'Broken Hill'),
    ('Lindeman', 'Lindeman'),
    ('Sydney', 'Sydney'),
    ('Eucla', 'Eucla'),
    ('Darwin', 'Darwin'),
    ('Brisbane', 'Brisbane'),
    ('Hobart', 'Hobart'),
)
add_introspection_rules([], ["^annoying\.fields\.AutoOneToOneField"])

class Profile(models.Model):
    user = AutoOneToOneField(User, primary_key=True,)
    activation_key = models.CharField(max_length=40, blank=True,)
    time_zone = models.CharField(max_length=50, choices=TIME_ZONES,)
    organisation = models.CharField(max_length=100, blank=True,)

    def __unicode__(self):
        return 'Profile for %s' % self.user
