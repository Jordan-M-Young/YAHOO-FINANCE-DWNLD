# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 18:33:56 2019

@author: Jordan
"""

import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import shutil
import csv
import os

def get_bad_tickers(path):
    if os.path.exists(path):
        bad_tickers = pd.read_csv(path)
        bad_tickers = list(bad_tickers.iloc[:,1])
    else:
        bad_tickers = []
    
    return bad_tickers

def check_downloads_yahoo(tickers,directory):
    """checks working directory for downloaded stock files
    prevents going over per day limit"""
    files = []
    for ticker in tickers:
        filename = directory + '/' + ticker + '.csv'
        if os.path.exists(filename):
            files.append(ticker)
    return files


def open_list(file):
    """opens and formats downloaded stock data from nasdaq.com"""
    #makes sure the input filename has '.csv' extension
    if '.csv' in file:
        filename = file
    else:
        filename = file + '.csv'
    
    #lists for database information    
    tickers = []
    
    #opens file
    with open(filename,'r') as csvfile:
        securities = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        #populates the various data lists with proper entries
        for row in securities:
           tickers.append(row[0])
           
    #assign headers to headers list
    headers = [tickers[0]]    
    
    #remove headers from other lists
    tickers.remove(tickers[0])
    
    
    #remove quotation marks from strings
    for i in range(len(tickers)):
        tickers[i] = tickers[i].replace('"',"")
       
    
    return tickers   





def move_file(ticker,directory,download_dir):
    old_name = download_dir + '/' + ticker + '.csv'
    new_path = directory + '/' + ticker + '.csv'
    shutil.move(old_name,new_path)

def locate_click(driver,elem_path,Flag):
    """locates and clicks an element in the xml doc based on its xpath"""
    try:
        x = driver.find_element_by_xpath(elem_path)
        x.click()
    except WebDriverException:
        try:
            x = driver.find_element_by_xpath(elem_path)
            x.click()
        except WebDriverException:
            Flag = True
            return Flag
        
def stock_download_yahoo(ticker,directory,download_dir,Flag,frequency='"1d"',
                         driverpath='E:/PythonProjects/Yahoo_DataBase/chromedriver.exe'):
    """downloads stock data csv file for the selected ticker"""
    driver = webdriver.Chrome(driverpath)
    url = 'https://finance.yahoo.com/quote/' + ticker + '/history?p=' + ticker
    driver.get(url)
    
    #Xpath of each element that requires an interaction to get the correct
    #downloaded file
    date_button_path = '//div[@class="Pos(r) D(ib) Va(m) Mstart(8px)"]'
    max_button_path = '//button[@data-value="MAX"]' 
    done_button_path = '//button[@class=" Bgc($linkColor) Bdrs(3px) Px(20px) Miw(100px) Whs(nw) Fz(s) Fw(500) C(white) Bgc($linkActiveColor):h Bd(0) D(ib) Cur(p) Td(n)  Py(9px) Miw(80px)! Fl(start)"]'
    frequency_button_path = '//span[@data-test="historicalFrequency-selected"]'
    #for time period, 1mo = month , 1d = day, 1wk = week
    frequency_menu_path = '//div[@data-value=' + frequency + ']'
    apply_button_path = '//button[@class=" Bgc($linkColor) Bdrs(3px) Px(20px) Miw(100px) Whs(nw) Fz(s) Fw(500) C(white) Bgc($linkActiveColor):h Bd(0) D(ib) Cur(p) Td(n)  Py(9px) Fl(end)"]'
    download_button_path = '//a[@download="' + ticker + '.csv"]'
    
    #locates and clicks each required element to facilitate a correct download
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,200)")
    locate_click(driver,date_button_path,Flag)
    locate_click(driver,max_button_path,Flag)
    driver.execute_script("window.scrollTo(200,300)")
    locate_click(driver,done_button_path,Flag)
    locate_click(driver,frequency_button_path,Flag)
    locate_click(driver,frequency_menu_path,Flag)
    locate_click(driver,apply_button_path,Flag)
    
    #waits twenty seconds before downloading file; allows web app to update
    #data
    time.sleep(5)
    #locates and downloads spreadsheet
    locate_click(driver,download_button_path,Flag)
    time.sleep(2)
    
    move_file(ticker, directory, download_dir)
    #closes the browser
    time.sleep(5)
    driver.quit()
    return Flag

