from torch.utils.data import Dataset
# from transformers import
import os
import pandas as pd
import csv
from rake_nltk import Rake
from langdetect import detect
#
# class Music4AllDataset(Dataset):
#     def __init__(self):
#         super().__init__()
#
#     def __len__(self):
#
#
#     def __getitem__(self, index):
#
#




def lyrics_preprocessing(folder_path, tags_csv_path, output_csv_path):
    collection = list()

    # genre
    tags_table = pd.read_csv(tags_csv_path, sep='\t', index_col='id')

    # lyrics
    for i, file_name in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        file_id = file_name.split('.')[0]

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = [i.strip() for i in lines]
            lyrics = ';'.join(lines)

        # keywords
        r = Rake()
        r.extract_keywords_from_sentences(lines)
        keywords = r.get_ranked_phrases()
        keywords_str = ','.join(keywords[:3])
        tags = tags_table.loc[file_id, 'tags']

        # clean data
        if len(lyrics) < 50:
            continue
        if detect(lyrics[:100]) != 'en':
            continue

        # add line
        collection.append([tags, keywords_str, lyrics])

        if i % 100 == 0:
            print(i)

    with open(output_csv_path, 'w', encoding='utf-8',newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        # writer.writerow(['tags','keywords','lyrics'])
        writer.writerows(collection)


lyrics_path = r'C:\Users\ldzha\OneDrive\AIM\Music4All\lyrics\lyrics'
tags_path = r'C:\Users\ldzha\OneDrive\AIM\Music4All\id_tags.csv'
output_path = r'C:\Users\ldzha\OneDrive\AIM\Music4All\output_clean.csv'

lyrics_preprocessing(lyrics_path, tags_path, output_path)