from django.core.management.color import no_style
from django.db import connection
from clue.models import ClueMain
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Displays current time"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Give a csv file.")

    def handle(self, *args, **kwargs):
        file = kwargs["file"]
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [ClueMain])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
        return "ok"
