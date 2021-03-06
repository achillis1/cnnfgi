# -*- coding: utf-8 -*-
import smtplib
import time
import codecs
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from cnnfgi.settings import EMAIL_PROVIDER, PHANTOMJS_PATH
from cnnfgiapp.models import Fgi
from cnnfgiapp.management.commands import SendEmail_Base

from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        t = datetime.now()
        hr = t.hour
        wkday = t.isoweekday()

        if wkday < 6:
            if hr > 7 and hr < 16:
                phantomjs_path = PHANTOMJS_PATH + "/phantomjs"
                driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)
                driver.wait = WebDriverWait(driver, 5)
                driver.get("http://money.cnn.com/data/fear-and-greed/")
                try:
                    cr = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#needleChart")))
                    indexes = cr.find_elements_by_tag_name("li")
                    for index in indexes:
                        f1 = index.get_attribute("innerHTML").find("Greed Now:")
                        f2 = index.get_attribute("innerHTML").find("Greed Previous Close:")
                        f3 = index.get_attribute("innerHTML").find("Greed 1 Week Ago:")
                        f4 = index.get_attribute("innerHTML").find("Greed 1 Month Ago:")
                        f5 = index.get_attribute("innerHTML").find("Greed 1 Year Ago:")

                        if f1!=-1:
                            fgi_now = index.get_attribute("innerHTML")[f1+11:f1+11+2]
                        if f2!=-1:
                            fgi_previous_close = index.get_attribute("innerHTML")[f2+22:f2+22+2]
                        if f3!=-1:
                            fgi_one_week_ago = index.get_attribute("innerHTML")[f3+18:f3+18+2]
                        if f4!=-1:
                            fgi_one_month_ago = index.get_attribute("innerHTML")[f4+19:f4+19+2]
                        if f5!=-1:
                            fgi_one_year_ago = index.get_attribute("innerHTML")[f5+18:f5+18+2]

                    try:
                        last_fgi = Fgi.objects.latest('id')
                        if last_fgi.index != fgi_now:

                            fgi_index = Fgi(
                                index=fgi_now,
                                previous_close=fgi_previous_close,
                                one_week_ago=fgi_one_week_ago,
                                one_month_ago=fgi_one_month_ago,
                                one_year_ago=fgi_one_year_ago,
                                week_day=datetime.now().strftime("%a")
                                )
                            fgi_index.save()
                            to = 'dingstaging1@gmail.com'
                            subject = 'FG Index is ' + str(fgi_now) + ' at ' + datetime.now().strftime('%a, %b %d %Y %H:%M:%S')
                            html_body = ''
                            SendEmail_Base.Send(to, subject, html_body, EMAIL_PROVIDER, None, None, None, None, fgi_now, None, None, None, False, None, None)


                        else:
                            print('skip this record since it stays the same')


                    except:
                        if Fgi.objects.all().count() == 0:
                            fgi_index = Fgi(
                                index=fgi_now,
                                previous_close=fgi_previous_close,
                                one_week_ago=fgi_one_week_ago,
                                one_month_ago=fgi_one_month_ago,
                                one_year_ago=fgi_one_year_ago,
                                week_day=timezone.now().weekday()
                                )
                            fgi_index.save()
                        else:
                            print("try error")
                            pass
                except TimeoutException:
                    print("except timeout error")
                    pass

                driver.quit()
