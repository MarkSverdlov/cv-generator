from pydantic import BaseModel

from .cv_gen import CV, Skill


class Modification(BaseModel):
    new_summary: str
    new_skill_list: list[Skill]
    new_ds_job_description: list[str]
    new_bo_job_description: list[str]


def modify(cv: CV, modification: Modification) -> CV:
    new_cv = cv.model_copy(
        deep=True,
        update={
            "summary": modification.new_summary,
        },
    )
    new_cv.experience[0].description = modification.new_ds_job_description
    new_cv.experience[1].description = modification.new_bo_job_description
    return new_cv
