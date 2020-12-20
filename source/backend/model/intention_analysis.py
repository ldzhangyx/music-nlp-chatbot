from torchnlp.word_to_vector import FastText

def intention_analysis_bag_of_words(input_text):
    '''
    使用词袋的方式判断意图。
    分别计算输入的词袋和意图词向量的相似度，取最大项输出。
    可以选择fasttext还是glove。默认选择fasttext。
    '''
    intention_list = [
        'generate melody',
        'add arrangement',
        'add drums',
        'generate lyrics',
        'chat' # 这个应该被归类到others
    ]
    vectors = FastText()
    intention_list_vector = [

    ]
    pass