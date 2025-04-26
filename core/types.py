
from pydantic import BaseModel


class Skill(BaseModel):
    skill_name: str
    skill_description: str | None
    points: int

class SkillCategory(BaseModel):
    category_name: str
    category_description: str | None
    skills: list[Skill]
    sum_points: int | None = None



class SkillSet(BaseModel):
    summary: str | None
    skill_categories: list[SkillCategory]