from peewee import *

db = SqliteDatabase("./recept.db")


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


class Categorie(BaseModel):
    name = CharField()


class CategorieRecept(BaseModel):
    categorie = ForeignKeyField(Categorie)
    recept = ForeignKeyField(Recept)

    class Meta:
        primary_key = CompositeKey('categorie', 'recept')


db.connect()
db.create_tables([Categorie, Recept, CategorieRecept])

if __name__ == "__main__":
    pass
