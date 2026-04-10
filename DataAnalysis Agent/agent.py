def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

from langchain_openai import ChatOpenAI
from langchain.agents import tool, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor
from setUp import Parser, Log
import environ
from toolsCollection import ToolCollection, DATAFRAME_CACHE
import inspect
##############################################################
## to do:
## create class for auto tool calling
## create class for manula tool calling
## create function for input intent sanitization
##############################################################
modelName="openai"
parser = Parser(modelName=modelName)
config = parser.load_config()

logger = Log()

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     config[modelName]['systemPrompt']),
    
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")  # Required for tool-calling agents
])

llm = init_chat_model(config[modelName]['modelName'], model_provider=config[modelName]['model_provider'], streaming=config.getboolean(modelName, 'streaming'))

tools=[value for key, value in ToolCollection.tool_map]
           
agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
agent_executor.agent.stream_runnable = False

print("Ask questions about your dataset (type 'exit' to quit):")

while True:
    user_input=input(" You:")
    if user_input.strip().lower() in ['exit','quit']:
        print("see ya later")
        break
        
    result=agent_executor.invoke({"input":user_input})
    print(f"my Agent: {result['output']}")