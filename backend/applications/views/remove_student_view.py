from applications.services.submission_service import InvalidSupervisorIdException, SubmissionNotAcceptedException, SubmissionService
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import Role

class RemoveStudentFromThesisView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, submission_id):
        if request.user.role != Role.SUPERVISOR:
            return Response(
                {'error': 'Tylko promotorzy mogą usuwać studentów z prac'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission_service = SubmissionService()
        
        try:
            result = submission_service.remove_student_from_thesis(request.user, submission_id)
            return Response(result, status=status.HTTP_200_OK)
        
        except InvalidSupervisorIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except SubmissionNotAcceptedException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Wystąpił błąd podczas usuwania studenta'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        