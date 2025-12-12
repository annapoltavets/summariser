from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

CHAT_MODEL = "gpt-4o-mini"
video_transcript = ""
system_msg = (
    ""
    ""
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_msg),
        ("human", "{video_transcript}"),
    ]
)

llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
parser = StrOutputParser()
chain = prompt | llm | parser

chain.invoke({"video_transcript": video_transcript})

