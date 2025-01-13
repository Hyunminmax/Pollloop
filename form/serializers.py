from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *
from user.models import CustomUser

###############현민###############
# UUID 처리를 위한 클래스
class UUIDHypenRemoveMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'uuid' in representation and isinstance(representation['uuid'], str):
            representation['uuid'] = representation['uuid'].replace('-', '')
        return representation

# 폼 참여인원 시리얼라이저
class FormInvitedSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(write_only=True)
    user = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Respondent
        fields = ['uuid', 'user', 'is_complete']
    
    def validate_uuid(self, value):
        form = get_object_or_404(Form, uuid=value)
        return form
    
    def validate_user(self, value):
        user = get_object_or_404(CustomUser, id=value)
        return user
    
    def create(self, validated_data):
        form = validated_data['uuid']
        user = validated_data['user']
        # form, user 정보로 기존 참여자가 있는지 조회
        existing_respondent = Respondent.objects.filter(user=user, form=form).first()
        # 기존 참여자면 참여자 정보 반환
        if existing_respondent:
            return existing_respondent, False
        # 신규 참여자면 생성
        respondent = Respondent.objects.create(user=user, form=form)
        return respondent, True

#폼 시리얼라이저가 질문과 질문의 보기를 포함해야 하기 때문에 질문의 보기부터 질문, 폼 순서로 작성
# 객관식 질문의 보기 시리얼라이저 클래스
class OptionsOfQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionsOfQuestions
        fields = [
            'option_number', 
            'option_context'
            ]

# 객관식 질문의 보기 시리얼라이저 클래스 조회용!
class OptionsOfQuestionsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionsOfQuestions
        fields = [
            'option_number', 
            'option_context'
            ]

# 질문 시리얼라이저
class QuestionsSerializer(serializers.ModelSerializer):
    # OptionsOfQuestions와 관계 설정 Question은 여러개의 Options를 가질수 있지만 필수는 아니다.
    options_of_questions = OptionsOfQuestionsSerializer(many=True, required=False)
    # options_of_questions = OptionsOfQuestionsSerializer(many=True, source='optionsofquestions_set', required=False)

    class Meta:
        model = Questions
        fields = [
            'layout_type', 
            'question', 
            'question_order',
            'is_required', 
            'options_of_questions'
            ]
        
# 질문 시리얼라이저 조회용!
class QuestionsReadSerializer(serializers.ModelSerializer):
    # OptionsOfQuestions와 관계 설정 Question은 여러개의 Options를 가질수 있지만 필수는 아니다.
    options_of_questions = OptionsOfQuestionsSerializer(many=True, source='optionsofquestions_set', required=False)

    class Meta:
        model = Questions
        fields = [
            'layout_type', 
            'question', 
            'question_order',
            'is_required', 
            'options_of_questions'
            ]
# 폼 시리얼라이저
class FormSerializer(UUIDHypenRemoveMixin, serializers.ModelSerializer):
    # Form의 관계 설정 Form은 Questions를 가질수 있지만 필수는 아니다. 생성 후 바로 임시저장의 경우 질문 없음.
    questions = QuestionsSerializer(many=True, required=False)
    
    class Meta:
        model = Form
        fields = [
            'user', #커스텀유저와 관계설정용
            'title', # 폼의 제목
            'tag', # 폼의 테그
            'create_at', #폼의 생성시간
            'end_at', # 폼의 작성 제한 시간
            'is_closed', # 폼 종료여부
            'target_count', # 목표인원
            'is_bookmark', # 즐겨찾기 여부
            'is_private', # 비공개 여부 
            'access_code', # 폼 접근 코드
            'subtitle', # 폼의 소제목
            'form_description', # 폼의 설명
            'uuid', # 링크에 사용할 uuid
            'questions' # 폼이 포함하고 있는 질문과 관계설정용
        ]

    def create(self, validated_data):
        # questions 만들기 위해 questions을 분리한다. 없다면 빈 리스트반환
        questions_data = validated_data.pop('questions', [])
        form = Form.objects.create(**validated_data)
        # 질문 생성
        for question_data in questions_data:
            options_data = question_data.pop('options_of_questions', [])
            question = Questions.objects.create(form=form, **question_data)
            # 보기 생성
            for option_data in options_data:
                OptionsOfQuestions.objects.create(question=question, **option_data)
            
        return form
    
class FormReadSerializer(UUIDHypenRemoveMixin, serializers.ModelSerializer):
    # Form의 관계 설정 Form은 Questions를 가질수 있지만 필수는 아니다. 생성 후 바로 임시저장의 경우 질문 없음.
    questions = QuestionsReadSerializer(many=True, source='questions_set', required=False)
    
    class Meta:
        model = Form
        fields = [
            'user', #커스텀유저와 관계설정용
            'title', # 폼의 제목
            'tag', # 폼의 테그
            'create_at', #폼의 생성시간
            'end_at', # 폼의 작성 제한 시간
            'is_closed', # 폼 종료여부
            'target_count', # 목표인원
            'is_bookmark', # 즐겨찾기 여부
            'is_private', # 비공개 여부 
            'access_code', # 폼 접근 코드
            'subtitle', # 폼의 소제목
            'form_description', # 폼의 설명
            'uuid', # 링크에 사용할 uuid
            'questions' # 폼이 포함하고 있는 질문과 관계설정용
        ]


# 폼 요약 기본정보 시리얼라이저
class FormSummarySerializer(UUIDHypenRemoveMixin, serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = [
            'user',
            'uuid',
            'title',
            'tag',
            'subtitle',
            'form_description',
            'create_at',
            'end_at',
            'user_count',
            'completed_count',
            'target_count',
            'is_closed',
            'is_private',
            'access_code'
        ]
    
    def get_user_count(self, form):
        return Respondent.objects.filter(form=form).count()
    def get_completed_count(self, form):
        return Respondent.objects.filter(form=form, is_complete=True).count()

# 폼 요약 데이터(요약 탭) 시리얼라이저
class FromDataSerializer(UUIDHypenRemoveMixin, serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = [
            'uuid',
            'title',
            'data',
        ]
    
    # 통계 데이터 취합
    def get_data(self, form):
        questions = Questions.objects.filter(form=form)
        data = []
        for question in questions:
            options = OptionsOfQuestions.objects.filter(question=question)
            options_stats = []
            
            # 객관식
            if question.layout_type in ['CHECKBOX_TYPE', 'RADIO_TYPE', 'DROPDOWN_TYPE', 'RANGE_TYPE', 'STAR_RATING_TYPE', 'IMAGE_SELECT_TYPE']:
                for option in options:
                    if option.option_number in [100, 200]:
                        continue
                    if option.option_number not in [99]:
                        count = MultipleAnswers.objects.filter(options_of_question=option).count()
                        options_stats.append({
                            'label': option.option_context,
                            'count': count,
                        })
                    else:
                        etc_responses = SubjectiveAnswers.objects.filter(question=question, options_of_question=option)
                        response_values = []
                        
                        for res in etc_responses:
                            response_values.append(
                                res.response
                                )
                        count = len(response_values)
                    
                        options_stats.append({
                        'label': option.option_context,
                        'values': response_values,
                        'count': count,
                        })
                        
            # 주관식
            else:
                subjective_responses = SubjectiveAnswers.objects.filter(question=question)
                response_values = []
                for res in subjective_responses:
                    options_stats.append({
                        'value': res.response,
                    })

            data.append({
                'id': question.question_order,
                'layout_type': question.layout_type,
                'is_required': question.is_required,
                'question': question.question,
                'results': options_stats,
            })
        return data

# 폼 제출 시리얼라이저
class FormSubmitSerializer(serializers.Serializer):
    user = serializers.IntegerField(write_only=True)
    uuid = serializers.UUIDField(write_only=True)
    questions = serializers.ListField(child=serializers.DictField(), write_only=True)

    def validate(self, data):
        # 폼, 사용자 확인
        form = get_object_or_404(Form, uuid=data['uuid'])
        user = get_object_or_404(CustomUser, id=data['user'])
        data['form']=form
        data['user']=user
        return data
    
    def create(self, validated_data):
        form = validated_data['form']
        user = validated_data['user']
        # 제출자 등록 호출 FormInvitedSerializer 이용
        form_invited_serializer = FormInvitedSerializer(data={
            'uuid' : form.uuid,
            'user' : user.id
        })
        form_invited_serializer.is_valid(raise_exception=True)
        respondent, created = form_invited_serializer.create(form_invited_serializer.validated_data)

        # 폼 저장
        questions_data = validated_data['questions']
        for question_data in questions_data:
            question = get_object_or_404(
                Questions, 
                form=form, 
                question_order=question_data['question_order']
            )
            options = question_data.get('options_of_questions', [])
            
            # 주관식
            if question.layout_type in ['SHORT_TYPE','LONG_TYPE','DATE_TYPE','NUMBER_TYPE','EMAIL_TYPE','FILE_UPLOAD_TYPE']:
                if options:
                    option_number = options[0]['option_number']
                    selected_option = get_object_or_404(
                        OptionsOfQuestions,
                        question = question, 
                        option_number=option_number
                    )
                    response = options[0].get('option_context','')
                    SubjectiveAnswers.objects.create(user=user, question=question, options_of_question=selected_option, response=response)

            # 객관식
            if question.layout_type in ['CHECKBOX_TYPE', 'RADIO_TYPE', 'DROPDOWN_TYPE', 'RANGE_TYPE', 'STAR_RATING_TYPE', 'IMAGE_SELECT_TYPE']:
                for option_data in options:
                    if option_data['option_number'] == 99:
                        selected_option = get_object_or_404(
                            OptionsOfQuestions,
                            question=question,
                            option_number=option_data['option_number']
                        )
                        response = option_data.get('option_context', '')
                        SubjectiveAnswers.objects.create(user=user, question=question, options_of_question=selected_option, response=response)
                    else:
                        selected_options = get_object_or_404(
                            OptionsOfQuestions, 
                            question=question, 
                            option_number=option_data['option_number']
                        )
                        MultipleAnswers.objects.create(user=user, options_of_question=selected_options)
        # 제출자 제출완료로 변경 FormInvitedSerializer 이용
        form_invited_serializer.update(instance=respondent, validated_data={'is_complete':True})
        return form
        
# 폼 리스트 시리얼라이저
class FormListSerializer(UUIDHypenRemoveMixin, serializers.ModelSerializer):
    class Meta:
        model = Form
        fields =[
            'title',
            'tag',
            'create_at',
            'end_at',
            'is_closed',
            'access_code',
            'uuid',
            'target_count',
            'is_private',
            'is_bookmark'
        ]

# 폼 요약 데이터(참여자 목록 탭) 시리얼라이저
class FormCompletedUserSerializer(UUIDHypenRemoveMixin, serializers.ModelSerializer):
    # uuid 받아서 폼 찾고
    # respondent에서 해당 폼 관련 데이터 찾고
    # 관련 유저들의 이메일과 is_complete 상태반환
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Respondent
        fields = ['email', 'is_complete']

# 폼 즐겨찾기 설정 
class FormBookmarkSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    is_bookmark = serializers.BooleanField()
    # 인증 적용후 삭제 예정
    user = serializers.IntegerField()

# 폼 삭제
class FromRemoveSerializer(serializers.Serializer):
    # 첫 시도는 ModelSerializer를 상속받아 시도했지만 기존데이터와 충돌?이 발생하며 삭제하지 못한다. 
    uuid = serializers.UUIDField()
    user = serializers.IntegerField()
    
    def delete(self):
        uuid = self.validated_data['uuid']
        user = self.validated_data['user']
        form = get_object_or_404(Form, uuid=uuid, user=user)
        form.delete()
        return True



###############명현############### 