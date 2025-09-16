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
    name='Writer',
    description='you are a great writer',
    model_client=model_client,
    system_message='You are a really helpful writer who writes in less than 30 words.'
)

assistant2 = AssistantAgent(
    name='Reviewer',
    description='you are a great reviewer',
    model_client=model_client,
    system_message='You are a really helpful reviewer who writes in less than 30 words..'
)

assistant3 = AssistantAgent(
    name='Editor',
    description='you are a great editor',
    model_client=model_client,
    system_message='You are a really helpful editor who writes in less than 30 words..'
)


team = RoundRobinGroupChat(
    participants=[assistant, assistant2, assistant3],
    max_turns=1
)

async def main():
    task = 'Write 3 line poem about the sky'

    while True:
        stream = team.run_stream(task=task)
        
        await Console(stream)

        feedback_from_user_or_application=input('Please Provide feedback to the team: ')

        if(feedback_from_user_or_application.lower().strip()=='exit'):
            break

        task = feedback_from_user_or_application

    
if (__name__ == '__main__'):
    asyncio.run(main())