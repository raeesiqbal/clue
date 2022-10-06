from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from django.db.models import Q
from tablib import Dataset
from django.contrib import messages
from .tasks import scrapCluee, res
from celery import group, chord


def index(request):
    search = request.GET.get("search", False)
    digits = request.GET.get("digits", False)
    answersFinal = []
    if search:
        # if ClueMain.objects.filter(clue__icontains=search).exists():
        clues = ClueMain.objects.filter(clue__icontains=search).distinct("answer")
        if digits:
            for clue in clues:
                if len(clue.answer) == int(digits) and clue not in answersFinal:
                    answersFinal.append(clue)
        else:
            answersFinal = clues
        context = {"clues": answersFinal, "search": search}
        return render(request, "answers.html", context)
    return render(request, "index.html")


def addClue(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "GET":
            return render(request, "add-clue.html")
        if request.method == "POST":
            new_resource = request.FILES["file"]
            dataset = Dataset()
            data_set = dataset.load(new_resource.read(), format="xlsx", headers=False)
            # scrapClue.delay(data_set)
            # scrapCluee.chunks(data_set, 1).group().apply_async()
            # jobs = group([scrapCluee.chunks(data_set, 1)])
            # jobs.apply_async()

            # callback = res.s()
            # header = [scrapCluee.chunks(data_set, 5).group()]
            # result = chord(header)(callback)
            callback = res.s()
            header = [scrapCluee.chunks(data_set, 100).group()]
            result = chord(header)(callback)
            return JsonResponse({"done": True}, safe=False)
        return redirect("add_clue")
    return redirect("index")


def myblog(request):
    blogs = Blog.objects.filter(active=True).order_by("-publish_date")
    context = {"blogs": blogs}
    return render(request, "new-blog.html", context)


def blog_detail(request, id):
    blog = Blog.objects.filter(id=id).first()
    if blog:
        blog_clues = BlogClue.objects.filter(blog=blog).order_by("-publish_date")
    else:
        messages.warning(request, "No such blog exists.")
        blog_clues = None
    context = {"blog_clues": blog_clues}
    return render(request, "blog-detail.html", context)


def clue_word(request, clue):
    clue_words = ClueMain.objects.filter(clue=clue).distinct("answer")
    if clue_words:
        return JsonResponse([word.serialize() for word in clue_words], safe=False)
    else:
        return JsonResponse({"empty": True}, safe=False)


def subscribeview(request):
    if request.method == "POST":
        mail = request.POST.get("email", False)
        if mail:
            makerecord = subscribe.objects.create(emailsub=mail)
            makerecord.save()
            return redirect("/")
        else:
            return redirect("/")
    return render(request, "subscribe.html")
