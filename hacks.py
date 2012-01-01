import logging

from google.appengine.api.datastore import Query
from google.appengine.api import datastore

from .logger import log_call, time_call, CallTypes


def make_callable_loggable(original_callable, call_type):
    if original_callable.__name__ == 'replacement_callable':
        #Don't apply the patch more than once
        return original_callable
    logging.warning('patch applied %s', call_type)
    def replacement_callable(*args, **kwargs):
        time_taken, ret_val = time_call(original_callable, *args, **kwargs)
        log_call(call_type, time_taken, args, kwargs)
        return ret_val
    return replacement_callable



def apply_hacks():
    Query.Run = make_callable_loggable(Query.Run, CallTypes.QUERY)
    datastore.Get = make_callable_loggable(datastore.Get, CallTypes.GET)





