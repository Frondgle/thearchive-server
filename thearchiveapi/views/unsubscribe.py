from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from thearchiveapi.models import Subscriber

class UnsubscribeView(APIView):
    """Handle unsubscribe requests via token"""
    
    def delete(self, request): 
        token = request.query_params.get('token') 
        
        if not token:
            return Response(
                {"success": False, "message": "Invalid unsubscribe link"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            subscriber = Subscriber.objects.get(unsubscribe_token=token)
            subscriber.delete()
            print("Subscriber deleted successfully")
            
            return Response({
                "success": True, 
                "message": "User has been successfully unsubscribed"
            })
        
        except Subscriber.DoesNotExist:
            return Response(
                {"success": False, "message": "Invalid or expired unsubscribe link"},  
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e:
            print(f"Error unsubscribing: {str(e)}")
            return Response(
                {"success": False, "message": "An error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )