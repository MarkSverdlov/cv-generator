import pathlib

import typer
from pydantic import BaseModel, ValidationError

from premble_text_he import premble

# SUMMARY SECTION


def summary_section(summary: str) -> str:
    prefix = """
\\section{תקציר}
"""

    return prefix + summary


# EDUCATION SECTION
class EducationLine(BaseModel):
    start_year: str
    end_year: str
    description: str


def education_section(education: list[EducationLine]) -> str:
    education_prefix = """
\\section{השכלה}
\\begin{tabularx}{\\linewidth}{@{}l X@{}}
"""
    education_suffix = """
\\end{tabularx}
"""
    result = ""
    first = True
    for education_line in education:
        if not first:
            result += " \\\\\n"
        result += f"{education_line.start_year} - {education_line.end_year} & {education_line.description}"
        first = False
    return education_prefix + result + education_suffix


# EXPERIENCE SECTION


class Job(BaseModel):
    title: str
    timeframe: str
    description: list[str]


def experience_section(experience: list[Job]) -> str:
    result = ""
    prefix_experience = """
\\section{ניסיון}
"""
    for job in experience:
        result += "\\begin{joblong}{" + job.title + "}{" + job.timeframe + "}\n"
        for item in job.description:
            result += "    \\item " + item + "\n"
        result += "\\end{joblong}\n\n"
    return prefix_experience + result


# SKILL SECTION


class Skill(BaseModel):
    name: str
    description: str


def skill_section(skills: list[Skill]) -> str:
    result = ""
    prefix_skills = """
\\section{מיומנויות}
\\begin{tabularx}{\\linewidth}{@{}l X@{}}
"""
    for skill in skills:
        result += f"{skill.name} & {skill.description} \\\\\n"
    result += "\\end{tabularx}\n"
    return prefix_skills + result


suffix = """
\\vfill
\\center{\\footnotesize עודכן לאחרונה: \\today}

\\end{document}%Interests/ Keywords/ Summary"""


class CV(BaseModel):
    summary: str
    education: list[EducationLine]
    experience: list[Job]
    skills: list[Skill]


def generate_cv(cv: CV) -> str:
    text = (
        premble
        + summary_section(cv.summary)
        + education_section(cv.education)
        + experience_section(cv.experience)
        + skill_section(cv.skills)
        + suffix
    )
    return text


def main(cv_path: pathlib.Path, path: pathlib.Path) -> None:
    try:
        with open(cv_path, "r") as input_file:
            cv_json = input_file.read()
        cv = CV.model_validate_json(cv_json)
    except ValidationError as e:
        print(f"Validation failed with {e.error_count()} error(s):\n")
        for error in e.errors():
            location = " -> ".join(str(loc) for loc in error["loc"])
            print(f"Field: {location}")
            print(f"  Error: {error['msg']}")
            print(f"  Value: {error['input']}\n")
    else:
        text = generate_cv(cv)
        with open(path, "w") as output_file:
            output_file.write(text)


if __name__ == "__main__":
    typer.run(main)
