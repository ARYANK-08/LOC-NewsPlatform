from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm
from django.contrib.auth.decorators import login_required

@login_required
def like_post(request):
    if request.method == 'POST' and request.is_ajax():
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        question.likes += 1
        question.save()
        return JsonResponse({'likes': question.likes})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def like_answer(request):
    if request.method == 'POST' and request.is_ajax():
        answer_id = request.POST.get('answer_id')
        answer = get_object_or_404(Answer, pk=answer_id)
        answer.likes += 1
        answer.save()
        return JsonResponse({'likes': answer.likes})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def like_comment(request):
    if request.method == 'POST' and request.is_ajax():
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.likes += 1
        comment.save()
        return JsonResponse({'likes': comment.likes})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def chat(request):
    return render(request, 'social.html')

@login_required
def community_chat(request):
    # Retrieve all questions along with their answers and comments
    questions = Question.objects.prefetch_related('answer_set__comment_set').all()
    return render(request, 'social.html', {'questions': questions})

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('community_chat')
    else:
        form = QuestionForm()
    return render(request, 'ask_question.html', {'form': form})

@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('community_chat')
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})

@login_required
def comment_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.answer = answer
            comment.save()
            return redirect('community_chat')
    else:
        form = CommentForm()
    return render(request, 'comment_answer.html', {'form': form, 'answer': answer})
