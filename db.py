from peewee import *
from dateutil.parser import parse as dateparse

db = SqliteDatabase("/tmp/recept.db")


class BaseModel(Model):
    class Meta:
        database = db


class Recept(BaseModel):
    calories = FloatField(null=True)
    fat = FloatField(null=True)
    protein = FloatField(null=True)
    rating = FloatField(null=True)
    sodium = FloatField(null=True)
    desc = TextField(null=True)
    directions = TextField(null=True)
    ingredients = TextField(null=True)
    title = CharField(null=True)
    date = DateTimeField(null=True)

    def create(
        self=None,
        calories=None,
        fat=None,
        protein=None,
        rating=None,
        sodium=None,
        desc=None,
        directions=None,
        ingredients=None,
        title=None,
        date=None,
    ):
        self.calories = calories
        self.fat = fat
        self.protein = protein
        self.rating = rating
        self.sodium = sodium
        self.desc = desc
        if directions is not None:
            self.directions = "".join(map(lambda x: x+"\n", directions))
        if ingredients is not None:
            self.ingredients = "".join(map(lambda x: x+"\n", ingredients))
        self.title = title
        if date is not None:
            self.date = dateparse(date)


class Categorie(BaseModel):
    name = CharField(unique=True)


class CategorieRecept(BaseModel):
    categorie = ForeignKeyField(Categorie, backref="recepts")
    recept = ForeignKeyField(Recept, backref="categories")

    class Meta:
        primary_key = CompositeKey("categorie", "recept")


db.connect()
db.create_tables([Categorie, Recept, CategorieRecept])

if __name__ == "__main__":
    import json
    from sys import argv
    from tqdm import tqdm

    def init_categories(names):
        for name in names:
            entity, _ = Categorie.get_or_create(name=name.lower())
            yield entity

    with open(argv[1]) as json_file:
        js = json.load(json_file)

        for data in tqdm(js):
            categories = data.pop(
                "categories") if "categories" in data.keys() else None

            recept = Recept()
            recept.create(**data)
            recept.save()

            if categories is not None:
                entity_categories = init_categories(
                    categories
                )
                for categorie in entity_categories:
                    categorie_recept = CategorieRecept.create(
                        categorie=categorie,
                        recept=recept
                    )
