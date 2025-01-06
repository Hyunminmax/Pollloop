from django.db import models
from user.models import CustomUser
import uuid as uuid_lib

class Form(models.Model):
    STATUS_CHOICES = [      #상태
        ('TEMP', 'TEMP'),
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="제목")
    tag = models.CharField(max_length=255, verbose_name="태그")
    create_at = models.DateField(auto_now_add=True)
    end_at = models.DateField()
    is_closed = models.CharField(choices=STATUS_CHOICES,max_length=20,  help_text="상태") #ENUM값으로 변경해야함
    access_code = models.CharField(max_length=255, verbose_name="입장코드", null=True, blank=True)
    subtitle = models.CharField(max_length=255, verbose_name="부 제목")
    form_description = models.CharField(max_length=255, help_text="상세 내용")
    uuid = models.UUIDField(default=uuid_lib.uuid4, unique=True)
    target_count = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False) # 기본 값 false = 공개
    is_bookmark = models.BooleanField(default=False) # 기본 값 false = 즐겨찾기 X인 상태


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'form'

# Form참여 인원
class Respondent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    class Meta:
        db_table = 'respondent'


# 질문
class Questions(models.Model):
    LAYOUT_CHOICES = [
        ('SHORT_TYPE', 'SHORT_TYPE'),
        ('LONG_TYPE', 'LONG_TYPE'),
        ('CHECKBOX_TYPE', 'CHECKBOX_TYPE'),
        ('RADIO_TYPE', 'RADIO_TYPE'),
        ('DROPDOWN_TYPE', 'DROPDOWN_TYPE'),
        ('RANGE_TYPE', 'RANGE_TYPE'),
        ('STAR_RATING_TYPE', 'STAR_RATING_TYPE'),
        ('IMAGE_SELECT_TYPE', 'IMAGE_SELECT_TYPE'),
        ('NUMBER_TYPE', 'NUMBER_TYPE'),
        ('DATE_TYPE', 'DATE_TYPE'),
        ('EMAIL_TYPE', 'EMAIL_TYPE'),
        ('FILE_UPLOAD_TYPE', 'FILE_UPLOAD_TYPE')
    ]
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    layout_type = models.CharField(choices=LAYOUT_CHOICES, max_length=255)
    question = models.TextField()
    question_order = models.IntegerField()
    is_required = models.BooleanField(default=False)

    class Meta:
        db_table = 'questions'

# 보기
class OptionsOfQuestions(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    # 아래 예시와 같이 받기 위해 수정
    option_number = models.CharField(max_length=3, default=0)
    option_context = models.CharField(max_length=255, blank=True,)
# [
#     {
#         'option_number': 1, 'option_context': 'asdflkjsadfj',
#         'option_number': 2, 'option_context': 'asdflkjsadfj',
#         'option_number': 3, 'option_context': 'asdflkjsadfj',
#         'option_number': 4, 'option_context': 'asdflkjsadfj',
#     }
# ]

    class Meta:
        db_table = 'options_of_questions'


# 객관식
class MultipleAnswers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    options_of_question = models.ForeignKey(OptionsOfQuestions, on_delete=models.CASCADE)

    class Meta:
        db_table = 'multiple_answers'


# 주관식
class SubjectiveAnswers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    response = models.TextField()

    class Meta:
        db_table = 'subjective_answers'


# 객관식 통계
class Statistics(models.Model):
    options_of_question = models.ForeignKey(OptionsOfQuestions, on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        db_table = 'statistics'