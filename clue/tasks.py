from celery import shared_task
from core.celery import app
from celery_progress.backend import ProgressRecorder
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    InvalidSessionIdException,
    WebDriverException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tablib import Dataset
from .models import *
from datetime import date
from .utils import worker_email


@shared_task(bind=True)
def scrapClue(self, data_set):
    # progress_recorder = ProgressRecorder(self)
    try:
        ser_obj = Service("C:/c/chromedriver.exe")
        options = Options()
        options.page_load_strategy = "eager"
        driver = webdriver.Chrome(service=ser_obj, options=options)
        word_dic = {}
        result_dic = {}
        clue_added = 0
        clue_not_found = []
        blog_created = False
        blog = Blog.objects.create(title="Updated Clue list at {}".format(date.today()))
        for key, i in enumerate(data_set):
            if i[0]:
                clu = str(i[0].strip())
                u = str(i[0].strip())
                cluu = u.strip()
                # progress_recorder.set_progress(
                #     key + 1, len(data_set), f"Worker is processing clue: {key}"
                # )
                words = []
                if not Clue.objects.filter(clue=cluu).exists():
                    print(key)
                    print(Clue.objects.filter(clue=clu).exists())
                    try:
                        clu = "-".join(clu.split())
                        driver.get("https://crossword-solver.io/clue/{}/".format(clu))
                        body = driver.find_element(By.TAG_NAME, "tbody")
                        cells = body.find_elements(By.TAG_NAME, "tr")
                        for cell in cells:
                            tds = cell.find_elements(By.TAG_NAME, "td")
                            for idx, td in enumerate(tds):
                                if idx == 1:
                                    words.append(td.text)
                                if idx == 0:
                                    num = td.text.replace("%", "")
                                    if num:
                                        print("raees", num)
                                        if int(num) >= 85:
                                            pass
                                        else:
                                            break
                        if not words:
                            clu = "-".join(clu.split())
                            driver.get(
                                "https://www.dictionary.com/e/crosswordsolver/{}/".format(
                                    clu
                                )
                            )
                            try:
                                mytable = driver.find_element(
                                    By.CLASS_NAME, "solver-table"
                                )
                                cells = mytable.find_elements(
                                    By.CLASS_NAME, "solver-table__row"
                                )
                                for index, cell in enumerate(cells):
                                    if index > 0:
                                        tds = cell.find_elements(
                                            By.CLASS_NAME, "solver-table__cell"
                                        )
                                        first = None
                                        for idx, td in enumerate(tds):
                                            if idx == 0:
                                                first = td.text
                                            if idx == 1:
                                                num = td.text.replace("%", "")
                                                if num:
                                                    if int(num) >= 90:
                                                        words.append(first)
                            except NoSuchElementException:
                                print("second site no such element", i[0])
                            except TimeoutException:
                                print("second site time out error", i[0])
                        if not words:
                            clu = "+".join(clu.split())
                            driver.get(
                                "https://www.the-crossword-solver.com/word/{}/".format(
                                    clu
                                )
                            )
                            try:
                                mytable = driver.find_element(By.CLASS_NAME, "clues")
                                body = driver.find_elements(By.TAG_NAME, "tbody")
                                for ii in body:
                                    cells = ii.find_elements(By.TAG_NAME, "tr")
                                    for index, cell in enumerate(cells):
                                        if index > 1:
                                            tds = cell.find_elements(By.TAG_NAME, "td")
                                            for idx, td in enumerate(tds):
                                                if idx == 1 and td.text:
                                                    words.append(str(td.text))
                                                    print(words)
                                word_dic[i[0]] = words
                            except NoSuchElementException:
                                print("third site no such element", i[0])
                            except TimeoutException:
                                print("third site no such element", i[0])
                        if words:
                            clue = Clue.objects.create(clue=cluu)
                            for word in words:
                                clue_added = clue_added + 1
                                Word.objects.create(clue=clue, word=word)
                                BlogClue.objects.create(blog=blog, clue=clue)
                                print("word created")
                        else:
                            print("not found")
                            clue_not_found.append(i[0])
                        word_dic[i[0]] = words
                    except NoSuchElementException:
                        print("nosuchelement")
                    except TimeoutException:
                        print("timeout")
                else:
                    print("exists")
        result_dic["total clues"] = len(data_set)
        result_dic["total clue added"] = clue_added
        result_dic["total clue not found"] = len(clue_not_found)
        result_dic["clue not found"] = clue_not_found
        if clue_added != 0:
            blog_created = True
        result_dic["blog created"] = blog_created
        driver.close()
    except InvalidSessionIdException:
        pass
    return result_dic


@shared_task()
def scrapCluee(data_set):
    if data_set:
        print(data_set)
        clu = str(data_set.strip())
        cluu = str(data_set.strip())
        words = []
        result = {
            "word": cluu,
            "scraping-error": False,
            "already-exists": False,
            "clue-not-found": False,
            "clue-found": False,
        }
        if not Clue.objects.filter(clue=cluu).exists():
            try:
                ser_obj = Service(
                    "C:/Users/Muhammad Raees/OneDrive/Desktop/selenium/selenium/chromedriver.exe"
                )
            except InvalidSessionIdException:
                result.update({"scraping-error": True})
            options = Options()
            options.page_load_strategy = "eager"
            driver = webdriver.Chrome(service=ser_obj, options=options)
            print("not exists", cluu)
            try:
                clu = "-".join(clu.split())
                driver.get("https://crossword-solver.io/clue/{}/".format(clu))
                body = driver.find_element(By.TAG_NAME, "tbody")
                cells = body.find_elements(By.TAG_NAME, "tr")
                for cell in cells:
                    tds = cell.find_elements(By.TAG_NAME, "td")
                    for idx, td in enumerate(tds):
                        if idx == 1:
                            words.append(td.text)
                        if idx == 0:
                            num = td.text.replace("%", "")
                            if num:
                                if int(num) >= 85:
                                    pass
                                else:
                                    break
            except NoSuchElementException:
                result.update({"scraping-error": True})
            except TimeoutException:
                result.update({"scraping-error": True})
            except InvalidSessionIdException:
                result.update({"scraping-error": True})
            if not words:
                clu = "-".join(clu.split())
                driver.get(
                    "https://www.dictionary.com/e/crosswordsolver/{}/".format(clu)
                )
                try:
                    mytable = driver.find_element(By.CLASS_NAME, "solver-table")
                    cells = mytable.find_elements(By.CLASS_NAME, "solver-table__row")
                    for index, cell in enumerate(cells):
                        if index > 0:
                            tds = cell.find_elements(
                                By.CLASS_NAME, "solver-table__cell"
                            )
                            first = None
                            for idx, td in enumerate(tds):
                                if idx == 0:
                                    first = td.text
                                if idx == 1:
                                    num = td.text.replace("%", "")
                                    if num:
                                        if int(num) >= 90:
                                            words.append(first)
                except NoSuchElementException:
                    result.update({"scraping-error": True})
                except TimeoutException:
                    result.update({"scraping-error": True})
                except InvalidSessionIdException:
                    result.update({"scraping-error": True})
            if not words:
                clu = "+".join(clu.split())
                driver.get("https://www.the-crossword-solver.com/word/{}/".format(clu))
                try:
                    mytable = driver.find_element(By.CLASS_NAME, "clues")
                    body = driver.find_elements(By.TAG_NAME, "tbody")
                    for ii in body:
                        cells = ii.find_elements(By.TAG_NAME, "tr")
                        for index, cell in enumerate(cells):
                            if index > 1:
                                tds = cell.find_elements(By.TAG_NAME, "td")
                                for idx, td in enumerate(tds):
                                    if idx == 1 and td.text:
                                        words.append(str(td.text))
                                        print(words)
                except NoSuchElementException:
                    result.update({"scraping-error": True})
                except TimeoutException:
                    result.update({"scraping-error": True})
                except InvalidSessionIdException:
                    result.update({"scraping-error": True})
            if words:
                clue = Clue.objects.create(clue=cluu)
                for word in words:
                    Word.objects.create(clue=clue, word=word)
                print("word created")
                result.update({"clue-found": True})
            else:
                result.update({"clue-not-found": True})
                print("not found")
            driver.close()
        else:
            result.update({"already-exists": True})
            print("exists")
    return result


@shared_task()
def res(x):
    print(x)
    clue_added = 0
    blog = Blog.objects.create(title=f"Blog created at {date.today()}")
    for i in x:
        for ii in i:
            if ii["clue-found"] == True:
                print(ii["word"])
                clue = Clue.objects.filter(clue=ii["word"]).first()
                if clue:
                    print("yes")
                    BlogClue.objects.create(blog=blog, clue=clue)
                else:
                    print("no")
                clue_added = clue_added + 1
    if BlogClue.objects.filter(blog=blog).exists():
        blog_created = True
    else:
        blog_created = False
        Blog.objects.get(id=blog.id).delete()
    worker = WorkerResult.objects.create(
        clue_added=clue_added, data=x, blog_created=blog_created
    )
    blog.clue_count = clue_added
    blog.save()
    worker_email(worker.id)
    return True


@shared_task(bind=True)
def addDb(self, data_set):
    for count, row in enumerate(data_set):
        if row[3] and row[2]:
            if not Clue.objects.filter(clue=row[3]).exists():
                clue = Clue.objects.create(clue=row[3])
            else:
                clue = Clue.objects.get(clue=row[3])
            if not Word.objects.filter(clue=clue, word=row[2]).exists():
                Word.objects.create(clue=clue, year=row[1], word=row[2])
        print(count)
    return True


@shared_task(bind=True)
def r(self, data_set):
    print(data_set)
    return True


@shared_task()
def ress(x):
    worker_email("DB")
    return True
