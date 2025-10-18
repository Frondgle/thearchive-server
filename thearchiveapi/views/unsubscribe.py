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
            email = data.get('email')
            
            if not email:
                return JsonResponse(
                    {"success": False, "message": "Email is required"}, 
                    status=400
                )
            
            try:
                subscriber = Subscriber.objects.get(email=email)
                subscriber.delete()
                print(f"Subscriber {email} deleted successfully")
                
                return JsonResponse({
                    "success": True, 
                    "message": "Successfully unsubscribed"
                })
            
            except Subscriber.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Email not found"}, 
                    status=404
                )
        
        except Exception as e:
            print(f"Error unsubscribing: {str(e)}")
            return JsonResponse(
                {"success": False, "message": "An error occurred"}, 
                status=500
            )