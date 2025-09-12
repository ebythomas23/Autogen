import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)


assisant = AssistantAgent(
    name='Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='you are a helpful assistant who help on the task given'
)

user_proxy_agent = UserProxyAgent(
    name='UserProxy',
    description=' you are a user proxy agent',
    input_func= input
)

termination_condition = TextMentionTermination(text='APPROVE')

team = RoundRobinGroupChat(
    participants=[assisant,user_proxy_agent]
    ,termination_condition=termination_condition,
    max_turns=10
)

stream = team.run_stream(task='write a poem about australia')

async def main():
    await Console(stream)

if(__name__=='__main__'):
    asyncio.run(main())