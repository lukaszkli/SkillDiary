
from pydantic import BaseModel

import LLM.gemini as gemini
from LLM.gemini import GeminiModel

import database as db

class SkillPoint(BaseModel):
    skill_name: str
    skill_description: str | None
    points: int

class SkillCategory(BaseModel):
    category_name: str
    category_description: str | None
    skills: list[SkillPoint]

class SkillUpdate(BaseModel):
    updated_skills: list[SkillCategory] | None


class SkillCategoryDemand(BaseModel):
    category_names: list[str]


async def _get_skill_categories_demand(message: str) -> SkillCategoryDemand:
    """
    Function to get the skill categories demand for a user.
    """

    system_prompt = ""
    with open("./core/prompts/skill_update_category.txt", "r") as f:
        system_prompt = f.read()

    existing_categories = await db.SkillCategory.all().values_list("name", flat=True)

    user_prompt = f"Existing Categories:\n{str(existing_categories)}\n\nUser Message:\n{message}"


    max_retries = 3
    retry_count = 0
    while True:
        try:
            response = gemini.get_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=GeminiModel.GEMINI_2_0_FLASH,
                output_schema=SkillCategoryDemand
            )

            skill_category_demand = SkillCategoryDemand.model_validate_strings(response)
            return skill_category_demand
            
        except Exception as e:
            # TODO: Handle specific exceptions
            # TODO: Add logging
            print(f"Error: {e}, Retrying...")
            retry_count += 1
            if retry_count >= max_retries:
                raise e
            continue


async def skill_updater_message_handler(user_id: int, message: str):
    """
    Function to update the skills of a user.
    """
    

    skill_category_demand = await _get_skill_categories_demand(user_id)