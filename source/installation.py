import sys
sys.path.insert(0, r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\music-nlp-chatbot")

from database import database_op
from torchnlp.word_to_vector import GloVe

if __name__ == '__main__':
    database_op.log_table_init('log.sqlite3')
    database_op.creation_table_init('log.sqlite3')

    vector = GloVe('6B',dim=50)