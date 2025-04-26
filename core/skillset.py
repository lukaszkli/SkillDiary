import LLM.gemini as gemini
from LLM.gemini import GeminiModel

from pydantic import BaseModel
import json

import database as db


from core.types import Skill, SkillCategory, SkillSet


async def get_skillset(user: db.User, summary: bool = False) -> SkillSet:
    """
    Function to get the skillset of a user.
    """

    experiences = await db.UserExperience.filter(user=user).select_related("skill", "skill__category").all()


    # Reformatting the data to match the SkillSet schema
    category_dict = {}

    for experience in experiences:
        skill: db.Skill = experience.skill
        category: db.SkillCategory = skill.category

        if category.name not in category_dict:
            category_dict[category.name] = SkillCategory(
                category_name=category.name,
                category_description=category.description,
                skills=[]
            )

        skill_data = Skill(
            skill_name=skill.name,
            skill_description=skill.description,
            points=experience.points
        )
        category_dict[category.name].skills.append(skill_data)

    # Summing up the points for each category
    for category in category_dict.values():
        category.sum_points = sum(skill.points for skill in category.skills)

    category_list = sorted(category_dict.values(), key=lambda x: x.sum_points, reverse=True)

    skillset = SkillSet(
        summary=None,
        skill_categories=category_list
    )

    if not summary:
        return skillset
    else:
        # Sending the skillset to Gemini for summary
        system_prompt = None
        with open("core/prompts/skillset_summary.txt", "r") as file:
            system_prompt = file.read()
        user_prompt = str(skillset.model_dump_json())

        response = gemini.get_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=GeminiModel.GEMINI_2_0_FLASH
        )

        skillset.summary = response
        return skillset