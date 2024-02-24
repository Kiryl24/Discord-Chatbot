import discord
from discord.ext import commands
import json

TOKEN = 'DISCORD_BOT_TOKEN'

TARGET_CHANNEL_ID = #channel ID

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data_from_file(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    return data

DATA_FILE = 'data.json'

questions_and_answers = load_data_from_file(DATA_FILE)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    await observe_channel(channel)

async def observe_channel(channel):
    async for message in channel.history(limit=None):
        if message.author != bot.user:
            await learn_from_message(message)

async def learn_from_message(message):
    content = message.content.split('::')
    if len(content) == 2:
        question, answer = content
        questions_and_answers[question.strip()] = answer.strip()
        save_data_to_file(questions_and_answers, DATA_FILE)
        print(f"Zainicjalizowano: {question.strip()} -> {answer.strip()}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(''):
        question = message.content[len(''):].strip()
        if question in questions_and_answers:
            await message.channel.send(questions_and_answers[question])

    if message.content.startswith('!'):
        content = message.content[len('!'):].strip()
        try:
            question, answer = content.split('::')
            questions_and_answers[question.strip()] = answer.strip()
            save_data_to_file(questions_and_answers, DATA_FILE)
            print(f"Zainicjalizowano: {question.strip()} -> {answer.strip()}")
            await message.channel.send(f"Zainicjalizowano: {question.strip()} -> {answer.strip()}")
        except ValueError:
            await message.channel.send("Podaj pytanie i odpowiedź w formacie: ! pytanie::odpowiedź")

    await bot.process_commands(message)
bot.run(TOKEN)
