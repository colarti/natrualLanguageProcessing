import os, glob, zipfile
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import plotly.express as px
from datetime import datetime

def check_for_nltk():
    nltk.download('vader_lexicon')
    

def check_for_zip():
    print(os.getcwd())
    # os.chdir('.\\App8-NaturalLanguageProcessingBook\\natrualLanguageProcessing\\')

    dirlist = os.listdir()
    zip = glob.glob('*zip')
    print(f'zip: {zip}')

    for file in zip:
        if file.split('.zip') in dirlist:
            continue
        else:
            with zipfile.ZipFile(file, 'r') as f:
                f.extractall(f'.\\{file.strip(".zip")}\\')

    return zip

if __name__ == '__main__':
    try:
        analyzer = SentimentIntensityAnalyzer()
    except:
        check_for_nltk()
        analyzer = SentimentIntensityAnalyzer()
    
    dirlist = check_for_zip()
    print(f'dirlist: {dirlist}')

    datelist = list()
    resultlist = list()
    for x in dirlist:
        print(f'x: {x}')
        folder = x.removesuffix('.zip')
        
        for y in os.listdir(folder):
            date = y.removesuffix('.txt')
            date = datetime.strptime(date, '%Y-%m-%d').date()
            datelist.append(date)
            with open(f'{folder}\\{y}', 'r') as f:
                data = f.read()
            result = analyzer.polarity_scores(data)
            resultlist.append(result)
    
    # for date, result in zip(datelist, resultlist):
    #     print(date, result['pos'])

    print(f'datelist: {datelist}')
    print(f'resultlist: {resultlist}')

    poslist = [item['pos'] for item in resultlist]
    neglist = [item['neg'] for item in resultlist]

    st.title('Diary Tone')

    st.header('Positivity')

    fig = px.line(x=datelist, y=poslist, labels={'x':'Dates', 'y':'Confidence'})
    st.plotly_chart(fig)

    st.header('Negativity')

    negfig = px.line(x=datelist, y=neglist, labels={'x':'Dates', 'y':'Confidence'})
    st.plotly_chart(negfig)