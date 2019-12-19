# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities, Remote

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

    def test_needThreeWords(self):
        self.askPageOpen()
        self.page.clickLogin()
        self.page.login()
        self.page.open()

        self.page.setQuestionTheme('hello, world!')
        self.page.clickChooseAnother()
        self.page.clickSendQuestion()
        self.assertTrue(self.page.isAlert())

    def test_profile(self):
        self.askPageOpen()
        self.page.clickLogin()
        self.page.login()
        self.page.open()

        self.assertTrue(self.page.clickAndWaitProfile())

    def test_notEmptyQuestion(self):
        self.askPageOpen()
        self.page = AskPage(self.driver)
        self.page.open()

        shortQuestion = u'Why, man?'
        self.page.setQuestionTheme(shortQuestion)
        self.page.clearQuestionThemeByKeys()
        self.assertEqual(self.page.getAlertUnderAdditional(),
                         u'Поле «Тема вопроса» обязательно для заполнения')

    def test_mentionCountry(self):
        self.askPageOpen()
        questionWithCountry = u'Россия'
        self.page.setQuestionTheme(questionWithCountry)
        self.page.autosettingSubcategory(u'Политика')
        self.assertEqual(self.page.getSubcategory(),
                         u'Политика')

    def test_loginBtn_and_authorization(self):
        self.askPageOpen()
        self.page.clickLogin()
        self.assertTrue(self.page.lofinFormIsVisible())
        self.page.login()
        self.assertTrue(self.page.sameUrl("https://otvet.mail.ru"))

    def test_photoVideoUploadTest(self):
        self.askPageOpen()
        self.page.open_photo_upload_form()
        self.page.can_press_esc()

        self.page.open_video_upload_form()
        self.page.can_press_esc()

    def test_notValidTheme(self):
        self.askPageOpen()
        self.page.clickLogin()
        self.page.login()
        self.page.open()
        self.page.setQuestionTheme(u'ыв ыва ыва 23')
        self.page.clickSendQuestion()
        self.assertTrue(self.page.isAlert())

    def test_tooBigQuestion(self):
        self.askPageOpen()
        bigStr = u''
        for _ in range(122):
            bigStr = bigStr + u'a'
        self.page.setQuestionTheme(bigStr)
        self.assertEqual(self.page.getAlertUnderAdditional(),
                         u'Поле «Тема вопроса» не может '
                         u'быть больше 120 символов.')

    def test_newQuestionEditTest(self):
        self.askPageOpen()
        self.page.clickLogin()
        self.page.login()
        self.page.open()

        randTitle = self.page.getGetRandomTitle()
        self.page.setQuestionTheme(randTitle)
        self.page.setQuestionAdditional(u'Собственно говоря,'
                                        u'если греческий салат испортился,'
                                        u'то можно ли его называть '
                                        u'древнегреческим?')

        self.page.clickChooseAnother()
        self.page.make_default_question()

        self.assertTrue(self.page.can_edit_time())

    def test_settingsTest(self):
        self.askPageOpen()
        self.page.clickLogin()
        self.page.login()
        self.page.open()

        self.assertTrue(self.page.check_settings_page())

    def test_pollOptionsTest(self):
        self.page.open_poll_form()

        self.assertTrue(self.page.check_poll_option_correct_add())
