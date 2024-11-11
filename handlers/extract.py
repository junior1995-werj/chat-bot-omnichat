import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer

from .questions import Movie

lemmatizer = WordNetLemmatizer()

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))        

def clear_writing(writing):
    
    sentence_words = nltk.word_tokenize(writing)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    

def bag_of_words(writing, words):
    """
        Pega as sentenças que são limpas e cria um pacote de palavras que são usadas 
        para classes de previsão que são baseadas nos resultados que obtivemos treinando o modelo.
    """
    sentence_words = clear_writing(writing)

    bag = [0]*len(words)
    for setence in sentence_words:
        for i, word in enumerate(words):
            if word == setence:
                bag[i] = 1
                
    return(np.array(bag))


def class_prediction(writing, model):

    prevision = bag_of_words(writing, words)
    response_prediction = model.predict(np.array([prevision]))[0]
    results = [[index, response] for index, response in enumerate(response_prediction) if response > 0.25]    
    
    if "1" not in str(prevision) or len(results) == 0 :
        results = [[0, response_prediction[0]]]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]


def get_response(intents, intents_json, writing):
    tag = intents[0]['intent']
    list_of_intents = intents_json['intents']
    try:
        for idx in list_of_intents:

            if idx['tag'] == tag:
                if tag == "bem_vindo": 
                    result = idx['responses']
                    break
                else:
                    movie = Movie()
                    result = movie.processar_tag(tag, writing)
                    break
    except:
        return "Desculpe não consegui encontrar nada relacionado ao assunto!"
    
    return result
