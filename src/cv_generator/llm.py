import structlog
from langchain_openai import ChatOpenAI

logger = structlog.get_logger()
model = "gpt-4o"
llm = ChatOpenAI(model=model)
logger.info("Established connection to model", model=model)
