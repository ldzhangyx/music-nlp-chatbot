from functools import reduce
import torch
import transformers
from transformers import DistilBertTokenizer, DistilBertModel
import pprint


def calculate_BERT_representation(input_text):
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertModel.from_pretrained("distilbert-base-uncased")
    input_ids = torch.tensor(tokenizer.encode(input_text)).unsqueeze(0)
    outputs = model(input_ids)
    last_hidden_states = outputs[0]

    mean_representation = torch.mean(last_hidden_states.squeeze(0)[1:-1], dim=0)

    return mean_representation

intention_list = [
        'generate melody',
        'write lyrics',
        'revise melody',
        'revise lyrics',
        'others'
    ]

def intention_analysis_bag_of_words(input_text):
    '''
    使用词袋的方式判断意图。
    分别计算输入的词袋和意图词向量的相似度，取最大项输出。
    可以选择fasttext还是glove。默认选择fasttext。
    '''

    minimum_similarity = 0.02



    intention_list_vector = torch.stack([
        calculate_BERT_representation(intention)
        for intention in intention_list[:-1]
    ])

    message_vector = calculate_BERT_representation(input_text)

    similarity = [float(torch.cosine_similarity(message_vector.T, intention_vector, dim = 0))
    for intention_vector in intention_list_vector]

    max_index = similarity.index(max(similarity))

    s = {intention_list[i]: similarity[i] for i in range(len(similarity))}
    pprint.pprint(s)

    # 设置最小阈值
    if similarity[max_index] > minimum_similarity:
        return intention_list[max_index]
    return intention_list[-1]
    
intention_analysis_bag_of_words('generate melody')

# vectors = GloVe('6B', dim=50)


def state_transfer(intention, keywords, current_state):
    if len(keywords) == 0:
        for i in range(len(intention_list)):
            if intention_list[i] == intention:
                current_state = i + 1
    return current_state
