# encoding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.widget import DatePickerInput

from localflavor.generic.forms import DateField
from localflavor.fr.forms import FRZipCodeField as OriginalFRZipCodeField
from localflavor.fr.forms import FRPhoneNumberField as OriginalFRPhoneNumberField


class FRDateField(DateField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = DatePickerInput(
                format="%d/%m/%Y", 
                attrs={'placeholder': 'jj/mm/aaaa'})
        super(FRDateField, self).__init__(*args, **kwargs)


class FRZipCodeField(OriginalFRZipCodeField):
    default_error_messages = {
        'invalid': _(u"Enterez un code postal au format XXXXX."),
    }

    def __init__(self, max_length=5, min_length=5, *args, **kwargs):
        super(FRZipCodeField, self).__init__(*args, **kwargs)
        self.label = _('Code postal')

class FRPhoneNumberField(OriginalFRPhoneNumberField):
    default_error_messages = {
        'invalid': _(u"Le numéro de téléphone doit correspondre au format 0X XX XX XX XX."),
    }