from rest_framework import serializers
from .models import *

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
            'is_required', 
            'options_of_questions'
            ]

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
        for quesiton_data in questions_data:
            options_data = questions_data.pop('options_of_questions', [])
            question = Questions.objects.create(form=form, **questions_data)
            # 보기 생성
            for option_data in options_data:
                OptionsOfQuestions.objects.create(question=question, **options_data)
        return form
        
    def update(self, instance, validated_data):
        # 질문 갱신을 위해 질문내용을 새로 받는다.
        questions_data = validated_data.pop('questions', [])
        
        # 폼의 모든 정보를 새로 갱신한다.
        instance.title = validated_data.pop('title', instance.title)
        instance.tag = validated_data.pop('tag', instance.tag)
        instance.end_at = validated_data.pop('end_at', instance.end_at)
        instance.is_closed = validated_data.pop('is_closed', instance.is_closed)
        instance.access_code = validated_data.pop('access_code', instance.access_code)
        instance.subtitle = validated_data.pop('subtitle', instance.subtitle)
        instance.form_description = validated_data.pop('form_description', instance.form_description)
        instance.save()

        # 기존 질문을 삭제하고 새로 받은 질문내용으로 갱신한다.
        # questions_set 장고에서 form과 연결된 questions를 관리하기 위해 생성한 set.
        instance.questions_set.all().delete()
        for question_data in questions_data:
            options_data = question_data.pop('options_of_questions',[])
            question = Questions.objects.create(form=instance, **questions_data)
            for option_data in options_data:
                OptionsOfQuestions.objects.create(question=question, **options_data)
        return instance