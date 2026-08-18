import structlog
from langchain_core.prompts import ChatPromptTemplate

from llm import llm
from modify import Modification

logger = structlog.get_logger()


def suggest_fit(cv: str, role: str) -> str:
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are an assistant that helps to apply to jobs. Consider the following CV:\n\n{cv}\n\nAnd consider the following role:\n\n{role}",
            ),
            (
                "human",
                "Write a concise summary suggesting the fit of the applicant to the role. What are the main strengths? What he should emphasize for his advantage and what he may omit? Write conise, actionable summary",
            ),
        ]
    )
    prompt = prompt.format_messages(cv=cv, role=role)
    logger.info("Invoked LLM", prompt=prompt)
    return llm.invoke(prompt).text


def suggest_modification(cv: str, role_fit_summary: str) -> Modification:
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are an assistant that helps to apply to jobs. Consider the following CV:\n\n{cv}\n\nAnd consider the following role fit:\n\n{role_fit_summary}",
            ),
            (
                "human",
                "Write proposed modification to the cv, especially to the summary, the job descriptions and the skills. Emphasize relevant skills and omit irrelevant details",
            ),
        ]
    )
    prompt = prompt.format_messages(cv=cv, role_fit_summary=role_fit_summary)
    logger.info("Invoked LLM", prompt=prompt)
    return llm.with_structured_output(Modification).invoke(prompt)
