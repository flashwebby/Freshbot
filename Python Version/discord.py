import discord
from discord.ext import commands
from datetime import datetime, timedelta
import aiohttp

# Replace with your actual bot token
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
# Replace with your actual Gemini API key
GEMINI_API_KEY = 'YOUR_API_KEY'
GEMINI_MODEL = 'gemini-1.5-flash'
MAX_TOKENS = 32768  # Maximum input size for the gemini-pro model

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

async def fetch_messages(channel, duration_hours):
    import discord
    from discord.ext import commands
    from datetime import datetime, timedelta
    import aiohttp

    # Replace with your actual bot token
    DISCORD_TOKEN = ':)'
    # Replace with your actual Gemini API key
    GEMINI_API_KEY = ':)'
    GEMINI_MODEL = 'gemini-1.5-flash'
    MAX_TOKENS = 32768  # Maximum input size for the gemini-pro model

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    async def fetch_messages(channel, duration_hours):
        after_time = datetime.utcnow() - timedelta(hours=duration_hours)
        messages = []
        async for message in channel.history(after=after_time, limit=None):
            messages.append(message.content)
        return messages

    async def summarize_text(text):
        # Check if the input text is empty
        if not text.strip():
            return "No relevant information found in the specified duration."

        # Check if the input text exceeds the maximum token limit
        if len(text) > MAX_TOKENS:
            return f"The input text exceeds the maximum token limit of {MAX_TOKENS} tokens. Please try summarizing a shorter duration."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                print(f"API Request: {payload}")  # Log request payload for debugging
                print(f"API Response Status: {response.status}")  # Log response status for debugging
                print(f"API Response Headers: {response.headers}")  # Log response headers for debugging
                print(f"API Response Text: {await response.text()}")  # Log response text for debugging
                if response.status == 200:
                    data = await response.json()
                    return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Failed to summarize the text.')
                else:
                    return f"Failed to summarize the text. API response code: {response.status}"

    @bot.command()
    async def summarize(ctx):
        try:
            duration_hours = 3

            messages = await fetch_messages(ctx.channel, duration_hours)
            if not messages:
                await ctx.send("No messages found in the specified duration.")
                return

            text = " ".join(messages)

            summary = await summarize_text(text)
            await ctx.send(summary)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    bot.run(DISCORD_TOKEN)

    messages = []
    async for message in channel.history(after=after_time, limit=None):
        messages.append(message.content)
    return messages

async def summarize_text(text):
    # Check if the input text is empty
    if not text.strip():
        return "No relevant information found in the specified duration."

    # Check if the input text exceeds the maximum token limit
    if len(text) > MAX_TOKENS:
        return f"The input text exceeds the maximum token limit of {MAX_TOKENS} tokens. Please try summarizing a shorter duration."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            print(f"API Request: {payload}")  # Log request payload for debugging
            print(f"API Response Status: {response.status}")  # Log response status for debugging
            print(f"API Response Headers: {response.headers}")  # Log response headers for debugging
            print(f"API Response Text: {await response.text()}")  # Log response text for debugging
            if response.status == 200:
                data = await response.json()
                return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Failed to summarize the text.')
            else:
                return f"Failed to summarize the text. API response code: {response.status}"

@bot.command()
async def summarize(ctx):
    try:
        duration_hours = 3

        messages = await fetch_messages(ctx.channel, duration_hours)
        if not messages:
            await ctx.send("No messages found in the specified duration.")
            return

        text = " ".join(messages)

        summary = await summarize_text(text)
        await ctx.send(summary)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

bot.run(DISCORD_TOKEN)
