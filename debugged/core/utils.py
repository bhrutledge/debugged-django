import re
import types

from django.conf import settings
from django.utils import dateformat
from django.core import exceptions
from django.utils.importlib import import_module
from django.db.models import Model

def replace_date(source, format, date_value):
    date_string = str(dateformat.format(date_value, format[1:-1]))
    return source.replace(format, date_string, 1)

def format_dates(start_date, end_date=None):
    if not end_date or end_date <= start_date:
        return dateformat.format(start_date, settings.DATE_FORMAT)

    format = settings.DATE_RANGE_YEAR_FORMAT

    if start_date.year == end_date.year:
        format = settings.DATE_RANGE_MONTH_FORMAT

        if start_date.month == end_date.month:
            format = settings.DATE_RANGE_DAY_FORMAT
    
    m = re.search("(\(.*?\)).*(\(.*?\))", format)
    
    format = replace_date(format, m.group(1), start_date)
    format = replace_date(format, m.group(2), end_date)

    return unicode(format)

def get_module_attr(attr_path):
    try:
        dot = attr_path.rindex('.')
    except ValueError:
        raise exceptions.ImproperlyConfigured, '%s isn\'t a valid path' % attr_path

    module_name, attr_name = attr_path[:dot], attr_path[dot + 1:]
    try:
        mod = import_module(module_name)
    except ImportError, e:
        raise exceptions.ImproperlyConfigured, 'Error importing module %s: "%s"' % (module_name, e)

    try:
        attr = getattr(mod, attr_name)
    except AttributeError:
        raise exceptions.ImproperlyConfigured, 'Module "%s" does not define a "%s" attribute' % (module_name, attr_name)

    return attr

def get_model(model_path):
    model_class = get_module_attr(model_path)

    if not issubclass(model_class, Model):
        raise exceptions.ImproperlyConfigured, '%s isn\'t a model' % attr_name

    return model_class

def get_callback(callback_path):
    callback = get_module_attr(callback_path)
    
    if not isinstance(callback, types.FunctionType):
        raise exceptions.ImproperlyConfigured, '%s isn\'t a function' % attr_name
        
    return callback
