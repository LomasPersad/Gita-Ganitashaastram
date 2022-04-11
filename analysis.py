# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud,STOPWORDS
import re
import json
import collections
from indic_transliteration import sanscript
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

#to do make large data into datafram

#------Extract sections from large datafile

def get_data(nam):
    f = open(nam)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()
    return data

def get_verses():
    # Opening JSON file
    f = open('LP_dataset_english.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()

    # Iterating through the chapters
    # list
    # for i in data['chapters']:
    #     print(data['chapters'][i]['name'])
    V=['a']*640
    indx=0
    # Iterating through the verses
    for i in data['chapters']:
        for v in data['verses'][i]:
            # print(data['verses'][str(i)][str(v)]['text'].replace('।।\* ।।',' '))
            print('chapter{} and verse{}'.format(i,v))
            tmp=data['verses'][str(i)][str(v)]['text'].replace('|',' ') #remove symbol
            tmp = tmp.replace('।', ' ')#remove symbol
            tmp = re.sub(r'\d+', '', tmp) #remove number
            V[indx]=tmp
            indx+=1

    # print(indx)
    data_file = open("LP_verses.json", "w", encoding="utf-8")
    json.dump(V, data_file, ensure_ascii=False)



#-----------------------main code
#--------redo getverse
# get_verses()

#---------------------ANALYSE Sanskrit
# Opening JSON file
# f = open('LP_verses.json')
# Verses = json.load(f)
# f.close()
data=get_data('LP_dataset_english.json') # all data
Verses=get_data('LP_verses.json')
df_verses = pd.DataFrame(Verses)
df_verses.rename(columns ={0:'hindi'}, inplace = True)

#------plot chapter-verse#
plt_vers=[0]*18
n=0
for i in data['chapters']:
    num=data['chapters'][str(i)]['verses_count']
    print('Chapter {} has {} verses'.format(i, num))
    plt_vers[n]=num
    n+=1

# Setting the dimensions of the figure
plt.figure(figsize=(15,5), frameon=False)
plt.tick_params(labelsize=11, length=6, width=2)
# Passing the data to plot
# sns.countplot(plt_vers)
sns.barplot(x='chapter_number', y='verses_count', data=data['chapters'])
plt.xlabel("Number of verses", fontsize=18)
plt.ylabel("Counts (Chapter(s))", fontsize=18)
# Displaying the plot
plt.show()


#get common words df_verses.head()
df_verses = df_verses.apply(lambda row: row['hindi'].strip().split(), axis=1)
data = []
for row in df_verses:
    temp = []
    for words in row:
        if len(words)>2:
            temp.append(words)
    data.append(temp)
data_flat = [item for sublist in data for item in sublist]

# Getting to know the most prominent 10 words used across the documen
# as per my knowledge of this holy document it makes sense to see these results because of the words used such as भारत, अर्जुन, कर्म, ज्ञानं.
top_10 = [i[0] for i in sorted(dict(collections.Counter(data_flat)).items(), key=lambda k: k[1], reverse=True)[:10]]
print(top_10)


#plot world cloud- generate for all, then each chapter
wordfreq = collections.Counter(data_flat)
text = data_flat
fig = plt.figure(figsize=(20,10), facecolor='k')
wordcloud = WordCloud(width=1300, height=600,max_words=2000,font_path='/home/ubuntu/Downloads/lohit_devanagari/Lohit-Devanagari.ttf').generate(str(wordfreq))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
plt.show()