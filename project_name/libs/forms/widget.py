import re
import os
import logging

from django.conf import settings
from django import forms
from django.template import Context
from django.forms.widgets import FileInput as OriginalFileInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.util import flatatt

from sorl.thumbnail.shortcuts import get_thumbnail

logger = logging.getLogger(__name__)


class FileInput(OriginalFileInput):
    """
    Widget prodiving a input element for file uploads based on the
    Django ``FileInput`` element. It hides the actual browser-specific
    input element and shows the available image for images that have
    been previously uploaded. Selecting the image will open the file
    dialog and allow for selecting a new or replacing image file.
    """
    template_name = 'partials/file_input_widget.html'
    attrs = {'accept': 'file/*'}

    original_filename = None

    def render(self, name, value, attrs=None):
        """
        Render the ``input`` field based on the defined ``template_name``. The
        image URL is take from *value* and is provided to the template as
        ``image_url`` context variable relative to ``MEDIA_URL``. Further
        attributes for the ``input`` element are provide in ``input_attrs`` and
        contain parameters specified in *attrs* and *name*.
        If *value* contains no valid image URL an empty string will be provided
        in the context.
        """
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        file_url = final_attrs.get('value', '')
        file_original_url = None
        file_name = self.original_filename
        if not file_name and file_url:
            file_original_url = os.path.join(settings.MEDIA_URL, file_url)
            file_name = os.path.basename(file_url)
        
        return render_to_string(self.template_name, Context({
            'input_attrs': flatatt(final_attrs),
            'file_url': file_url,
            'file_name': file_name,
            'file_original_url': file_original_url,
            'file_id': "%s-file" % final_attrs['id'],
        }))


class ImageInput(OriginalFileInput):
    """
    Widget prodiving a input element for file uploads based on the
    Django ``FileInput`` element. It hides the actual browser-specific
    input element and shows the available image for images that have
    been previously uploaded. Selecting the image will open the file
    dialog and allow for selecting a new or replacing image file.
    """
    template_name = 'partials/image_input_widget.html'
    attrs = {'accept': 'image/*'}

    def render(self, name, value, attrs=None):
        """
        Render the ``input`` field based on the defined ``template_name``. The
        image URL is take from *value* and is provided to the template as
        ``image_url`` context variable relative to ``MEDIA_URL``. Further
        attributes for the ``input`` element are provide in ``input_attrs`` and
        contain parameters specified in *attrs* and *name*.
        If *value* contains no valid image URL an empty string will be provided
        in the context.
        """
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        image_url = final_attrs.get('value', '')
        image_original_url = None
        image_thumb = None
        if image_url:
            image_original_url = os.path.join(settings.MEDIA_URL, image_url)
            try:
                image_thumb = get_thumbnail(image_url, '100x100', crop='center', upscale=True)
            except IOError as inst:
                logger.error(inst)
        
        return render_to_string(self.template_name, Context({
            'image_thumb': image_thumb,
            'input_attrs': flatatt(final_attrs),
            'image_url': image_url,
            'image_original_url': image_original_url,
            'image_id': "%s-image" % final_attrs['id'],
        }))


def datetime_format_to_js_date_format(format):
    """
    Convert a Python datetime format to a date format suitable for use with JS
    date pickers
    """
    converted = format
    replacements = {
        '%Y': 'yy',
        '%m': 'mm',
        '%d': 'dd',
        '%H:%M': '',
    }
    for search, replace in replacements.iteritems():
        converted = converted.replace(search, replace)
    return converted.strip()


def datetime_format_to_js_time_format(format):
    """
    Convert a Python datetime format to a time format suitable for use with JS
    date pickers
    """
    converted = format
    replacements = {
        '%Y': '',
        '%m': '',
        '%d': '',
        '%H': 'HH',
        '%M': 'mm',
    }
    for search, replace in replacements.iteritems():
        converted = converted.replace(search, replace)

    converted = re.sub('[-/][^%]', '', converted)

    return converted.strip()


def add_js_formats(widget):
    """
    Set data attributes for date and time format on a widget
    """
    attrs = {
        'data-dateFormat': datetime_format_to_js_date_format(
            widget.format),
        'data-timeFormat': datetime_format_to_js_time_format(
            widget.format)
    }
    widget.attrs.update(attrs)


class DatePickerInput(forms.DateInput):
    """
    DatePicker input that uses the jQuery UI datepicker.  Data attributes are
    used to pass the date format to the JS
    """
    def __init__(self, *args, **kwargs):
        super(DatePickerInput, self).__init__(*args, **kwargs)
        add_js_formats(self)


class DateTimePickerInput(forms.DateTimeInput):
    # Build a widget which uses the locale datetime format but without seconds.
    # We also use data attributes to pass these formats to the JS datepicker.

    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', False)
        super(DateTimePickerInput, self).__init__(*args, **kwargs)

        if not include_seconds:
            self.format = re.sub(':?%S', '', self.format)
        add_js_formats(self)
