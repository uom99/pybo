from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import question

def index(request):
  page = request.GET.get('page', 'i')
  kw = request.GET.get('kw', '') #검색어
  question_list = question.objects.order_by('-create_date')
  if kw:
      question_list = question_list.filter(
          Q(subject__icontains=kw) | #제목
          Q(content__icontains=kw) | #내용
          Q(answer__content__icontains=kw) | #답변내용
          Q(author__username__icontains=kw) | #질문 글쓴이
          Q(answer__author__username__icontains=kw) #답변 글쓴이
      ).distinct()
  paginator = Paginator(question_list, 10)
  page_obj = paginator.get_page(page)
  context = {'question_list': page_obj, 'page': page, 'kw': kw}
  return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
  questions = get_object_or_404(question, pk=question_id)
  context = {'question': questions}
  return render(request, 'pybo/question_detail.html', context)