from langchain.agents import create_agent
from langchain_groq import ChatGroq
from riplex.services.tools import web_search
from riplex.core.config import GROQ_API_KEY

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=GROQ_API_KEY,
    reasoning_format="hidden",
    temperature=0.7
)

agent = create_agent(tools=[web_search], model=llm, system_prompt="Use web_search only when external information is needed.")

def run_agent(question: str) -> str:
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return result["messages"][-1].content
