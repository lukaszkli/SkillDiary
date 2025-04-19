from tortoise import fields, Tortoise
from tortoise.models import Model

import os


async def init_db():
    login = os.getenv("db_login")
    password = os.getenv("db_password")
    host = os.getenv("db_host")
    db_name = os.getenv("db_name")
    port = os.getenv("db_port")

    db_url = f"postgres://{login}:{password}@{host}:{port}/{db_name}"
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["database"]}
    )

    # await drop()  # Drop existing tables if any
    await Tortoise.generate_schemas()

async def drop():
    """ Function to drop the database tables """

    # Pobranie wszystkich tabel z PostgreSQL
    query = """
    SELECT tablename FROM pg_tables WHERE schemaname = 'public';
    """
    tables = await Tortoise.get_connection("default").execute_query_dict(query)

    # Iteracja po tabelach i usuwanie każdej z nich
    for table in tables:
        table_name = table['tablename']
        drop_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        await Tortoise.get_connection("default").execute_query(drop_query)


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    first_name = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"


class SkillCategory(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)

    class Meta:
        table = "skill_categories"


class Skill(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)

    categories: fields.ManyToManyRelation[SkillCategory] = fields.ManyToManyField(
        "models.SkillCategory", related_name="skills", through="skill_category_skills"
    )

    class Meta:
        table = "skills"


class UserExperience(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="experiences", on_delete=fields.CASCADE)
    skill = fields.ForeignKeyField("models.Skill", related_name="user_experiences", on_delete=fields.CASCADE)
    points = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    