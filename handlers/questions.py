import random
import requests
import ast
from unidecode import unidecode
from config import settings
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class Movie: 

    def __init__(self):
        self.name = ""
        self.id = ""
        self.vote_average = ""
        self.type_of_movie = ""
        self.cast_movie = ""
        self.synopsis_movie = ""
        self.casts_movie = ""

    def _set_values(self):
        
        if not self.id:
            url = f"{settings.API_URL}search/movie?api_key={settings.API_KEY}&language=pt-BR&query={self.name}"
            response = self._get_api(url)

            if len(response['results']) == 0: 
                return 0
            
            self.id = response['results'][0]['id']
            
            self.vote_average = response['results'][0]['vote_average']
            self.synopsis_movie = response['results'][0]['overview']

            url = f"{settings.API_URL}movie/{self.id}/credits?api_key={settings.API_KEY}&language=pt-BR"
            response = self._get_api(url)

            self.casts_movie = response['cast'][:5]
            
            url = f"{settings.API_URL}movie/{self.id}?api_key={settings.API_KEY}&language=pt-BR"
            response = self._get_api(url)
        else: 
            pass


    def get_avaliation(self, *args): 
        self.name = args[0]
        self._set_values()
        text_return = f"Esta é a nota do filme '{self.name}': \n {str(self.vote_average)}"

        return text_return


    def get_synopsis(self, *args):
        self.name = args[0]
        self._set_values()
        text_return = f"Esta é a sinopse do filme '{self.name}': \n {self.synopsis_movie}"

        return text_return


    def get_cast(self, *args):
        self.name = args[0]
        self._set_values()
        text_return = f"Estes são os 5 principais atores do filme '{self.name}': \n"

        for cast in self.casts_movie: 
            text_return +=f"    - Ator: {cast['name']}, Personagem: {cast['character']}\n"

        return text_return


    def get_top_three_best(self, *args):
        url = f"{settings.API_URL}movie/top_rated?api_key={settings.API_KEY}&language=pt-BR&sort_by=vote_average.desc"
        response = self._get_api(url)

        response = response['results'][:3]
        text_return = "Os 3 filmes melhores avaliados no momento são: \n"
        for movie in response:
            text_return +=f"    - Filme: {movie['original_title']}, nota: {movie['vote_average']}\n"

        return text_return
    

    def get_type_of_movie(self, *args):
        url = f"{settings.API_URL}genre/movie/list?api_key={settings.API_KEY}&language=pt-BR"
        response = self._get_api(url)
        dict_genres = response['genres']

        for value in dict_genres:
            if unidecode(value['name'].lower()) in unidecode(args[1].lower()):
                url = f"{settings.API_URL}discover/movie?api_key={settings.API_KEY}&language=pt-BR&with_genres={value['id']}"
                response = self._get_api(url)

                response = random.sample(response['results'], 4)
                text_return = f"Você escolheu o genero {value['name']}, sugestoes que você pode gostar: \n"

                for movie in response:
                    text_return +=f"    - Filme: {movie['title']}, nota: {movie['vote_average']}\n"

                text_return + f"Espero que goste!"

        return text_return
    

    def get_similar(self, *args):
        self.name = args[0]
        self._set_values()

        url = f"{settings.API_URL}movie/{self.id}/similar?api_key={settings.API_KEY}&language=pt-BR"
        response = self._get_api(url)

        response = random.sample(response['results'], 4)

        text_return = f"Filmes semelhantes ao '{self.name}', sugestão: \n"

        for movie in response: 
            text_return +=f"    - Filme: {movie['title']}, nota: {movie['vote_average']}\n"
        return text_return


    def processar_tag(self, tag, writing):
        method_name = f"get_{tag}"
        metodo = getattr(self, method_name, None)

        movie_name = ""
        if tag in ['cast', "synopsis", "avaliation", "similar"]:
            movie_name = self._find_name_movie(writing)
        
        args=(movie_name,writing)

        if callable(metodo):
            return metodo(*args)
        else:
            return f"Sinto muito, ainda não estou preparado para esta ação!"
    
    @staticmethod
    def _get_api(url): 
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        return response
    

    @staticmethod
    def _find_name_movie(writing):
        
        template_mensagem = ChatPromptTemplate.from_messages([
            ("system", "Qual o nome do filme na fraze, no retorno quero apenas o nome do filme em formato de list python, onde o nome do filme esta sempre na primeira posicao"),
            ("user", "{texto}"),
        ])
        modelo = ChatOpenAI(model="gpt-3.5-turbo")
        parser = StrOutputParser()
        chain = template_mensagem | modelo | parser
        value_return = chain.invoke({"texto": writing})
        return ast.literal_eval(value_return)[0]
