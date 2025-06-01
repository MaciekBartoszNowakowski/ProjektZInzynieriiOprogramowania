from applications.serializers.submission_serializer import SubmissionSerializer
from applications.services.submission_service import InvalidSupervisorIdException, InvalidThesisIdException, SubmissionService
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import Role

class ThesisSubmissionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, thesis_id):
        if request.user.role != Role.SUPERVISOR:
            return Response(
                {'error': 'Tylko promotorzy mogą przeglądać aplikacje na swoje prace'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission_service = SubmissionService()
        
        try:
            thesis = submission_service.get_thesis_with_submissions(request.user, thesis_id)
            submissions = thesis.submission_set.all()
            submission_serializer = SubmissionSerializer(submissions, many=True)
            
            response_data = {
                'thesis_id': thesis.id,
                'thesis_name': thesis.name,
                'submissions': submission_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except InvalidSupervisorIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidThesisIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e) + 'Wystąpił błąd podczas pobierania aplikacji'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
