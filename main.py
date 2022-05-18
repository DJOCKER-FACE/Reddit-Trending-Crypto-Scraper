import requests
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import time
now = datetime.now()
current_time  = date.today()
filter= 'all'
#ADD YOUR TOKENS HERE!
Telegram_Photo_Token= ""
Telegram_Message_Token=""
CHAT_ID=""

def sendpicture():
    # Send plot picture to telegram.
    #create a variable with the path to str(current_time) + '.png' in rb mode.
    file = open(str(current_time) + '.png', 'rb')
    time.sleep(40)
    url = Telegram_Photo_Token
    files = {'photo': file}
    payload = {'chat_id': CHAT_ID}
    response = requests.post(url, data=payload, files=files)
    print(response)
    #close str(current_time) + '.png'.
    file.close()
    os.remove(str(current_time) + '.png')

def main():
    pageNbr=1
    while pageNbr < 2:   
        url = f'https://apewisdom.io/api/v1.0/filter/{filter}/page/{pageNbr}'
        response = requests.get(url)           
        pageNbr+=1
        #Extract results list from response.
        results = response.json()['results']
        #For result in results: put into a dataframe
        df = pd.DataFrame(results)
        #convert all numbers to floats
        df['mentions'] = df['mentions'].astype(float)
        #Plot 20 first mentions and tickers.
        df.sort_values(by='mentions', ascending=False).head(25).plot(kind='bar', x='ticker', y='mentions')
        plt.title('Top 25 tickers in reddit by mentions ' + str(current_time))
        # plt.show()
        #labe the x axis with tickers, and y axis with mentions.
        plt.xlabel('Ticker')
        plt.ylabel('Mentions')
        #Save plot to file with current time.
        plt.savefig(str(current_time) + '.png')
        #append 20 first tickers to tickers list.
        tickers = df.sort_values(by='mentions', ascending=False).head(25)['ticker'].tolist()
        print(tickers)
        #if new element in tickers list, send request post to telegram.
        for ticker in tickers:
            if ticker not in tickers_list:
                print(ticker)
                url = Telegram_Message_Token
                payload = {'chat_id': CHAT_ID, 'text': ticker+' is trending in reddit'}
                response = requests.post(url, data=payload)
                tickers_list.append(ticker)
        for ticker in tickers_list:
            if ticker not in tickers:
                print(ticker)
                url = Telegram_Message_Token
                payload = {'chat_id': CHAT_ID, 'text': ticker+ ' has been removed from the list'}
                response = requests.post(url, data=payload)
                tickers_list.remove(ticker)
                time.sleep(1)
        sendpicture()
       
tickers_list = []

while True:
    print("new load")
    main()
    time.sleep(3600)
        



