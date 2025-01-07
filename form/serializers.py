from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *
from user.models import CustomUser

###############현민###############
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

# 질문 시리얼라이저
class QuestionsSerializer(serializers.ModelSerializer):
    # OptionsOfQuestions와 관계 설정 Question은 여러개의 Options를 가질수 있지만 필수는 아니다.
    options_of_questions = OptionsOfQuestionsSerializer(many=True, required=False)

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
class FormSerializer(serializers.ModelSerializer):
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
        
    # def update(self, instance, validated_data):
    #     # 질문 갱신을 위해 질문내용을 새로 받는다.
    #     questions_data = validated_data.pop('questions', [])
        
    #     # 폼의 모든 정보를 새로 갱신한다.
    #     instance.title = validated_data.pop('title', instance.title)
    #     instance.tag = validated_data.pop('tag', instance.tag)
    #     instance.end_at = validated_data.pop('end_at', instance.end_at)
    #     instance.is_closed = validated_data.pop('is_closed', instance.is_closed)
    #     instance.access_code = validated_data.pop('access_code', instance.access_code)
    #     instance.subtitle = validated_data.pop('subtitle', instance.subtitle)
    #     instance.form_description = validated_data.pop('form_description', instance.form_description)
    #     instance.save()

    #     # 기존 질문을 삭제하고 새로 받은 질문내용으로 갱신한다.
    #     # questions_set 장고에서 form과 연결된 questions를 관리하기 위해 생성한 set.
    #     instance.questions_set.all().delete()
    #     for question_data in questions_data:
    #         options_data = question_data.pop('options_of_questions',[])
    #         question = Questions.objects.create(form=instance, **question_data)
    #         for option_data in options_data:
    #             OptionsOfQuestions.objects.create(question=question, **option_data)
    #     return instance

# 폼 요약 시리얼라이저
class FormSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Form
        fields = [
            'user',
            'title',
            'tag',
            'end_at',
            'is_closed',
            'access_code',
            'subtitle',
            'form_description',
            'uuid',
        ]

   
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
            question = get_object_or_404(Questions, form=form, question_order=question_data['question_order'])
            # 주관식
            if question.layout_type in ['SHORT_TYPE','LONG_TYPE','DATE_TYPE','NUMBER_TYPE','EMAIL_TYPE','FILE_UPLOAD_TYPE']:
                response = question_data.get('options_of_questions', [])[0].get('option_context', '')
                SubjectiveAnswers.objects.create(user=user, question=question, response=response)
            # 객관식
            if question.layout_type in ['CHECKBOX_TYPE', 'RADIO_TYPE', 'DROPDOWN_TYPE', 'RANGE_TYPE', 'STAR_RATING_TYPE', 'IMAGE_SELECT_TYPE']:
                for option_data in question_data.get('options_of_questions',[]):
                    selected_options = get_object_or_404(
                        OptionsOfQuestions, 
                        question=question, 
                        option_number=option_data['option_number']
                    )
                    MultipleAnswers.objects.create(user=user, options_of_question=selected_options)
        # 제출자 제출완료로 변경 FormInvitedSerializer 이용
        form_invited_serializer.update(instance=respondent, validated_data={'is_complete':True})
        return form
        






    # LAYOUT_CHOICES = [
    #     ('SHORT_TYPE', 'SHORT_TYPE'),
    #     ('LONG_TYPE', 'LONG_TYPE'),
    #     ('DATE_TYPE', 'DATE_TYPE'),
    #     ('NUMBER_TYPE', 'NUMBER_TYPE'),
    #     ('EMAIL_TYPE', 'EMAIL_TYPE'),
    #     ('FILE_UPLOAD_TYPE', 'FILE_UPLOAD_TYPE')
    # ]
    LAYOUT_CHOICES = [
        ('CHECKBOX_TYPE','CHECKBOX_TYPE'),
        ('RADIO_TYPE','RADIO_TYPE'),
        ('DROPDOWN_TYPE','DROPDOWN_TYPE'),
        ('RANGE_TYPE','RANGE_TYPE'),
        ('STAR_RATING_TYPE','STAR_RATING_TYPE'),
        ('IMAGE_SELECT_TYPE','IMAGE_SELECT_TYPE'),
    ]        



###############명현############### 