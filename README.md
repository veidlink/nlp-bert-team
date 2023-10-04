# nlp_bert_team

## Natural Language Processing

### Project

Elbrus Bootcamp | Phase-2 | Team Project

## 🦸‍♂️ Team
1. [Anton Yablokov](https://github.com/AntNikYab)
2. [Vika Ivanova](https://github.com/Vikaska031)
3. [Salman Chakaev](https://github.com/veidlink)

## 🎯 Task    
Development of a multipage application using streamlit [(Streamlit service deployed on HuggingFace Spaces)](https://huggingface.co/spaces/AntNikYab/NaturalLanguageProcessing):

- Page 1 • Review Classification for Polyclinics

        User-entered review classification model
        Outputs prediction results by three models:
        1) Classic ML algorithm (Logistic Regression) trained on BagOfWords representation
        2) LSTM model
        3) BERT-based
        Alongside the prediction, the time it was obtained is displayed
        The page features a comparative table based on the f1-macro metric for all constructed classifiers

- Page 2 • Text Generation with GPT Model

        Generative model 
        Users can adjust the length of the generated sequence
        The number of generations, temperature, top-k/p, maximum length, and the number of generated sequences can be controlled

- Page 3 • Evaluation of User Message Toxicity. The model is also available as a [Telegram bot](https://t.me/ToxicElbBot))

        Accepts user messages and assesses their toxicity
        Implemented using rubert-tiny-toxicity
