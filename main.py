import discord
from discord.ext import commands
from dotenv import load_dotenv
from ollama import chat
from ollama import ChatResponse
import os
import time


load_dotenv()

# dot env is used to safely load the token number and client id required for the bot to work
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="/", intents=intents)
@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user.name}")

@bot.command(name='hello')
async def hello(context):
    await context.send("Hello I am a Botanium. How Can I help You today?")

@bot.command(name='ask')
async def ask(context, *, message):
    await context.send("Let me think ... ")
    response: ChatResponse = chat(model='llama3.1:8b', messages=[
        {
            'role': 'system',
            'content': "You are a helpful assistant who provides answers to questions in no more than 1000 words.",
        }
        ,
        {
            'role': 'user',
            'content': message,
        },
    ])
    print(response['message']['content'])
    await context.send(response['message']['content'])

@bot.command(name='summarize')
async def summarize(context):
    await context.send("Ok. On it right now ...")

    msgs = [message.content async for message in context.channel.history(limit=50)]

    summarize_prompt = f"""
            Please Summarize this following messages delimited by 3 backticks:
            ```
            {msgs}
            ```
    """

    await context.send("I have read last 50 conversations. Now I will start summarizing.")

    response: ChatResponse = chat(model='llama3.1:8b', messages=[
        {
            'role': 'system',
            'content': "You are a helpful assistant who summarizes the provided messages in no more than 1000 words. If you find any links inside the message or a message itself is a link, consider them as crucial links, and then list all those links in a chronological order.",
        }
        ,
        {
            'role': 'user',
            'content': summarize_prompt,
        },
    ])
    await context.send(response['message']['content'])

@bot.command(name='who_sent_this')
async def who_sent_this(context,  *, message):
    await context.send("Ok. I am looking...")
    msgs = [(msg.author.name, msg.content) async for msg in context.channel.history(limit=50) if message in msg.content]
    await context.send(f"Total Messages Found : {len(msgs)}")
    for user_name, user_message in msgs:
        filtered = user_message.replace('/who_sent_this', '')
        filtered = filtered.replace('/summarize', '')
        filtered = filtered.replace('/ask ', '')
        filtered = filtered.replace('/hello', '')
        await context.send(f"User : {user_name}\nMessage : {filtered}")
        time.sleep(0.1)



bot.run(DISCORD_BOT_TOKEN)





