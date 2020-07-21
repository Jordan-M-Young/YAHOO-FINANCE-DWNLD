# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 18:36:15 2019

@author: Jordan
"""

import stock_download_yahoo as sdy


"""example of how the stock_download_yahoo functions can be combined to produce
a working database download manager for Y@h00 stock database"""



#directory where you want your files to go to
directory = 'C:/Users/jmyou/Desktop/Yahoo_DB_2020_Weekly'

#where your files are normally downloaded to
download_dir = 'C:/Users/jmyou/Downloads'

#Where your 'bad ticker file' should go
bad_ticker_file = 'E:/PythonProjects/Yahoo_DataBase/Yahoo_Bad_Tickers_Weekly.csv'

#directory of your driver
driverpath = 'E:/PythonProjects/Yahoo_DataBase/chromedriver.exe'

#frequency of the data you want to download '"1d"' '"1wk"' or '"1mo"'
frequency = '"1wk"'

#gets list of tickers from the companylist.csv file
#any list of tickers can be used though
tickers = sdy.open_list('companylist')



count = 0
downloads = []
failed_downloads = []
Flag = False
previous_downloads = sdy.Check_Downloads_Yahoo(tickers,directory)
bad_tickers = sdy.get_bad_tickers(bad_ticker_file)

for i in range(len(tickers)):
    if tickers[i] in previous_downloads:
        count += 1
    elif tickers[i] in bad_tickers:
        count += 1
    else:
        try:
            #change frequency to 1mo for monthly data and 1wk for weekly data
            sdy.Stock_Download_Yahoo(tickers[i],directory,download_dir,frequency,
                                     bad_ticker_file,driverpath,Flag)
            if Flag == False:
                count += 1
                downloads.append(tickers[i])
                Flag = False
            else:
                Flag = False
                failed_downloads.append(tickers[i])
        except FileNotFoundError:
            Flag = False
            failed_downloads.append(tickers[i])
            

print(downloads)
print(failed_downloads)    
