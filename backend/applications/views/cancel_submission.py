from applications.services.submission_service import InvalidStudentIdException, SubmissionAlreadyResolvedException, SubmissionService
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import Role


class CancelSubmissionView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        if request.user.role != Role.STUDENT:
            return Response(
                {'error': 'Tylko studenci mogą anulować swoje aplikacje'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission_service = SubmissionService()
        
        try:
            result = submission_service.cancel_submission(request.user)
            return Response(result, status=status.HTTP_200_OK)
        
        except InvalidStudentIdException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except SubmissionAlreadyResolvedException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Wystąpił błąd podczas anulowania aplikacji'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
