from applications.serializers.submission_create_serializer import SubmissionCreateSerializer
from applications.serializers.submission_serializer import SubmissionSerializer
from applications.serializers.submission_status_serializer import SubmissionStatusSerializer
from applications.services.submission_service import InvalidStudentIdException, InvalidSupervisorIdException, InvalidThesisIdException, StudentAlreadyAssignedException, SubmissionService, ThesisFullException, ThesisNotAvailableException
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from thesis.services.thesis_service import ThesisService
from users.models import Role

class AcceptSubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, submission_id):
        if request.user.role != Role.SUPERVISOR:
            return Response(
                {'error': 'Tylko promotorzy mogą akceptować aplikacje'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission_service = SubmissionService()
        
        try:
            submission = submission_service.accept_submission(request.user, submission_id)
            submission_serializer = SubmissionSerializer(submission)
            return Response(submission_serializer.data, status=status.HTTP_200_OK)
        
        except InvalidSupervisorIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Wystąpił błąd podczas akceptacji aplikacji'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)