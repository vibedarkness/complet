import random
import factory

from factory.faker import faker

from .models import Produit

FAKE= faker.Faker()

class ProduitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Produit


    nom=factory.Faker("sentence",nb_words=12)
    libelle=factory.Faker("catch_phrase")
    # quantite=factory.LazyAttribute(random.randrange(0,100))
