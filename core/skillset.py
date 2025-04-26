import LLM.gemini as gemini
from LLM.gemini import GeminiModel

from pydantic import BaseModel
import json

import database as db


class SkillSet(BaseModel):
    summary: str


async def generate_skillset_summary(user: db.User) -> str:

    skills = await db.UserExperience.filter(user=user).values_list("skill").