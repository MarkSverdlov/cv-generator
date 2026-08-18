import os
import pathlib

import typer

from cv_gen import CV
from modify import modify
from role_fit import suggest_fit, suggest_modification


def detect_language(text: str) -> str:
    hebrew = sum("\u0590" <= c <= "\u05ff" for c in text)
    latin = sum(("a" <= c.lower() <= "z") for c in text)

    total = hebrew + latin

    if total == 0:
        return "en"  # fallback

    return "he" if hebrew / total > 0.3 else "en"


def main(cv_path: pathlib.Path, role_path: pathlib.Path, role_name: str) -> None:
    with open(cv_path) as file:
        cv_json = file.read()
    with open(role_path, encoding="utf-8") as file:
        role_ad = file.read()

    os.mkdir(role_name)

    role_fit = suggest_fit(cv_json, role_ad)
    modification = suggest_modification(cv_json, role_fit)
    cv = CV.model_validate_json(cv_json)
    new_cv = modify(cv, modification)

    with open(f"{role_name}/role-fit-summary.txt", "w") as file:
        file.write(role_fit)

    language = detect_language(role_ad)
    if language == "he":
        from cv_gen_he import generate_cv
    else:
        from cv_gen import generate_cv
    new_cv_txt = generate_cv(new_cv)
    with open(f"{role_name}/mark-sverdlov-cv.tex", "w") as file:
        file.write(new_cv_txt)


if __name__ == "__main__":
    typer.run(main)
