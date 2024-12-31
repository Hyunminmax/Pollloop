from rest_framework import serializers
from .models import *

# 객관식 질문의 보기 시리얼라이져 클래스
class OptionsOfQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionsOfQuestions
        fields = ['question', 'option_context']

class QuestionsSerializer(serializers.ModelSerializer):
    # OptionsOfQuestions와 관계 설정 Question은 여러개의 Options를 가질수 있지만 필수는 아니다.
    options_of_questions = OptionsOfQuestionsSerializer(many=True, required=False)

    class Meta:
        model = Questions
        fields = ['layout_type', 'question', 'is_required', 'options_of_questions']

    def create(self, vaildated_data):
        # options를 만들기 위해 options_of_questions을 분리한다. 없다면 빈 리스트반환
        options_data = vaildated_data.pop('options_of_questions', [])
        # **언패킹 연산 = 딕셔너리로 'aaa':'111'이 들어왔다면 aaa = '111'로 반환
        question = Questions.objects.create(**vaildated_data)
        for option_data in options_data:
            OptionsOfQuestions.objects.create(question=question, **option_data)


# #폼 시리얼라이져가 질문과 질문의 보기를 포함해야 하기 때문에 질문의 보기부터 질문, 폼 순서로 작성
# class FormSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Form
#         fields = '__all__'
    
# [
#     {
#         "option_number": 1, 'option_context': 'asdflkjsadfj',
#         "option_number": 2, 'option_context': 'asdflkjsadfj',
#         "option_number": 3, 'option_context': 'asdflkjsadfj',
#         "option_number": 4, 'option_context': 'asdflkjsadfj',
#     }
# ]