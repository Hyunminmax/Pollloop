from django.db import models
from user.models import CustomUser
import uuid as uuid_lib

class Form(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="제목")
    tag = models.CharField(max_length=255, verbose_name="태그")
    create_at = models.DateField(auto_now_add=True)
    end_at = models.DateField()
    is_closed = models.BooleanField(default=False, help_text="상태") #ENUM값으로 변경해야함
    access_code = models.CharField(max_length=255, verbose_name="입장코드", null=True, blank=True)
    subtitle = models.CharField(max_length=255, verbose_name="부 제목")
    form_description = models.CharField(max_length=255, help_text="상세 내용")
    uuid = models.UUIDField(default=uuid_lib.uuid4, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'form'

# Form참여 인원
class Respondent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'respondent'


# 질문
class Questions(models.Model):
    LAYOUT_CHOICES = [
        ('단답형', '단답형'),
        ('장문형', '장문형'),
        ('체크박스', '체크박스'),
        ('라디오', '라디오'),
        ('드롭다운', '드롭다운'),
        ('범위 선택', '범위 선택'),
        ('별점', '별점'),
        ('이미지 선택', '이미지 선택'),
        ('숫자', '숫자'),
        ('날짜', '날짜'),
        ('이메일', '이메일'),
        ('파일업로드', '파일업로드'),
    ]
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    layout_type = models.CharField(choices=LAYOUT_CHOICES, max_length=255)
    question = models.TextField()
    is_required = models.BooleanField(default=False)

    class Meta:
        db_table = 'questions'

# 보기
class OptionsOfQuestions(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option_context = models.CharField(max_length=255)

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