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
        self.TEXT_FILE = open('search_words', 'r')
        self.HOST = 'http://%s.%s/' % (os.getenv('CITY'), os.getenv('HOST'))
        self.browser = webdriver.Firefox()
        

    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""
        self.browser.close()
        self.TEXT_FILE.close()
        if sys.exc_info()[0]:   
            print sys.exc_info()[0]


    

    def test_search(self):

        cnt=0 #счетчик ошибок теста

       
        line_cnt=0 #счетчик строк теста
        if os.path.getsize('%s/search_words' % os.getenv('WORKSPACE'))==0: #проверка на то, что файл не пустой
            raise Exception('\nSearching file is empty\nAre you sure it`s been upload')
            
        for line in self.TEXT_FILE:
                
            line_cnt+=1
            if line.count(';') != 1: #проверка на то, что строка оформлена правильно
                print 'Некорректная строка поискового файла:'
                print 'Номер строки: %s' % line_cnt
                print '-'*80
                cnt+=1
                    
            else:    
                sline = line.strip().split(';')
                self.browser.get('%ssearch/?q=%s' %(self.HOST, sline[0]))

                try:
                    search_title = self.browser.find_element_by_class_name('componentHeader').text
                    search_field = self.browser.find_element_by_class_name('search-string').get_attribute('value')

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
             
                                           
        assert cnt==0, (u'Errors found: %d')%(cnt)
        
    
