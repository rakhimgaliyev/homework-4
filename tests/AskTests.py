# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import unittest

from tests.AskPage import AskPage


class AskTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AskTests, self).__init__(*args, **kwargs)

    def askPageOpen(self):
        self.page = AskPage(self.driver)
        self.page.open()

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        self.page = AskPage(self.driver)
        self.page.open()

    def tearDown(self):
        self.driver.quit()

    def test_need_three_words(self):
        self.page.click_login_button()
        self.page.login()

        self.page.set_question_title(u'Hello, world!')
        self.page.set_question_category(u'Другое')
        self.page.click_send_question()
        self.assertEqual(self.page.get_alert_message(), \
            u'Просьба более подробно и грамотно сформулировать тему вопроса.')

    def test_profile(self):
        self.page.click_login_button()
        self.page.login()

        description = 'i can speak uk'
        self.page.edit_profile_description(description)
        self.page.refresh_page()
        self.assertEqual(self.page.get_profile_description(), description)

    def test_not_empty_question(self):
        self.page.set_question_title(u'Алло, Галочка!?')
        self.page.clear_question_theme_by_keys()
        self.assertEqual(self.page.get_alert_under_additional(),
                         u'Поле «Тема вопроса» обязательно для заполнения')

    def test_question_category_swich(self):
        self.page.set_question_title(u'Овен')
        self.page.set_question_category(u'Юмор')
        self.assertEqual(self.page.get_question_category(),
                         u'Юмор')

    def test_login_and_authorization(self):
        self.page.click_login_button()
        self.page.login()

        self.assertIn(self.page.BASE_URL, self.page.get_url())

    def test_photo_and_video_upload(self):
        self.page.click_login_button()
        self.page.login()

        self.page.open_photo_upload_form()
        self.assertIsNotNone(self.page.get_photo_upload_section())
        self.page.press_esc()

        self.page.open_video_upload_form()
        self.assertEqual(self.page.UPLOAD_VIDEO_WINDOW_URL, self.page.get_video_upload_section())

    def test_not_valid_question_title(self):
        self.page.click_login_button()
        self.page.login()
        self.page.set_question_title(u'ыв ыва ыва 23')

        self.page.set_question_category(u'Другое')

        self.page.click_send_question()
        self.assertEqual(self.page.get_alert_message(), \
            u'Просьба более подробно и грамотно сформулировать тему вопроса.')

    def test_too_big_question(self):
        bigStr = u''
        for _ in range(122):
            bigStr = bigStr + u'a'
        self.page.set_question_title(bigStr)
        self.assertEqual(self.page.get_alert_under_additional(),
                         u'Поле «Тема вопроса» не может '
                         u'быть больше 120 символов.')

    def test_new_question_edit(self):
        self.page.click_login_button()
        self.page.login()

        randTitle = self.page.get_random_title()
        self.page.set_question_title(randTitle)
        self.page.set_question_additional(u'Собственно говоря,'
                                          u'если греческий салат испортился,'
                                          u'то можно ли его называть '
                                          u'древнегреческим?')

        self.page.set_question_category('Другое')
        self.page.click_send_question()
        self.page.wait_for_swich_to_question_page()

        newTilte = u'А можно тесты сдать?'

        self.page.click_edit_question()
        self.page.edit_question_title(newTilte)
        self.page.save_edited_question()
        self.page.wait_for_question_title_change(newTilte)

        currentTitle = self.page.get_question_title()
        self.assertEqual(currentTitle, newTilte)

    def test_poll_options(self):
        self.page.open_poll_form()

        self.assertIsNotNone(self.page.get_poll_section())

        self.page.set_text_to_poll_option(3, u'Тестовая_строка_1')
        self.assertEqual(self.page.get_text_of_poll_option(3), 
            u'Тестовая_строка_1')

        self.page.set_text_to_poll_option(4, u'Тестовая_строка_2')
        self.assertEqual(self.page.get_text_of_poll_option(4), 
            u'Тестовая_строка_2')

        self.page.set_text_to_poll_option(5, u'Тестовая_строка_3')
        self.assertEqual(self.page.get_text_of_poll_option(5), 
            u'Тестовая_строка_3')

