# Concepts illustrés dans ce projet

## 🔒 Encapsulation

L'encapsulation consiste à **cacher les détails d'implémentation** et **contrôler l'accès aux données** en utilisant des méthodes publiques qui s'appuient sur des méthodes/attributs privés.

### Exemples dans le code

#### Méthodes publiques utilisant des méthodes privées

```python
# Dans CountryInterface
def get_data(self):  # Méthode PUBLIQUE
    choice = CountryInterface._ask_to_user()  # Utilise méthode PRIVÉE
    # ...

# Dans Country  
def __init__(self, data):  # Méthode PUBLIQUE
    name, language, population, currency = Country._parse_data(data)  # Utilise méthode PRIVÉE
```

**Avantage** : L'utilisateur appelle une méthode simple sans connaître les détails internes.

#### Attributs privés avec contrôle d'accès

```python
class Country:
    def __init__(self, data):
        # ...
        self._population = population  # Attribut PRIVÉ
    
    @property
    def population(self):  # Interface PUBLIQUE
        return self._population
    
    @population.setter
    def population(self, value):  # Contrôle d'accès
        if value < 0:
            raise ValueError("Population ne peut pas être négative !")
        self._population = value
```

**Principe clé** : Créer une **façade simple** (méthodes publiques) qui cache la **complexité** (méthodes/attributs privés).

## 💉 Injection de dépendance

L'injection de dépendance consiste à **passer les objets dont on a besoin** plutôt que de les créer à l'intérieur de la classe.

### Exemple dans le code

```python
class CountryInterface:
    def __init__(self, country_data: CountryData):  # INJECTION
        self.country_data = country_data

# Usage
interface = CountryInterface(CountryData())  # Dépendance injectée
```

### Avantages
- **Flexibilité** : on peut injecter différentes implémentations
- **Testabilité** : on peut injecter des mocks pour les tests
- **Faible couplage** : les classes sont moins dépendantes entre elles

## 🔗 Agrégation

L'agrégation représente une relation **"has-a"** où un objet contient une référence vers un autre objet, mais les deux peuvent exister indépendamment.

### Exemple dans le code

```python
class CountryInterface:
    def __init__(self, country_data: CountryData):
        self.country_data = country_data  # AGRÉGATION
```

`CountryInterface` **"a un"** `CountryData`, mais ils peuvent exister séparément.

## 🏗️ Séparation des responsabilités

Chaque classe a une responsabilité claire :

- **`CountryData`** : Récupérer et sauvegarder les données depuis l'API
- **`CountryInterface`** : Gérer l'interface utilisateur et l'interaction
- **`Country`** : Représenter un pays avec ses attributs et méthodes

Cette séparation rend le code plus **maintenable**, **testable** et **évolutif**.

## 🎯 Conventions Python

- **`_methode_privee()`** : Méthode "privée" (convention, pas forcé par le langage)
- **`_attribut_prive`** : Attribut "privé" (convention)
- **`@property`** : Getter élégant
- **`@attribut.setter`** : Setter avec validation