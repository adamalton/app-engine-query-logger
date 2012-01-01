import logging
from time import time

from google.appengine.api import memcache

class CallTypes:
    QUERY = 'QUERY'
    GET = 'GET'
    
    def __setattr__(self, *args, **kwargs):
        raise AttributeError("You can't set values on this.")



def time_call(kallable, *args, **kwargs):
    """ Call a callable and time how long it takes. """
    start = time()
    ret_val = kallable(*args, **kwargs)
    time_taken = time() - start
    return time_taken, ret_val


def log_call(typ, time_taken, call_args, call_kwargs):
    """ Log a call to datastore.Get or datastore.Query.Run. """
    stats = make_stats(typ, time_taken, call_args, call_kwargs)
    logging.info(stats)



def make_stats(typ, time_taken, call_args, call_kwargs):
    """ Given a CallTypes, the time taken to call it and the
        args and kwargs that were passed to it when it was
        called, return a nice dict of useful info about the call.
    """
    log = {}
    log['time taken'] = time_taken
    log['type'] = typ
    if typ == CallTypes.QUERY:
        query = call_args[0] #aka self
        log['kind'] = query._Query__kind
        filters = call_kwargs #any filters that were passed to the Run method
        filters.update(dict(query.items())) #Any filters that had already been applied to the Query object
        log['filters'] = filters
    elif typ == CallTypes.GET:
        #Get() can either take a single key or a list of keys
        try:
            key = call_args[0][0]
        except TypeError:
            key = call_args[0]
        log['kind'] = key.kind()
        log['filters'] = {'id': key.id(), 'name': key.name()}
    return log




