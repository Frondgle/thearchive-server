from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from thearchiveapi.models import Subscriber


@method_decorator(csrf_exempt, name='dispatch')
class SubscriberView(View):
    
    def post(self, request):
        try:
            print("Request body:", request.body)  # See raw data
            data = json.loads(request.body)
            print("Parsed data:", data)  # See parsed JSON
            email = data.get('email')
            print("Email:", email)  # See email value
            
            if not email:
                print("No email provided!")
                return JsonResponse({'success': False, 'message': 'Email is required'}, status=400)
            
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            
            if created:
                print("New subscriber created!")
                return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
            else:
                print("Email already exists!")
                return JsonResponse({'success': False, 'message': 'Email already subscribed'}, status=400)
                
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'message': str(e)}, status=500)