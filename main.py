import requests
import json

from rich.table import Table
from rich.console import Console

# https://restcountries.com/


class CountryNotFoundError(Exception):
    pass


class CountryData: # Penser évolutivité

    @staticmethod
    def get_data(term, search):
        if term == "country":
            response = requests.get(f"https://restcountries.com/v3.1/name/{search}?fullText=true")
        else:
            response = requests.get(f"https://restcountries.com/v3.1/capital/{search}")
        
        if response.status_code == 404:
            raise CountryNotFoundError(f"Pays ou capitale {search} introuvable")
        else:
            return response.json()
    
    @staticmethod
    def save_data(file_name, data):
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)
        


class CountryInterface:
    def __init__(self, country_data: CountryData):
        self.country_data = country_data
        self.data = list()
    
    @staticmethod
    def _ask_to_user():
        choices = ("1", "2")
        
        print("""
              Voulez-vous rechercher par nom de pays ou par capitale ?
              Choix 1. Pays
              Choix 2. Capitale
              """)
        
        choice = input("Votre choix : ")
        if choice not in choices:
            print("Mauvais choix")
            return
        return choice
    
    def get_data(self):
        choice = CountryInterface._ask_to_user()
        
        if choice == "1":
            country = input("Pays souhaités : ")
            data = self.country_data.get_data("country", country)
        else:
            capital = input("Capitales souhaitées : ")
            data = self.country_data.get_data("capital", capital)
            
        if data:
            self.data.append(data)
            return data
        else:
            return dict()
    
    def save_data(self, file_name, data):
        self.country_data.save_data(file_name, self.data)
        


class Country:
    def __init__(self, data):
        name, language, population, currency = Country._parse_data(data)
        self.name = name
        self.language = language
        self._population = population
        self.currency = currency
    
    def _parse_data(data):
        name = data[0]["name"]["common"]
        language = next(iter(data[0]["languages"].values()))
        population = data[0]["population"]
        currency = next(iter(data[0]["currencies"]))
        return name, language, population, currency
    
    def display_data(self):
        table = Table(title=f"Données de {self.name}")
        
        table.add_column("Titre", style="blue")
        table.add_column("Valeur", style="green")
        
        table.add_row("Langue", self.language)
        table.add_row("Population", str(self._population))
        table.add_row("Monnaie", self.currency)
        
        console = Console()
        console.print(table)
    
    @property
    def population(self):
        return self._population
    
    @population.setter
    def population(self, value):
        if value < 0:
            raise ValueError("Population ne peut pas être négative !")
        self._population = value


interface = CountryInterface(CountryData())
data = interface.get_data()
interface.save_data("file.json", data)

f = Country(data)

f.display_data()
f.population = 1
f.display_data()

