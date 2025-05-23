
from pydantic import BaseModel
import json

import LLM.gemini as gemini
from LLM.gemini import GeminiModel

import database as db


from core.types import Skill, SkillCategory


class SkillUpdate(BaseModel):
    updated_skills: list[SkillCategory] | None


class SkillCategoryDemand(BaseModel):
    """
    Class to represent the skill categories requested by the LLM to fetch the skills.
    """
    category_names: list[str]


async def _get_skill_categories_demand(message: str) -> SkillCategoryDemand:
    """
    LLM decides which skill categories are needed to update the skills based on the user message.
    The function will return the list of skill categories.
    """

    system_prompt = ""
    with open("./core/prompts/skill_update_category.txt", "r") as f:
        system_prompt = f.read()

    existing_categories = await db.SkillCategory.all().values_list("name", flat=True)

    user_prompt = f"Existing Categories:\n{str(existing_categories)}\n\nUser Message:\n{message}"

    response = gemini.get_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=GeminiModel.GEMINI_2_0_FLASH,
        output_schema=SkillCategoryDemand
    )

    skill_category_demand = SkillCategoryDemand.model_validate_json(response)
    return skill_category_demand
            

async def _save_skill_to_db(user_id: int, skill_update: SkillUpdate):
    """
    Function to save the skill update for a user.
    """

    for category in skill_update.updated_skills:
        category_name = category.category_name
        category_description = category.category_description

        # Check if the category already exists
        existing_category = await db.SkillCategory.get_or_none(name=category_name)
        if not existing_category:
            # Create a new category if it doesn't exist
            existing_category = await db.SkillCategory.create(name=category_name, description=category_description)

        # Save the skills in the category
        for skill in category.skills:
            skill_name = skill.skill_name
            skill_description = skill.skill_description
            points = skill.points

            existing_skill = await db.Skill.get_or_none(name=skill_name)
            if not existing_skill:
                # Create a new skill if it doesn't exist
                existing_skill = await db.Skill.create(name=skill_name, description=skill_description, category=existing_category)

            # Create user experience
            user = await db.User.get_or_none(id=user_id)
            if user:
                await db.UserExperience.create(user=user, skill=existing_skill, points=points)



async def skill_updater_message_handler(user_id: int, message: str) -> SkillUpdate:
    """
    Function to update the skills of a user.
    """
    

    skill_category_demand = await _get_skill_categories_demand(message)


    skills = {}
    for category in skill_category_demand.category_names:
        skills[category] = await db.Skill.filter(category__name=category).values_list("name", flat=True)
        skills[category] = list(skills[category])

    system_prompt = ""
    with open("./core/prompts/skill_update.txt", "r") as f:
        system_prompt = f.read()

    user_prompt = f"Skills:\n{str(skills)}\n\nUser Message:\n{message}"


    response = gemini.get_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=GeminiModel.GEMINI_2_0_FLASH,
        output_schema=SkillUpdate
    )
    print(response)
    skill_update = SkillUpdate.model_validate_json(response)
    await _save_skill_to_db(user_id, skill_update)
    return skill_update
            