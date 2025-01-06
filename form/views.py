from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from .models import Form, Respondent, Questions, OptionsOfQuestions, MultipleAnswers, SubjectiveAnswers, Statistics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FormSerializer, FormInvitedSerializer, FormSubmitSerializer
from uuid import UUID
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample



############현민############
class FormCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            #serializer의 create 실행
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FormView(APIView):
    @extend_schema(
            summary="폼의 모든정보 로드",
            description="미리보기, 참여폼에서 사용",
            parameters=[
                OpenApiParameter(
                    name='uuid', 
                    description="폼의 uuid(필수)",
                    required=True, 
                    type=str,
                    location=OpenApiParameter.PATH,
                    examples=[
                        OpenApiExample(
                            name='uuid예시',
                            value='f4f86d3e59954b57afe0b28bfc0fd8ad',
                            description='예시로 제공된 uuid'
                        ),
                    ],
                ),
            ],
            responses={
                    200: "폼 정보가 성공적으로 반환됨",
                    400: "잘못된 요청 (UUID 누락)",
                    404: "폼을 찾을 수 없음",
            }
    )
    def get(self, request, uuid):
        form_uuid = UUID(uuid)
        if not form_uuid:
            return Response({'error':'Form uuid is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            form = Form.objects.prefetch_related('questions_set__optionsofquestions_set').get(uuid=form_uuid)
        except Form.DoesNotExist:
            return Response({'error': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FormSerializer(form)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class FormInvitedView(APIView):
    @extend_schema(
            summary="폼에 참여하기",
            description="폼 링크를 눌러 접속하면 접속자의 Access Token으로 사용자를 구분하고 전달받은 폼 uuid를 조합하여 사용자가 참여한 폼을 기록한다.",
            request=FormInvitedSerializer,
            examples=[
                OpenApiExample(
                    name= 'Example Request',
                    value= {
                        'uuid': 'f4f86d3e59954b57afe0b28bfc0fd8ad',
                        'user': 1
                    },
                    description="폼 참여 데이터 user값은 추후에 토큰에서 추출하는 것으로 변경 예정"
                ),
            ],
            responses={
                    200: "폼 정보가 성공적으로 반환됨",
                    400: "잘못된 요청 (UUID 누락)",
                    404: "폼을 찾을 수 없음",
            },
    )
            
    def post(self, request):
        serializer = FormInvitedSerializer(data=request.data)
        if serializer.is_valid():
            respondent, created = serializer.save()
            if created:
                # 신규생성 완료
                return Response(status=status.HTTP_201_CREATED)
            # 기존 참여자
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FormSubmitView(APIView):
    @extend_schema(
            summary="폼 제출",
            description="사용자가 폼을 제출하는 경우",
            request=FormInvitedSerializer,
            examples=[
                OpenApiExample(
                    name= 'Example Request',
                    value= {
                        "user": 1,  # 추후 엑세스토큰으로 사용자 구분가능 
                        "uuid": "f4f86d3e59954b57afe0b28bfc0fd8ad",
                        "questions": [
                            {
                                "layout_type": "SHORT_TYPE",
                                "question": "이름을 입력해 주세요. ",
                                "question_order": 1,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "신현민"},
                                ]
                            },
                            {
                                "layout_type": "SHORT_TYPE",
                                "question": "소속 트랙을 선택해주세요.",
                                "question_order": 2,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "HOT TRACKS"},
                                ]
                            },
                            {
                                "layout_type": "SHORT_TYPE",
                                "question": "소속 기수를 입력해 주세요.",
                                "question_order": 3,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "6+2=8기?"},
                                ]
                            },
                            {
                                "layout_type": "RANGE_TYPE",
                                "question": "이번 주 나의 학습 성취도는 어땠나요",
                                "question_order": 4,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 7, "option_context": "7"},
                                    # {"option_number": 6, "option_context": "7"},
                                ]
                            },
                            {
                                "layout_type": "CHECKBOX_TYPE",
                                "question": "이번 주 어려웠던 주제를 모두 선택해주세요.",
                                "question_order": 5,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "TypeScript 타입 정의"},
                                    {"option_number": 3, "option_context": "Redux 상태 관리"},
                                    {"option_number": 4, "option_context": "비동기 통신 처리"},
                                    {"option_number": 99, "option_context": "기타는 악기인가?"},
                                ]
                            },
                            {
                                "layout_type": "STAR_RATING_TYPE",
                                "question": "이번 주 강의 내용은 어떠셨나요?",
                                "question_order": 6,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 4, "option_context": "4"},
                                ]
                            },
                            {
                                "layout_type": "RADIO_TYPE",
                                "question": "다음 주 수업은 어떤 방식으로 진행되면 좋을까요?",
                                "question_order": 7,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 3, "option_context": "지금 방식이 좋아요"},
                                ]
                            },
                            {
                                "layout_type": "LONG_TYPE",
                                "question": "이번 주 학습 내용 중 가장 기억에 남는 것과 그 이유를 작성해 주세요.",
                                "question_order": 8,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "FE, BE 소통 좋아요~"},
                                ]
                            },
                            {
                                "layout_type": "IMAGE_SELECT_TYPE",
                                "question": "마음에 드는 이미지를 선택해 주세요.",
                                "question_order": 9,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 2, "option_context": "성깔 더러운 토끼URL"},
                                ]
                            },
                            {
                                "layout_type": "FILE_UPLOAD_TYPE",
                                "question": "이번 주 과제물을 제출해 주세요.",
                                "question_order": 10,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "File URL"},
                                ]
                            },
                            {
                                "layout_type": "EMAIL_TYPE",
                                "question": "피드백 답변을 받을 이메일 주소를 입력해 주세요.",
                                "question_order": 11,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "pollloop@pollloop.com"},
                                ]
                            },
                        ]
                    },
                    description="폼 제출 데이터 user값은 토큰에서 추출하는 것으로 변경 예정"
                ),
            ],
            responses={
                    201: "폼 정보가 성공적으로 제출됨",
                    400: "잘못된 요청 (UUID 누락)",
            },
    )
    def post(self, request):
        serializer = FormSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
        
        
        





############명현############
class FormParticipantsView(View):
    def get(self, request, form_id):
        form = get_object_or_404(Form, id=form_id)

        # 설문에 참여한 모든 사용자 조회
        respondents = Respondent.objects.filter(form=form).values_list('user__CustomUser.email', flat=True)

        # 객관식 답변을 제출한 사용자 조회
        multiple_answer_users = MultipleAnswers.objects.filter(
            options_of_question__question__form=form
        ).values_list('user__CustomUser.email', flat=True).distinct()

        # 주관식 답변을 제출한 사용자 조회
        subjective_answer_users = SubjectiveAnswers.objects.filter(
            question__form=form
        ).values_list('user__CustomUser.email', flat=True).distinct()

        # 모든 답변을 제출한 사용자 (객관식과 주관식 모두 포함)
        all_answer_users = set(multiple_answer_users) | set(subjective_answer_users)

        data = {
            'all_respondents': list(respondents),
            'answered_users': list(all_answer_users),
        }

        return JsonResponse(data)


class FormActionView(View):
    def post(self, request, form_id):
        form = get_object_or_404(Form, id=form_id)
        action = self.kwargs.get('action')

        if action == 'enter':
            # 설문 입장 처리
            respondent, created = Respondent.objects.get_or_create(
                user=request.user,
                form=form
            )
            message = '설문에 입장했습니다.'
        elif action == 'submit':
            # 설문 제출 처리
            # 여기서는 제출 여부만 확인합니다. 실제 답변 저장은 별도의 뷰에서 처리해야 합니다.
            has_answers = MultipleAnswers.objects.filter(user=request.user,
                                                         options_of_question__question__form=form).exists() or \
                          SubjectiveAnswers.objects.filter(user=request.user, question__form=form).exists()
            if has_answers:
                message = '설문이 성공적으로 제출되었습니다.'
                submit_at = timezone.now()
                return JsonResponse({'submit': submit_at, 'message': message})
            else:
                return JsonResponse({'status': 'error', 'message': '제출할 답변이 없습니다.'})
        else:
            return JsonResponse({'status': 'error', 'message': '잘못된 액션입니다.'})

        return JsonResponse({'status': 'success', 'message': message})


'''
통계에서 각 질문당 몇번 답변 내용에 대한 data 보여주고
주관식의 경우 답변내용 전체 data보여주기
'''
# Form 요약
class FormDetailView(View):
    def get(self, request, form_id):
        form = get_object_or_404(Form, id=form_id)
        multiple_answer = get_object_or_404(MultipleAnswers, options_of_question__question__form=form)
        answer = Statistics.objects.filter(id=OptionsOfQuestions, options_of_question__statistics__count=request.count)
        questions = Questions.objects.filter(form=form)
