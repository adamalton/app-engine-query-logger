This is a simple app (hack) which logs all calls to the datastore (google.appengine.api.datastore).
It logs calls to datastore.Get and datastore.Query.Run.

For a Django project:
Simply add 'querylogger' into your INSTALLED_APPS.


For a non-Django project:
Just import querylogger.models somewhere, like main.py or wherever you guys put your code.

