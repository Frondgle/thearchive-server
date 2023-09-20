from rest_framework.decorators import api_view
from rest_framework.response import Response
from thearchiveapi.models import Fan


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Fan

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    fan = Fan.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if fan is not None:
        data = {
            'id': fan.id,
            'uid': fan.uid
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new Fan for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    fan = Fan.objects.create(
        uid=request.data['uid']
    )

    # Return the fan info to the client
    data = {
        'id': fan.id,
        'uid': fan.uid
    }
    return Response(data)
