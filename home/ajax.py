from django.utils import simplejson
from dajaxice.decorators import dajaxice_register, dajaxice_functions

@dajaxice_register
def sayHello(request):
    return simplejson.dumps({'message':'Hello, dajax'})


