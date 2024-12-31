from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from .models import Form, Respondent, Questions, OptionsOfQuestions, MultipleAnswers, SubjectiveAnswers


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


# Form 요약
class FormDetailView(View):
    def get(self, request, form_id):
        form = get_object_or_404(Form, id=form_id)
