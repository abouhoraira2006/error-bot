import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('levels.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS levels
             (user_id TEXT PRIMARY KEY, level INTEGER, exp INTEGER)''')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    c.execute('SELECT * FROM levels WHERE user_id=?', (user_id,))
    result = c.fetchone()

    if result is None:
        c.execute('INSERT INTO levels VALUES (?, ?, ?)', (user_id, 0, 0))
    else:
        exp = result[2] + 1
        level = result[1]
        if exp >= level * 100:
            exp = 0
            level += 1
            await message.channel.send(f'{message.author.mention} مستواك الجديد هو {level}!')
        c.execute('UPDATE levels SET level=?, exp=? WHERE user_id=?', (level, exp, user_id))

    conn.commit()
    await bot.process_commands(message)


@bot.command()
async def stats(ctx):
    user_id = str(ctx.author.id)
    c.execute('SELECT * FROM levels WHERE user_id=?', (user_id,))
    result = c.fetchone()

    if result is None:
        embed=discord.Embed(title="Levels", description="Show levels", color=0xdd0239)
        embed.add_field(name="Level", value="You hav not level now", inline=False)
        await ctx.send(embed=embed)
    else:
        level = result[1]
        exp = result[2]
        embed=discord.Embed(title="Levels", description="Show levels", color=0x0070df)
        embed.add_field(name="Level", value="*****{level}*", inline=False)
        embed.add_field(name="Xp", value="***{exp}***", inline=True)
        await ctx.send(embed=embed)

@bot.remove_command("help")
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help Command", description="show command of bot")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1093505126091735040/1112308803971584050/code-syntax-dark-minimal-4k-mr.jpg?width=375&height=250")
    embed.add_field(name="prefix", value="***!***", inline=True)
    embed.add_field(name="level", value="***stats***", inline=False)
    embed.add_field(name="list", value="leaderboard", inline=True)
    embed.set_footer(text="beata version")
    await ctx.send(embed=embed)

To = 'OTU2MTgyMTM5OTk1NTUzODQy'
ke = '.G_19bR.umqMjRn_'
ns = 'qiMlxUe9QDNPp0kaSGKPbeoOWllQlE'
Token = To + ke + ns
bot.run(Token)
