from applications.services.submission_service import InvalidSupervisorIdException, SubmissionAlreadyResolvedException, SubmissionService
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import Role

class RejectSubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, submission_id):
        if request.user.role != Role.SUPERVISOR:
            return Response(
                {'error': 'Tylko promotorzy mogą odrzucać aplikacje'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission_service = SubmissionService()
        
        try:
            result = submission_service.reject_submission(request.user, submission_id)
            return Response(result, status=status.HTTP_200_OK)
        
        except InvalidSupervisorIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except SubmissionAlreadyResolvedException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Wystąpił błąd podczas odrzucania aplikacji'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
