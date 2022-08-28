import pandas as pd
import json
import re

# with open(r'LP_dataset_english.json', encoding='utf-8') as f:
#      json_data = json.load(f)
#      f.close()

Gita_data = pd.read_json(r'LP_dataset_english.json')
translit_verses=[]
for i in range(1, 2):
    for v in Gita_data['verses'][i]:
        chpt_translit=Gita_data['verses'][i][v]['transliteration']
        # chpt_translit=chpt_translit.replace("?(\R)", '', case=False, regex=True)
        result = re.sub(r"uvācha\n", 'uvācha:', chpt_translit)
        translit_verses.append(result)

regular_list = '\n'.join(translit_verses)
# all_verses=regular_list.strip()
individ_lines = re.split('\n', regular_list)
#group two lines together
grp_verses=[]
for i in range(0, len(individ_lines), 2):
    verse= individ_lines[i] + ',' + individ_lines[i+1]
    grp_verses.append(verse)
    # print(verse)

translit_df=pd.DataFrame(grp_verses)
# print(regular_list.strip())
