import csv
import pandas as pd
import pickle

if __name__ == "__main__":

    tags_csv_path = r'C:\Users\ldzha\OneDrive\AIM\Music4All\id_tags.csv'

    tags_table = pd.read_csv(tags_csv_path, sep='\t', index_col='id')

    genre_set = dict()

    for i in range(len(tags_table)):
        genres = tags_table.iloc[i]['tags'].split(',')
        for item in genres:
            if item in genre_set.keys():
                genre_set[item] += 1
            else:
                genre_set[item] = 0

        if i % 500 == 0:
            counter_k = sorted(genre_set.items(), key=lambda x: x[1], reverse=True)[:10]
            print(counter_k)

    counter_k = sorted(genre_set.items(), key=lambda x: x[1], reverse=True)
    counter_k_keys = [i[0] for i in counter_k]
    print(len(counter_k_keys))

    with open('tags.pkl', 'wb') as f:
        pickle.dump(counter_k_keys, f)
