import os
import pathlib
import sys

import typer

from .cv_gen import CV
from .modify import modify
from .role_fit import suggest_fit, suggest_modification


def detect_language(text: str) -> str:
    hebrew = sum("\u0590" <= c <= "\u05ff" for c in text)
    latin = sum(("a" <= c.lower() <= "z") for c in text)

    total = hebrew + latin

    if total == 0:
        return "en"  # fallback

    return "he" if hebrew / total > 0.3 else "en"


def main(role_path: pathlib.Path, role_name: str | None = None) -> None:
    if role_name is None:
        role_name = role_path.stem
    role_cv_path = pathlib.Path(f"~/curriculum-vitae/{role_name}").expanduser()
    try:
        os.mkdir(role_cv_path)
    except FileExistsError:
        print(f"{role_name} already exists. Please choose another name")
        sys.exit(0)
    with open(role_path, encoding="utf-8") as file:
        role_ad = file.read()
    language = detect_language(role_ad)
    if language == "he":
        from cv_gen_he import generate_cv

        cv_path = pathlib.Path("~/curriculum-vitae/cv-he.json").expanduser()
    else:
        from cv_gen import generate_cv

        cv_path = pathlib.Path("~/curriculum-vitae/cv.json").expanduser()
    with open(cv_path) as file:
        cv_json = file.read()

    role_fit = suggest_fit(cv_json, role_ad)
    modification = suggest_modification(cv_json, role_fit)
    cv = CV.model_validate_json(cv_json)
    new_cv = modify(cv, modification)

    with open(role_cv_path / "role-fit-summary.txt", "w") as file:
        file.write(role_fit)

    new_cv_txt = generate_cv(new_cv)
    with open(role_cv_path / "mark-sverdlov-cv.tex", "w") as file:
        file.write(new_cv_txt)


if __name__ == "__main__":
    typer.run(main)
