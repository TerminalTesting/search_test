#! /usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class SearchTest(unittest.TestCase):
        
    def setUp(self):
        """Инициализация переменных для всех тестов"""
        self.TEXT_FILE = open('%s/search_words.csv' % os.getenv('WORKSPACE'), 'r')
        self.HOST = 'http://%s.%s/' % (os.getenv('CITY'), os.getenv('HOST'))
        self.browser = webdriver.Firefox()
        self.ARTSOURCE = '%sartifact/' % os.getenv('BUILD_URL')
        

    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""
        self.browser.close()
        self.TEXT_FILE.close()
        if sys.exc_info()[0]:   
            print sys.exc_info()[0]

    def is_element_present(self, how, what, timeout=10):
        """ Поиск элемента по локатору

            По умолчанию таймаут 10 секунд, не влияет на скорость выполнения теста
            если элемент найден, если нет - ждет его появления 10 сек
            
            Параметры:
               how - метод поиска
               what - локатор
            Методы - атрибуты класса By:
             |  CLASS_NAME = 'class name'
             |  
             |  CSS_SELECTOR = 'css selector'
             |  
             |  ID = 'id'
             |  
             |  LINK_TEXT = 'link text'
             |  
             |  NAME = 'name'
             |  
             |  PARTIAL_LINK_TEXT = 'partial link text'
             |  
             |  TAG_NAME = 'tag name'
             |  
             |  XPATH = 'xpath'
                                             """
	try:
            return WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
	except:
            print u'Элемент не найден'
	    print 'URL: ', self.browser.current_url
	    print u'Метод поиска: ', how
	    print u'Локатор: ', what
	    screen_name = '%d.png' % int(time.time())
	    self.browser.get_screenshot_as_file(screen_name)
	    print u'Скриншот страницы: ', self.ARTSOURCE + screen_name
	    raise Exception('ElementNotPresent')



    def test_search(self):

        cnt=0 #счетчик ошибок теста
        element = self.is_element_present
       
        line_cnt=0 #счетчик строк теста
        if os.path.getsize('%s/search_words.csv' % os.getenv('WORKSPACE'))==0: #проверка на то, что файл не пустой
            raise Exception('\nSearching file is empty')
            
        for line in self.TEXT_FILE:
                
            line_cnt+=1
            if line.count(';') != 1: #проверка на то, что строка оформлена правильно
                print 'Некорректная строка поискового файла:'
                print 'Номер строки: %s' % line_cnt
                print '-'*80
                cnt+=1
                    
            else:    
                sline = line.strip().split(';')#строка конвертируется в список по символу-разделителю
                self.browser.get('%ssearch/?q=%s' %(self.HOST, sline[0]))

                try:
                    search_title = element(By.CLASS_NAME, 'componentHeader').text
                    search_field = element(By.CLASS_NAME, 'search-string').get_attribute('value')

                except NoSuchElementException: #элементы на странице не найдены, соответственно либо страница вернулась с ошибкой, либо не правильный урл
                    cnt+=1
                    print '%ssearch/?q=%s' %(self.HOST, sline[0])
                    print 'Нужные элементы на странице не найдены. Возможна ошибка в адресе, либо страница вернулась с ошибкой'
                    print 'Номер строки: %s' % line_cnt
                    print '-'*80
                    continue

                
                if sline[1] != '0':
                        
                    if sline[1].decode('utf-8', 'ignore') not in search_title: #проверка корректности заголовка поиска
                        print 'Некорректный заголовок поиска:'
                        print 'Строка для поиска: %s' % sline[0]
                        print 'Ожидалось: Вы искали: «%s»' % sline[1], '  Получено: ', search_title.encode('utf-8', 'ignore')
                        print 'Номер строки: %s' % line_cnt
                        print '-'*80
                        cnt+=1
                    if sline[1].decode('utf-8', 'ignore') not in search_field: #проверка корректности значения в поле поиска
                        print 'Некорректное значение в поле поиска:'
                        print 'Строка для поиска: %s' % sline[0]
                        print 'Ожидалось: ', sline[1], '  Получено: ', search_field#.encode('utf-8', 'ignore')
                        print 'Номер строки: %s' % line_cnt
                        print '-'*80
                        cnt+=1

                else:
                    if u'Упс, ничего не нашлось?' not in search_title: #проверка корректности заголовка поиска при нулевом поиске
                        print 'Некорректный заголовок поиска:'
                        print 'Строка для поиска: %s' % sline[0]
                        print 'Ожидалось: Упс, ничего не нашлось?', '  Получено: ', search_title.encode('utf-8', 'ignore')
                        print 'Номер строки: %s' % line_cnt
                        print '-'*80
                        cnt+=1
        print '-'*29
        print '|   Строк проверено - %s   |' % line_cnt
        print '-'*29
                                           
        assert cnt==0, (u'Errors found: %d')%(cnt)
        
    
