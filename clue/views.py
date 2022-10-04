from enum import EnumMeta
from queue import Empty
import re
from telnetlib import STATUS
from turtle import delay
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from django.db.models import Q
from tablib import Dataset
from django.contrib import messages
from .tasks import scrapCluee, res
from celery import group, chord
import csv
import sys
import codecs
from io import StringIO
import io
from django.http import HttpResponse
import xlsxwriter


def index(request):
    search = request.GET.get("search", False)
    digits = request.GET.get("digits", False)
    answersFinal = []
    if search:
        if Clue.objects.filter(clue=search).exists():
            clue = Clue.objects.filter(clue=search).first()
            clues = Word.objects.filter(clue=clue)
            if digits:
                for clue in clues:
                    if len(clue.word) == int(digits) and clue.clue not in answersFinal:
                        answersFinal.append(clue)
            else:
                answersFinal = clues
                # for clue in clues:
                #     if clue.word not in answersFinal:
                #         answersFinal.append(clue.clue)
        context = {"clues": answersFinal, "search": search}
        return render(request, "answers.html", context)
    return render(request, "index.html")


def addClue(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "GET":
            print(WorkerResult.objects.filter().first())
            return render(request, "add-clue.html")
        if request.method == "POST":
            new_resource = request.FILES["file"]
            dataset = Dataset()
            data_set = dataset.load(new_resource.read(), format="xlsx", headers=False)
            # scrapClue.delay(data_set)
            # scrapCluee.chunks(data_set, 1).group().apply_async()
            # jobs = group([scrapCluee.chunks(data_set, 1)])
            # jobs.apply_async()
            callback = res.s()
            header = [scrapCluee.chunks(data_set, 5).group()]
            result = chord(header)(callback)
            # print("i am result", result.get())
            return JsonResponse({"done": True}, safe=False)
        return redirect("add_clue")
    return redirect("index")


# def addDb(request):
#     if request.user.is_authenticated and request.user.is_superuser == True:
#         if request.method == "GET":
#             return render(request, "add-db.html")
#         if request.method == "POST":
#             new_resource = request.FILES["file"]
#             dataset = Dataset()
#             data_set = dataset.load(new_resource.read(), format="xlsx", headers=True)
#             # for i in data_set:
#             #     print(i)
#             # callback = ress.s()
#             # header = [addDbTask.chunks(data_set, 5).group()]
#             # result = chord(header)(callback)
#             return JsonResponse({"done": True}, safe=False)
#         return redirect("add_clue")
#     return redirect("index")


def addDb(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "GET":
            return render(request, "t.html")
        if request.method == "POST":
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()
            col = 0
            row = 0
            file = request.FILES["file"]
            content = StringIO(file.read().decode("latin-1"))
            read_tsv = csv.reader(content, delimiter="\t")
            maxInt = sys.maxsize
            while True:
                try:
                    csv.field_size_limit(maxInt)
                    break
                except OverflowError:
                    maxInt = int(maxInt / 10)
            for roww, i in enumerate(read_tsv):
                print(roww)
                if roww < 70000:
                    worksheet.write(row, col, i[0])
                    col = col + 1
                    worksheet.write(row, col, i[1])
                    col = col + 1
                    worksheet.write(row, col, i[2])
                    col = col + 1
                    worksheet.write(row, col, i[3])
                    col = 0
                    row = row + 1
                else:
                    break
            workbook.close()
            output.seek(0)
            filename = "r_10_15.xlsx"
            response = HttpResponse(
                output,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=%s" % filename
            return response
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
    print(blog_clues)
    context = {"blog_clues": blog_clues}
    return render(request, "blog-detail.html", context)


def clue_word(request, id):
    clue = Clue.objects.filter(id=id).first()
    print("c", clue)
    clue_words = Word.objects.filter(clue=clue).order_by("-publish_date")
    print("w", clue_words)
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


def runThread(request):
    # thrd = threading.Thread(target=tsv_db)
    # thrd.setDaemon(True)
    # thrd.start()
    return redirect("/")
