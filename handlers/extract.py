import numpy as np
import pickle
import nltk
from config import user_history
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
    # tokenize the pattern
    sentence_words = clear_writing(writing)
    
    # cria uma matriz de N palavras
    bag = [0]*len(words)
    for setence in sentence_words:
        for i, word in enumerate(words):
            if word == setence:
                bag[i] = 1
                
    return(np.array(bag))


def registrar_interacao(name_movie, movie_obj):
    # Armazena a pergunta e resposta em uma lista associada ao usuário
    user_history[name_movie].append(movie_obj)

def class_prediction(writing, model):

    # filtra as previsões abaixo de um limite 0.25
    prevision = bag_of_words(writing, words)
    response_prediction = model.predict(np.array([prevision]))[0]
    results = [[index, response] for index, response in enumerate(response_prediction) if response > 0.25]    
    
    # verifica nas previsões se não há 1 na lista, se não há envia a resposta padrão (anything_else) 
    # ou se não corresponde a margem de erro
    if "1" not in str(prevision) or len(results) == 0 :
        results = [[0, response_prediction[0]]]
    
    # classifica por força de probabilidade
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]


def get_response(intents, intents_json, writing):
    tag = intents[0]['intent']
    list_of_intents = intents_json['intents']
    for idx in list_of_intents:
        if idx['tag'] == tag:
            if tag == "bem_vindo": 
                result = idx['responses']
                break
            else:
                try:
                    movie_name = Movie()._find_name_movie(writing)
                    if user_history[movie_name]:
                        movie = user_history[movie_name]
                        result = movie[0].processar_tag(tag, movie_name)
                        break
                    else:
                        movie = Movie()
                        result = movie.processar_tag(tag, movie_name)
                        registrar_interacao(movie.name, movie)
                        break
                except: 
                    return "Desculpe não consegui encontrar o Filme."
          
    return result
