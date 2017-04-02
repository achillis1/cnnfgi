# -*- coding: utf-8 -*-
import smtplib
import datetime
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

from cnnfgi.settings import EMAIL_PROVIDER
from cnnfgiapp.models import Fgi
from cnnfgiapp.management.commands import SendEmail_Base

from django.utils import timezone

#python manage.py   SendEmail     email    content_id      general_param
#                 (mgt command)   (To:)    (various)         (various)

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        phantomjs_path = "/usr/local/bin/phantomjs"
        driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)

        # driver = webdriver.Firefox()
        driver.wait = WebDriverWait(driver, 5)
        driver.get("http://money.cnn.com/data/fear-and-greed/")
        try:
            cr = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#needleChart")))
            indexes = cr.find_elements_by_tag_name("li")
            for index in indexes:
                # print(index.get_attribute("innerHTML"))
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

                fgi_index = Fgi(
                    index=index.get_attribute("innerHTML")[f1+11:f1+11+2] if f1!=-1 else '',
                    previous_close=index.get_attribute("innerHTML")[f2+22:f2+22+2] if f2!=-1 else '',
                    one_week_ago=index.get_attribute("innerHTML")[f3+18:f3+18+2] if f3!=-1 else '',
                    one_month_ago=index.get_attribute("innerHTML")[f4+19:f4+19+2] if f4!=-1 else '',
                    one_year_ago=index.get_attribute("innerHTML")[f5+18:f5+18+2] if f5!=-1 else '',
                    week_day=
                    )
            return index.get_attribute("innerHTML")
        except TimeoutException:
            print("Get greed error")



        driver.quit()

