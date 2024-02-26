from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import answerForm
from ..models import question, answer

@login_required(login_url='common:login')
def answer_create(request, question_id):
  questions = get_object_or_404(question, pk=question_id)
  if request.method == "POST":
    form = answerForm(request.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.author = request.user
      answer.create_date = timezone.now()
      answer.question = questions
      answer.save()
      return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=questions.id), answer.id))
  else:
    form = answerForm()
  context = {'question':questions, 'form': form}
  return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answers = get_object_or_404(answer, pk=answer_id)
    if request.user != answers.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answers.question.id)
    if request.method == "POST":
        form = answerForm(request.POST, instance=answers)
        if form.is_valid():
            answers = form.save(commit=False)
            answers.modify_date = timezone.now()
            answers.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answers.question.id), answers.id))
    else:
        form = answerForm(instance=answers)
    context = {'answer': answers, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answers = get_object_or_404(answer, pk=answer_id)
    if request.user != answers.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answers.delete()
    return redirect('pybo:detail', question_id=answers.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answers = get_object_or_404(answer, pk=answer_id)
    if request.user == answers.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answers.voter.add(request.user)
        return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answers.question.id), answers.id))