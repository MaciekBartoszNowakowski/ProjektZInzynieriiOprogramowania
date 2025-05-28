from applications.serializers.submission_create_serializer import SubmissionCreateSerializer
from applications.serializers.submission_serializer import SubmissionSerializer
from applications.serializers.submission_status_serializer import SubmissionStatusSerializer
from applications.services.submission_service import InvalidStudentIdException, InvalidThesisIdException, StudentAlreadyAssignedException, SubmissionService, ThesisFullException, ThesisNotAvailableException
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from thesis.services.thesis_service import ThesisService
from users.models import Role

class StudentSubmissionStatusView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.role != Role.STUDENT:
            return Response(
                {'error': 'Tylko studenci mogą sprawdzać status swoich aplikacji'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission_service = SubmissionService()
        
        try:
            submission = submission_service.get_student_submission(request.user)
            
            if submission:
                submission_serializer = SubmissionSerializer(submission)
                response_data = {
                    'has_submission': True,
                    'submission': submission_serializer.data
                }
            else:
                response_data = {
                    'has_submission': False,
                    'submission': None,
                    'message': 'Nie masz aktywnej aplikacji na żadną pracę dyplomową'
                }
            
            serializer = SubmissionStatusSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except InvalidStudentIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Wystąpił błąd podczas pobierania statusu aplikacji'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

