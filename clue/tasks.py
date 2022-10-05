from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    InvalidSessionIdException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from .models import *
from datetime import date
from .utils import worker_email


@shared_task()
def scrapCluee(data_set):
    if data_set:
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
        if not ClueMain.objects.filter(clue=cluu).exists():
            try:
                ser_obj = Service("/usr/local/bin/chromedriver")
            except InvalidSessionIdException:
                result.update({"scraping-error": True})
            options = Options()
            WINDOW_SIZE = "1920,1080"
            options.page_load_strategy = "eager"
            options.add_argument("--headless")
            options.add_argument("--window-size=%s" % WINDOW_SIZE)
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(service=ser_obj, options=options)
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
                except NoSuchElementException:
                    result.update({"scraping-error": True})
                except TimeoutException:
                    result.update({"scraping-error": True})
                except InvalidSessionIdException:
                    result.update({"scraping-error": True})
            if words:
                for word in words:
                    ClueMain.objects.create(clue=cluu, answer=word)
                result.update({"clue-found": True})
            else:
                result.update({"clue-not-found": True})
            driver.close()
        else:
            result.update({"already-exists": True})
    return result


@shared_task()
def res(x):
    clue_added = 0
    blog = Blog.objects.create(title=f"Blog created at {date.today()}")
    for i in x:
        for ii in i:
            if ii["clue-found"] == True:
                clue = ClueMain.objects.filter(clue=ii["word"]).first()
                if clue:
                    BlogClue.objects.create(blog=blog, clue=clue)
                    clue_added = clue_added + 1

    if BlogClue.objects.filter(blog=blog).exists():
        blog_created = True
        blog.clue_count = clue_added
        blog.save()
    else:
        blog_created = False
        Blog.objects.get(id=blog.id).delete()
    worker = WorkerResult.objects.create(
        clue_added=clue_added, data=x, blog_created=blog_created
    )
    worker_email(worker.id)
    return True
