import re
from django.shortcuts import redirect, render
from . models import newblog
from django.db.models import Q
from .TsvToDB import tsv_db
import threading

def newblog(request):
    records = newblog.objects.all()
    context = {
        'records' : records
    }
    return render(request, "blog.html", context)
