import pickle
"""
# open a file, where you stored the pickled data
file = open('meanings.pkl', 'rb')

# dump information to that file
data = pickle.load(file)


# close the file
file.close()

print('Showing the pickled data:')
cnt = 0
for item in data:
    print('The word', cnt, ' means: ', item)
    cnt += 1
"""
import pandas as pd

#object = pd.read_pickle('Sans.pkl')


with open('Sans.pkl', 'rb') as f:
    loaded_dict= pickle.load(f)
    Sans=loaded_dict.decode("utf-8", "ignore")
    print(Sans)