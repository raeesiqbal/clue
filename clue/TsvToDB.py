import csv
import sys
from .models import cluemain


def tsv_db():
    print("Here")
    tsv_file = open("./clue/clues.tsv", encoding="utf8")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    maxInt = sys.maxsize
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    for count, row in enumerate(read_tsv):
        print("Started: ", count)
        try:
            # if i < 24:
            #     print(f"{i}.\n{row[-2]}-{row[-1]}")
            #     i += 1
            if not cluemain.objects.filter(
                clue=row[-2], answer=row[-1], year=int(row[-3])
            ).exists():
                clue = cluemain.objects.create(
                    clue=row[-2], answer=row[-1], year=int(row[-3])
                )
                print("Clue: ", clue.id)
            else:
                print("Clue already exists")
        except ConnectionError:
            print("Connection Error")
            break
        except Exception as e:
            print(f"On Count: {count}, ", e)
            pass
    tsv_file.close()
