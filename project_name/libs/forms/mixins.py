# encoding: utf-8

from django.conf import settings
from django import forms
from django.template import loader
from django.core.mail.message import EmailMessage
from django.utils.translation import ugettext_lazy as _


class OwnerFormMixin(object):
    required_owner = True

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        if self.required_owner and not owner:
            raise ValueError("the `owner` key-value argument was not found")

        self.owner = owner
        super(OwnerFormMixin, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(OwnerFormMixin, self).clean()

        # check for ownership
        # NB: check for `owner_id` before `owner` because at this step the
        #     owner can be None because of a new instance being created
        #     but the database won't allow a null relationship
        instance = getattr(self, 'instance', None)
        if instance and instance.owner_id:
            # object ownership
            if self.required_owner and instance.owner != self.owner:
                raise forms.ValidationError("User '%s' is not the owner of this object '%s'" % (self.owner, type(instance)))

            # related objects ownership
            for field in instance._meta.fields:
                if field.rel and field.name != 'owner' and 'owner' in field.rel.to._meta.get_all_field_names():
                    rel_data = cleaned_data.get(field.name)
                    # print cleaned_data
                    if rel_data and rel_data.owner != self.owner: 
                        raise forms.ValidationError("User '%s' is not the owner of this object '%s'" % (self.owner, field.rel.to))

        return cleaned_data

    def save(self, *args, **kwargs):
        # check compatibility
        if not hasattr(self, 'owner'):
            raise TypeError("the form class '%s' does not have an `owner` "
                "property defined" % type(self))

        if self.required_owner and not getattr(self, 'owner'):
            raise ValueError("the `owner` property defined is evaluated "
                "as `False`: '%s'" % getattr(self, 'owner'))

        original_commit_kwarg = kwargs.get('commit', True)
        kwargs['commit'] = False
        obj = super(OwnerFormMixin, self).save(*args, **kwargs)

        obj.owner = self.owner
        if original_commit_kwarg:
            obj.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
        return obj


class SendMailFormMixin(object):
    from_email = settings.DEFAULT_FROM_EMAIL

    def get_from_email(self):
        return self.from_email

    def get_context(self):
        """
        Context sent to templates for rendering include the form's cleaned
        data and also the current Request object.
        """
        if not self.is_valid():
            raise ValueError("Cannot generate Context when form is invalid.")
        return dict(**self.cleaned_data)

    def get_recipient_list(self):
        raise NotImplementedError

    def get_subject(self):
        return _(u"CBien.com")

    def get_message(self):
        raise NotImplementedError

    def get_message_dict(self):
        message_dict = {
            "from_email": self.get_from_email(),
            "to": self.get_recipient_list(),
            "subject": self.get_subject(),
            "body": self.get_message(),
        }
        return message_dict

    def send_email(self, fail_silently=False):
        return EmailMessage(**self.get_message_dict()).send(fail_silently=fail_silently)


class BaseSendMailForm(SendMailFormMixin, forms.Form):
    emails = forms.CharField(label=_(u"Adresses emails"), required=True)
    body = forms.CharField(label=_(u"Message"), widget=forms.Textarea())

    def get_recipient_list(self):
        ctx = self.get_context()
        return map(lambda s: s.strip(), ctx['emails'].split(','))

    def get_message(self):
        ctx = self.get_context()
        return ctx['body']


class ContactFormMixin(SendMailFormMixin):
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.DEFAULT_FROM_EMAIL]

    message_template_name = "mail/contact_body.txt"

    def get_recipient_list(self):
        return self.recipient_list

    def get_message(self):
        return loader.render_to_string(self.message_template_name, self.get_context())


class BaseContactForm(ContactFormMixin, forms.Form):
    body = forms.CharField(label=_(u"Message"), widget=forms.Textarea())
