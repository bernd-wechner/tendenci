from builtins import str
from decimal import Decimal
import re
#from south.modelsinspector import add_introspection_rules

from django.forms import fields, ValidationError
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
import simplejson
from django.core import exceptions
from django_countries import countries as COUNTRIES
from localflavor.us.us_states import STATE_CHOICES, US_STATES
from localflavor.ca.ca_provinces import PROVINCE_CHOICES

from tendenci.apps.base import forms
from tendenci.apps.base.utils import custom_json_dumper
from tendenci.apps.base.widgets import EmailVerificationWidget, PercentWidget, PriceWidget
from tendenci.apps.site_settings.utils import get_setting


# # introspection rules for south migration for the slugfield
# add_introspection_rules([], [r'^tendenci\.apps\.base\.fields\.SlugField'])
# add_introspection_rules([], [r'^tendenci\.apps\.base\.fields\.DictField'])


class SlugField(CharField):
    """
        New slug field that uses a different set of validations
        Straight copy from django with modifications
    """
    description = _("String (up to %(max_length)s)")
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 100)
        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        super(SlugField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "SlugField"

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.SlugField}
        defaults.update(kwargs)
        return super(SlugField, self).formfield(**defaults)


class DictField(models.TextField):
    """
    A dictionary field
    """

    def to_python(self, value):
        if not value:
            return {}

        if isinstance(value, str):
            try:
                return simplejson.loads(value)
            except (ValueError, TypeError):
                raise exceptions.ValidationError(
                        self.error_messages['invalid'])

        if isinstance(value, dict):
            return value

        return {}

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if isinstance(value, dict):
            return simplejson.dumps(value, default=custom_json_dumper, indent=2)

        if isinstance(value, str):
            return value

        return ''


class EmailVerificationField(fields.MultiValueField):
    # widget = EmailVerificationWidget

    def __init__(self, attrs=None, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """

        all_fields = (
            fields.EmailField(max_length=75),
            fields.EmailField(max_length=75, label=_("Verfiy Email Address")),
            )
        label = kwargs.pop('label', '') + ' (Enter twice to verify)'
        label = _(label)
        super(EmailVerificationField, self).__init__(all_fields, widget=EmailVerificationWidget(attrs={'class': 'form-control'}), label=label, *args, **kwargs)

    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """
        if data_list:
            if not (data_list[0] and data_list[1]):
                raise ValidationError(_("Please enter the email twice to verify."))
            if data_list[0] != data_list[1]:
                raise ValidationError(_("Please enter the same email address."))
            email_data = "%s" % (data_list[0])
            return email_data
        return ''


class CountrySelectField(fields.ChoiceField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)

        initial_choices = ()
        exclude_list = []

        initial_choices_keys = get_setting('site', 'global', 'countrylistinitialchoices')
        if initial_choices_keys and initial_choices_keys != u'[]':
            initial_choices =  ((name, name) for key, name in list(COUNTRIES) if key in initial_choices_keys)
            exclude_list = initial_choices_keys

        initial_choices = tuple(initial_choices) + (('','-----------'),)
        countries = ((name,name) for key,name in list(COUNTRIES) if key not in exclude_list)
        self.choices = initial_choices + tuple(countries)
        self.initial = ''


class StateSelectField(fields.ChoiceField):
    def __init__(self, *args, app_name='', label="", **kwargs):
        empty_label = kwargs.pop('empty_label', '-----------')
        self.max_length = kwargs.pop('max_length', 50)
        self.app_name = app_name
        if get_setting('site', 'global', 'stateusesregion'):
            label = get_setting('module', 'regions', 'label')
        super(StateSelectField, self).__init__(*args, label=label, **kwargs)
        from tendenci.apps.regions.models import Region
        if get_setting('site', 'global', 'stateusesregion'):
            regions = Region.objects.filter(status_detail='active').order_by('position')
            regions_to_exclude = [int(region_id) for region_id in settings.ALTERNATIVE_REGIONS_MAP.keys()]
            if regions_to_exclude and self.app_name not in ['memberships', 'corporate_memberships']:
                regions = regions.exclude(id__in=regions_to_exclude)

            choices = (('',empty_label),) +tuple((region.region_name, region.region_name) for region in regions)
        else:
            if get_setting('site', 'global', 'usstatesonly'):
                choices = (('',empty_label),) + tuple((state, state_f.title()) for state, state_f in US_STATES)
            else:
                choices = (('',empty_label),) + tuple((state, state_f.title()) for state, state_f in STATE_CHOICES) \
                    + tuple((prov, prov_f.title()) for prov, prov_f in PROVINCE_CHOICES)
            choices = sorted(choices)
            # add non-us
            choices = choices + [('Non-US', _('Non-US')),]
        self.choices = choices
        self.initial = ''


class PriceField(fields.DecimalField):

    def __init__(self, max_value=None, min_value=None, max_digits=None, decimal_places=None, *args, **kwargs):
        super(PriceField, self).__init__(*args, max_value=max_value, min_value=min_value, max_digits=max_digits, decimal_places=decimal_places, **kwargs)
        self.widget = PriceWidget()

    def clean(self, value):
        comma_setting = get_setting('site', 'global', 'allowdecimalcommas')
        if comma_setting and value is not None and ',' in value:
            comma_validator = re.compile(r'^[0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?$')
            if comma_validator.match(value):
                value = re.sub(r',', '', value)
            else:
                raise ValidationError(self.error_messages['invalid'])

        return super(PriceField, self).clean(value)


class PercentField(fields.DecimalField):
    """
    Accepts value between 0 and 1 and displays it between 0 and 100
    """
    widget = PercentWidget()
    default_error_messages = {
        'out_of_range': _('Must be between 0 and 100'),
        'whole_number': _('Must be a whole number'),
        'decimal_places': _('Only {decimal_places} decimal place(s) allowed')
    }

    def __init__(self, allowed_decimal_places = None, *args, **kwargs):
        # Optionally specify how many decimal places are allowed.
        self.allowed_decimal_places = allowed_decimal_places
        # Track if errors occurred (Used to display values correctly on error)
        self.error_occurred = False
        # Track raw input from user (Used to display values correctonly on error)
        self.raw_input = None

        super(PercentField, self).__init__(*args, **kwargs)

    @property
    def decimal_validation_error(self):
        """Error message to display if decimal validation fails"""
        if not self.allowed_decimal_places:
            return self.error_messages['whole_number']

        return self.error_messages['decimal_places'].format(
            decimal_places=self.allowed_decimal_places)

    def to_python(self, value):
        """Save percent as decimal number"""
        value = super(PercentField, self).to_python(value)
        return Decimal("%.2f" % (float(value) / 100.0))

    def prepare_value(self, value):
        """Display as whole number"""
        value = super(PercentField, self).prepare_value(value) or 0

        # Display invalid values in a way expected by user.
        if self.error_occurred:
            return self.raw_input

        return str(int(value * 100))

    def raise_validation_error(self, error_message):
        """Track error occurred and raise ValidationError"""
        self.error_occurred = True
        raise ValidationError(error_message)

    def validate_decimal_places(self):
        """Validate input conforms to allowed decimal places"""
        if self.allowed_decimal_places is None:
            return

        value = Decimal(self.raw_input)
        decimal_places = abs(value.as_tuple().exponent)

        if decimal_places > self.allowed_decimal_places:
            self.raise_validation_error(self.decimal_validation_error)

    def clean(self, value):
        """
        Validate value is between 0 and 1 and that value
        follows rules for allowed decimal places.
        """
        # Track raw input in order to display value correctly in case of error.
        self.raw_input = value

        try:
            value = super(PercentField, self).clean(value)
        except Exception as e:
            self.raise_validation_error(e.args[0])

        if value is None:
            return 0

        self.validate_decimal_places()

        if (value < 0 or value > 1):
            self.raise_validation_error(self.error_messages['out_of_range'])

        return value
