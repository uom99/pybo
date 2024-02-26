from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import questionForm
from ..models import question

@login_required(login_url='common:login')
def question_create(request):
  if request.method == 'POST':
    form = questionForm(request.POST)
    if form.is_valid():
      question = form.save(commit=False)
      question.author = request.user
      question.create_date = timezone.now()
      question.save()
      return redirect('pybo:index')
  else:
    form = questionForm()
  context = {'form': form}
  return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    questions = get_object_or_404(question, pk=question_id)
    if request.user != questions.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=questions.id)
    if request.method == "POST":
        form = questionForm(request.POST, instance=questions)
        if form.is_valid():
            questions = form.save(commit=False)
            questions.modify_date = timezone.now()  # 수정일시 저장
            questions.save()
            return redirect('pybo:detail', question_id=questions.id)
    else:
        form = questionForm(instance=questions)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    questions = get_object_or_404(question, pk=question_id)
    if request.user != questions.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=questions.id)
    questions.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    questions = get_object_or_404(question, pk=question_id)
    if request.user == questions.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        questions.voter.add(request.user)
    return redirect('pybo:detail', question_id=questions.id)
