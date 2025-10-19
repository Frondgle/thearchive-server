from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from thearchiveapi.models import Subscriber


@method_decorator(csrf_exempt, name="dispatch")
class UnsubscribeView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if not token:
                return JsonResponse(
                    {"success": False, "message": "Invalid unsubscribe link"}, 
                    status=400
                )
            
            try:
                subscriber = Subscriber.objects.get(unsubscribe_token=token)
                # email = subscriber.email
                subscriber.delete()
                print(f"Subscriber deleted successfully")
                
                return JsonResponse({
                    "success": True, 
                    "message": f"User has been successfully unsubscribed"
                })
            
            except Subscriber.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Invalid or expired unsubscribe link"},  
                    status=404
                )
        
        except Exception as e:
            print(f"Error unsubscribing: {str(e)}")
            return JsonResponse(
                {"success": False, "message": "An error occurred"}, 
                status=500
            )