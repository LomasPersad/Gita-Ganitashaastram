# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
#from wordcloud import WordCloud,STOPWORDS
#import os
import json
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

# https://www.kaggle.com/datasets/schcsaba/bhagavadgita
# https://www.kaggle.com/code/yadavrohit/bhagavad-gita-analysis/notebook
# https://en.wikipedia.org/wiki/Sanskrit_nominals#Pronouns_and_determiners


# Opening JSON file
f = open('LP_dataset_english.json')

# returns JSON object as
# a dictionary
data = json.load(f)
# Closing file
f.close()

# Iterating through the json
# list
for i in data['chapters']:
    print(data['chapters'][i]['name'])



# Any results you write to the current directory are saved as output.