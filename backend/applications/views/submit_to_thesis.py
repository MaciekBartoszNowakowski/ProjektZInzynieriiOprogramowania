from applications.serializers.submission_create_serializer import SubmissionCreateSerializer
from applications.serializers.created_submission_serializer import CreatedSubmissionSerializer
from applications.services.submission_service import InvalidStudentIdException, InvalidThesisIdException, StudentAlreadyAssignedException, SubmissionService, ThesisNotAvailableException
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import Role

class SubmitToThesisView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionCreateSerializer
    
    def create(self, request):
        if request.user.role != Role.STUDENT:
            return Response(
                {'error': 'Tylko studenci mogą składać aplikacje na prace dyplomowe'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        thesis_id = serializer.validated_data['thesis_id']
        submission_service = SubmissionService()
        
        try:
            submission = submission_service.submit_to_thesis(request.user, thesis_id)
            submission_serializer = CreatedSubmissionSerializer(submission, context={'request': request})
            return Response(submission_serializer.data, status=status.HTTP_201_CREATED)
        
        except InvalidStudentIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidThesisIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ThesisNotAvailableException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except StudentAlreadyAssignedException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Wystąpił błąd podczas składania aplikacji'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
