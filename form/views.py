from .models import Form, Respondent
from user.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    FormListSerializer, FormSerializer, FormInvitedSerializer, 
    FormSubmitSerializer, FormSummarySerializer, FromDataSerializer,
    FormCompletedUserSerializer
)
from uuid import UUID
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


############현민############
class FormCreateView(APIView):
    @extend_schema(
            summary="폼 생성 For002-1",
            description="사용자가 폼을 생성하는 경우",
            request=FormInvitedSerializer,
            examples=[
                OpenApiExample(
                    name= 'Example Request',
                    value= {
                        "user": 1,  
                        "title": "설문조사 생성 테스트1",
                        "tag": "설문조사생성1 태그",
                        "end_at": "2025-01-31",  
                        "is_closed": 'TEMP',  
                        "target_count": 30,
                        "is_bookmark": False, 
                        "is_private": True, 
                        "access_code": "12345",  
                        "subtitle": "이렇게 표지~ ",
                        "form_description": "여기에 상세 설명 ",
                        "questions": [
                            {
                                "layout_type": "SHORT_TYPE",
                                "question": "이름을 입력해 주세요. ",
                                "question_order": 1,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": ""},
                                ]
                            },
                            {
                                "layout_type": "SHORT_TYPE",
                                "question": "소속 트랙을 선택해주세요.",
                                "question_order": 2,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": ""},
                                ]
                            },
                            {
                                "layout_type": "SHORT_TYPE",
                                "question": "소속 기수를 입력해 주세요.",
                                "question_order": 3,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": ""},
                                ]
                            },
                            {
                                "layout_type": "RANGE_TYPE",
                                "question": "이번 주 나의 학습 성취도는 어땠나요",
                                "question_order": 4,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "1"},
                                    {"option_number": 2, "option_context": "2"},
                                    {"option_number": 3, "option_context": "3"},
                                    {"option_number": 4, "option_context": "4"},
                                    {"option_number": 5, "option_context": "5"},
                                    {"option_number": 6, "option_context": "6"},
                                    {"option_number": 7, "option_context": "7"},
                                    {"option_number": 8, "option_context": "8"},
                                    {"option_number": 9, "option_context": "9"},
                                    {"option_number": 10, "option_context": "10"},
                                    {"option_number": 100, "option_context": "전혀 못 따라갔어요."},
                                    {"option_number": 200, "option_context": "완벽히 이해했어요."},
                                ]
                            },
                            {
                                "layout_type": "CHECKBOX_TYPE",
                                "question": "이번 주 어려웠던 주제를 모두 선택해주세요.",
                                "question_order": 5,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "TypeScript 타입 정의"},
                                    {"option_number": 2, "option_context": "Redux 상태 관리"},
                                    {"option_number": 3, "option_context": "Redux 상태 관리"},
                                    {"option_number": 4, "option_context": "비동기 통신 처리"},
                                    {"option_number": 5, "option_context": "Redux 상태 관리"},
                                    {"option_number": 99, "option_context": "기타"},
                                ]
                            },
                            {
                                "layout_type": "STAR_RATING_TYPE",
                                "question": "이번 주 강의 내용은 어떠셨나요?",
                                "question_order": 6,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "1"},
                                    {"option_number": 2, "option_context": "2"},
                                    {"option_number": 3, "option_context": "3"},
                                    {"option_number": 4, "option_context": "4"},
                                    {"option_number": 5, "option_context": "5"},
                                ]
                            },
                            {
                                "layout_type": "RADIO_TYPE",
                                "question": "다음 주 수업은 어떤 방식으로 진행되면 좋을까요?",
                                "question_order": 7,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "더 많은 실습 시간이 필요해요"},
                                    {"option_number": 2, "option_context": "더 자세한 이론 설명이 필요해요"},
                                    {"option_number": 3, "option_context": "지금 방식이 좋아요"},
                                    {"option_number": 99, "option_context": "기타"},
                                ]
                            },
                            {
                                "layout_type": "LONG_TYPE",
                                "question": "이번 주 학습 내용 중 가장 기억에 남는 것과 그 이유를 작성해 주세요.",
                                "question_order": 8,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": ""},
                                ]
                            },
                            {
                                "layout_type": "IMAGE_SELECT_TYPE",
                                "question": "마음에 드는 이미지를 선택해 주세요.",
                                "question_order": 9,
                                "is_required": True,
                                "options_of_questions": [
                                    {"option_number": 1, "option_context": "핑크 바람돌이URL"},
                                    {"option_number": 2, "option_context": "성깔 더러운 토끼URL"},
                                    {"option_number": 3, "option_context": "흰색 순댕이URL"},
                                    {"option_number": 4, "option_context": "졸려운 인절미URL"},
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
                                    {"option_number": 1, "option_context": ""},
                                ]
                            },
                        ]
                    },
                    description="폼 생성 데이터 user값은 토큰에서 추출하는 것으로 변경 예정"
                ),
            ],
            responses={
                    201: "폼 정보가 성공적으로 제출됨",
                    400: "잘못된 요청 (UUID 누락)",
            },
    )
    def post(self, request, *args, **kwargs):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            #serializer의 create 실행
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FormView(APIView):
    @extend_schema(
            summary="폼의 모든정보 로드 For002-2",
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
                            value='2bd64b2e1364441b9840020039906fe4',
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
            summary="폼에 참여하기 For003",
            description="폼 링크를 눌러 접속하면 접속자의 Access Token으로 사용자를 구분하고 전달받은 폼 uuid를 조합하여 사용자가 참여한 폼을 기록한다.",
            request=FormInvitedSerializer,
            examples=[
                OpenApiExample(
                    name= 'Example Request',
                    value= {
                        'uuid': '2bd64b2e1364441b9840020039906fe4',
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
    
class FromSummaryView(APIView):
    @extend_schema(
        summary="폼의 요약 기본 정보 로드 For004",
        description="폼 결과요약에서 사용",
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
                        value='2bd64b2e1364441b9840020039906fe4',
                        description='예시로 제공된 uuid, 사용자 정보는 token으로 처리'
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
            return Response({"error": "uuid is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            form = Form.objects.get(uuid=form_uuid)
        except Form.DoesNotExist:
            return Response({"error": "Form does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            serializer = FormSummarySerializer(form)
        except Exception :
            return Response({'error': str(Exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class FormSubmitView(APIView):
    @extend_schema(
            summary="폼 제출 For010",
            description="사용자가 폼을 제출하는 경우",
            request=FormInvitedSerializer,
            examples=[
                OpenApiExample(
                    name= 'Example Request',
                    value= {
                        "user": 1,  # 추후 엑세스토큰으로 사용자 구분가능 
                        "uuid": "2bd64b2e1364441b9840020039906fe4",
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
        
class FormListView(APIView):
    @extend_schema(
        summary="나의 폼 리스트 로드 For008",
        description="나의 폼에서 사용, user_id는 추후 토큰으로 변경 예정",
        responses={
                200: "폼 정보가 성공적으로 반환됨",
                400: "잘못된 요청 (UUID 누락)",
                404: "폼을 찾을 수 없음",
        }
    )
    def get(self, request, user_id):
        if not user_id: # 토큰으로 변경시 삭제 예정
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user_forms = Form.objects.filter(user=user)
        if not user_forms.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FormListSerializer(user_forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class FromDataView(APIView):
    @extend_schema(
        summary="폼의 요약 탭 정보 로드 For005",
        description="폼 결과요약의 요약탭에서 사용",
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
                        value='2bd64b2e1364441b9840020039906fe4',
                        description='예시로 제공된 uuid, 사용자 정보는 token으로 처리'
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
            return Response({"error": "uuid is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            form = Form.objects.get(uuid=form_uuid)
        except Form.DoesNotExist:
            return Response({"error": "Form does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FromDataSerializer(form)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FormCompletedUserView(APIView):
    @extend_schema(
        summary="폼의 참여자 목록 탭 정보 로드 For006",
        description="폼 결과요약의 참여자 목록 탭에서 사용",
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
                        value='2bd64b2e1364441b9840020039906fe4',
                        description='예시로 제공된 uuid, 사용자 정보는 token으로 처리'
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
            return Response({"error": "uuid is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            form = Form.objects.get(uuid=form_uuid)
        except Form.DoesNotExist:
            return Response({"error": "Form does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        respondents = Respondent.objects.filter(form=form)

        serializer = FormCompletedUserSerializer(respondents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        



############명현############