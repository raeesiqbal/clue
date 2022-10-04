from django.core.management.base import BaseCommand

# import tablib
from clue.models import *

# from clue.tasks import scrapCluee, res, addDbTask, ress
# from celery import group, chord
import csv
import sys


class Command(BaseCommand):
    help = "Displays current time"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Give a csv file.")

    def handle(self, *args, **kwargs):
        file = kwargs["file"]

        tsv_file = open("clues.tsv", encoding="utf8")
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        maxInt = sys.maxsize
        while True:
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt / 10)
        for count, row in enumerate(read_tsv):
            if row[3] and row[2]:
                if not Clue.objects.filter(clue=row[3]).exists():
                    clue = Clue.objects.create(clue=row[3])
                else:
                    clue = Clue.objects.get(clue=row[3])
                if not Word.objects.filter(clue=clue, word=row[2]).exists():
                    Word.objects.create(clue=clue, year=row[1], word=row[2])
            print(row[3])
            print(count)
        # dataset = tablib.Dataset()
        # dataset.xlsx = open(file, "rb").read()
        # callback = ress.s()
        # header = [addDbTask.chunks(dataset, 1000).group()]
        # result = chord(header)(callback)
        # print("done")
