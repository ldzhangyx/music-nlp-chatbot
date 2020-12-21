from functools import reduce
import torch
from torchnlp.word_to_vector import GloVe

def intention_analysis_bag_of_words(input_text):
    '''
    使用词袋的方式判断意图。
    分别计算输入的词袋和意图词向量的相似度，取最大项输出。
    可以选择fasttext还是glove。默认选择fasttext。
    '''

    minimum_similarity = 0.02

    actions = [
        'create add generate',
        'revise',
    ]

    items = [
        'melody',
        'arrangement',
        'chords',
        'drums beats',
        'lyrics text'
    ]

    combine_list = [' '.join([i, j]) for i in actions for j in items]

    intention_list = combine_list + ['others']


    vectors = GloVe('6B', dim=50)

    intention_list_vector = torch.stack([
        torch.mean(torch.stack([
            vectors[word] for word in intention.split()
        ]), dim = 0)
        for intention in intention_list[:-1]
    ])

    message_vector = torch.mean(torch.stack([
            vectors[word] for word in input_text.split()
        ]), dim = 0)

    similarity = [float(torch.cosine_similarity(message_vector.T, intention_vector, dim = 0))
    for intention_vector in intention_list_vector]

    max_index = similarity.index(max(similarity))

    # 设置最小阈值
    if similarity[max_index] > minimum_similarity:
        return intention_list[max_index]
    return intention_list[-1]
    
# intention_analysis_bag_of_words('generate melody')

# vectors = GloVe('6B', dim=50)