from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import nltk

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


def keyword_extractor(input_sentence):
    input_words = ['<SOS>'] + nltk.word_tokenize(input_sentence) + ['<EOS>']
    tokenizer = AutoTokenizer.from_pretrained("vblagoje/bert-english-uncased-finetuned-pos")
    model = AutoModelForTokenClassification.from_pretrained("vblagoje/bert-english-uncased-finetuned-pos")

    inputs = tokenizer(input_sentence)
    output = model(torch.tensor(inputs['input_ids']).unsqueeze(0))

    output_label = torch.argmax(output.logits.data.squeeze(0), dim=1)

    # what we need are ADJ and ADV
    keywords = list()
    for i, label in enumerate(output_label.tolist()):
        if str(label) in ['0','1','2']:
            keywords.append(input_words[i])

    return keywords