import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.http import HttpTool
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

'''
{
  "fact": "Cats with long, lean bodies are more likely to be outgoing, and more protective and vocal than those with a stocky build.",
  "length": 121
}
'''
fact_schema = {
    "type": "object",
    "properties": {
        "fact": {
            "type": "string",
            "description": "The fact statement to store"
        },
        "length": {
            "type": "integer",
            "description": "The length of the fact in characters"
        }
    },
    "required": ["fact", "length"]
}


http_tool = HttpTool(
    name="cat_fact_api",
    description="get a cool fact about cat",
    scheme="https",
    host="catfact.ninja",
    port=443,
    path="/fact",
    method="GET",
    return_type="json",
    json_schema=fact_schema,
)


agent  = AssistantAgent(

name ='CatFactAgent',
model_client=model_client,

system_message='you are a helpful assistant that can provide cat facts using cat_fact_api.Give the result with summary',
tools=[http_tool],
reflect_on_tool_use=True
)


async def main():
    result= await agent.run(task="give a random fact about cat")
    print(result.messages)
    # print(result.messages[-1].content)
if(__name__=="__main__"):
    asyncio.run(main())
