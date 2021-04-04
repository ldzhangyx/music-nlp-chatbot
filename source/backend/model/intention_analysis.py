from functools import reduce
import torch
import transformers
from transformers import AutoTokenizer, BertModel
import pprint


def calculate_BERT_representation(input_text):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    input_ids = torch.tensor(tokenizer.encode(input_text)).unsqueeze(0)
    outputs = model(input_ids)
    last_hidden_states = outputs[0]

    mean_representation = torch.mean(last_hidden_states.squeeze(0)[1:-1], dim=0)

    return mean_representation



def intention_analysis_bag_of_words(input_text):
    '''
    使用词袋的方式判断意图。
    分别计算输入的词袋和意图词向量的相似度，取最大项输出。
    可以选择fasttext还是glove。默认选择fasttext。
    '''

    minimum_similarity = 0.02

    actions = [
        'generate',
        'add'
        'revise alter',
        'delete remove'
    ]

    items = [
        'lyrics'
        'melody',
    ]

    combine_list = [' '.join([i, j]) for i in actions for j in items]

    intention_list = combine_list + ['others']

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
    
# intention_analysis_bag_of_words('generate melody')

# vectors = GloVe('6B', dim=50)

def state_transfer(intention):
    possible_states = [False, True, True, True, True, False]
    keywords = intention.split()
    if keywords[0] == 'generate':
        possible_states[2] = possible_states[4] = False
    if keywords[0] != 'generate':
        possible_states[1] = possible_states[3] = False
    if keywords[1] == 'melody':
        possible_states[3] = possible_states[4] = False
    if keywords[1] == 'lyrics':
        possible_states[1] = possible_states[2] = False
    for i in range(len(possible_states)):
        if possible_states[i] is True:
            return i
    return -2