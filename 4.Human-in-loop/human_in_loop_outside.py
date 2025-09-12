import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gpt-4o')


assistant = AssistantAgent(
    name="Writer"
    ,description='you are great writer',
    system_message='You are a helpful writer who writes less than 30 words.',
    model_client=model_client
)

assistant2 = AssistantAgent(
    name="Reviewer"
    ,description='you are great reviewer',
    system_message='You are a helpful reviewer who writes less than 30 words.',
    model_client=model_client
)

assistant3 = AssistantAgent(
    name="Editor"
    ,description='you are great editor',
    system_message='You are a helpful editor who writes less than 30 words.',
    model_client=model_client
)

team = RoundRobinGroupChat(
    participants=[assistant,assistant2,assistant3],
    max_turns=3 ## max_turn =1 gives interaction with human after each agent 
)

async def main():
    task = "Write 3 line poem about the sky"

    while True:
        stream = team.run_stream(task=task)

        await Console(stream)

        feedback_from_user_or_application = input("please provide feedback to the team: ")

        if( feedback_from_user_or_application.lower().strip()=='exit'):
            break
        task = feedback_from_user_or_application

if(__name__ == '__main__'):
    asyncio.run(main())