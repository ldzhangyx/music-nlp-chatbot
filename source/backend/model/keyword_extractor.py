from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import nltk
import pickle

id2label = {
    "0": "ADJ",
    "1": "ADP",
    "2": "ADV",
    "3": "AUX",
    "4": "CCONJ",
    "5": "DET",
    "6": "INTJ",
    "7": "NOUN",
    "8": "NUM",
    "9": "PART",
    "10": "PRON",
    "11": "PROPN",
    "12": "PUNCT",
    "13": "SCONJ",
    "14": "SYM",
    "15": "VERB",
    "16": "X"
},

with open('tags.pkl','rb') as f:
    genre_list = pickle.load(f)[:100]

keyword_blacklist = ['keyword', 'keywords','genre','genres', 'style']


# for lyrics
def keyword_extractor_lyrics(input_sentence):
    words = nltk.word_tokenize(input_sentence)
    genres = list()
    for word in words:
        if word in genre_list:
            genres.append(word)
    if len(genres) > 0:
        genres_text = ','.join(genres)
    else:
        genres_text = ""

    keywords = keyword_extractor(input_sentence, pos_list=['7'])
    keywords = list(filter(lambda x: x not in keyword_blacklist, keywords))
    if len(keywords) > 0:
        keywords_text = ','.join(keywords)
    else:
        keywords_text = ""

    return genres_text, keywords_text

# for music
def keyword_extractor(input_sentence, pos_list = ['0', '1', '2']):
    input_words = ['<SOS>'] + nltk.word_tokenize(input_sentence) + ['<EOS>']
    tokenizer = AutoTokenizer.from_pretrained("vblagoje/bert-english-uncased-finetuned-pos")
    model = AutoModelForTokenClassification.from_pretrained("vblagoje/bert-english-uncased-finetuned-pos")

    inputs = tokenizer(input_sentence)
    output = model(torch.tensor(inputs['input_ids']).unsqueeze(0))

    output_label = torch.argmax(output.logits.data.squeeze(0), dim=1)

    # what we need are ADJ and ADV
    keywords = list()
    for i, label in enumerate(output_label.tolist()):
        if str(label) in pos_list:
            keywords.append(input_words[i])

    return keywords