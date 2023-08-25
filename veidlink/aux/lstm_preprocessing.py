import re
import string
import numpy as np
import torch
import torch.nn as nn

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

class LSTMClassifier(nn.Module):
    def __init__(self, embedding_dim: int, hidden_size:int, embedding: torch.nn.modules.sparse.Embedding) -> None:
        super().__init__()

        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.embedding = embedding

        self.lstm = nn.LSTM(
            input_size=self.embedding_dim,
            hidden_size=self.hidden_size,
            batch_first=True
        )
        self.clf = nn.Linear(self.hidden_size, 1)

    def forward(self, x):
        embeddings = self.embedding(x)
        _, (h_n, _) = self.lstm(embeddings)
        out = self.clf(h_n.squeeze())
        return out


def data_preprocessing(text: str) -> str:
    """preprocessing string: lowercase, removing html-tags, punctuation, 
                            stopwords, digits

    Args:
        text (str): input string for preprocessing

    Returns:
        str: preprocessed string
    """    

    text = text.lower()
    text = re.sub('<.*?>', '', text) # html tags
    text = ''.join([c for c in text if c not in string.punctuation])# Remove punctuation
    text = ' '.join([word for word in text.split() if word not in stop_words])
    text = [word for word in text.split() if not word.isdigit()]
    text = ' '.join(text)
    return text

def get_words_by_freq(sorted_words: list, n: int = 10) -> list:
    return list(filter(lambda x: x[1] > n, sorted_words))

def padding(review_int: list, seq_len: int) -> np.array: # type: ignore
    """Make left-sided padding for input list of tokens

    Args:
        review_int (list): input list of tokens
        seq_len (int): max length of sequence, it len(review_int[i]) > seq_len it will be trimmed, else it will be padded by zeros

    Returns:
        np.array: padded sequences
    """    
    features = np.zeros((len(review_int), seq_len), dtype = int)
    for i, review in enumerate(review_int):
        if len(review) <= seq_len:
            zeros = list(np.zeros(seq_len - len(review)))
            new = zeros + review
        else:
            new = review[: seq_len]
        features[i, :] = np.array(new)
            
    return features

def preprocess_single_string(
    input_string: str, 
    seq_len: int, 
    vocab_to_int: dict,
    ) -> torch.tensor:
    """Function for all preprocessing steps on a single string

    Args:
        input_string (str): input single string for preprocessing
        seq_len (int): max length of sequence, it len(review_int[i]) > seq_len it will be trimmed, else it will be padded by zeros
        vocab_to_int (dict, optional): word corpus {'word' : int index}. Defaults to vocab_to_int.

    Returns:
        list: preprocessed string
    """    

    preprocessed_string = data_preprocessing(input_string)
    result_list = []
    for word in preprocessed_string.split():
        try: 
            result_list.append(vocab_to_int[word])
        except KeyError as e:
            print(f'{e}: not in dictionary!')
    result_padded = padding([result_list], seq_len)[0]

    return torch.tensor(result_padded)

def predict_sentence(text: str, model: nn.Module, seq_len: int, vocab_to_int: dict) -> str: 
    p_str = preprocess_single_string(text, seq_len, vocab_to_int).unsqueeze(0)
    model.eval() 
    output = model(p_str).sigmoid().round().item() 
    if output == 0: 
        result = 'negative' 
    else: 
        result = 'positive' 
    return result