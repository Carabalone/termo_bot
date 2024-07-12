import discord
from discord.ext import commands
import io
import aiohttp
import json
import datetime
from command_helpers import *
import keepalive
import os
from os import system
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents().default()
#intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))


@client.command()
async def caraba(ctx):
    msg, break_streak = contagem(ctx, 'caraba')

    await ctx.send(msg)
    if (break_streak != ""):
        await ctx.send(break_streak)
    res = streak_helper(ctx.channel.name)
    if (res != ""):
        await ctx.send(res)


@client.command()
async def rodrigo(ctx):
    msg, break_streak = contagem(ctx, 'rodrigo')

    await ctx.send(msg)
    if (break_streak != ""):
        await ctx.send(break_streak)
    res = streak_helper(ctx.channel.name)
    if (res != ""):
        await ctx.send(res)


@client.command()
async def last(ctx):
    await ctx.send(get_last())


@client.command()
async def set(ctx, arg):
    set_points(arg, ctx.channel.name)
    await ctx.send(get_last())


@client.command()
async def points(ctx):
    await ctx.send(stringify(open_points(), ctx.channel.name)[0])


@client.command()
async def reset(ctx):
    reset_helper()
    await ctx.send("resetado")


@client.command()
async def empate(ctx):
    msg, break_streak = empate_helper(ctx)

    await ctx.send(msg)
    if (break_streak != ""):
        await ctx.send(break_streak)


@client.command()
async def streaks(ctx):
    res = streaks_helper()
    if (res != ""):
        await ctx.send(streaks_helper())

@client.command()
async def streak(ctx):
    res = streak_helper(ctx.channel.name)
    if (res != ""):
        await ctx.send(res)

@client.command()
async def quatro_a_zero(ctx):
    with open("contagem.json", "r") as fd:
        json_r = json.load(fd)

        await ctx.send(four_zero(ctx, json_r["streaks"]["pontuação-geral"]["player"])[0])


try:
    #keepalive.keep_alive()
    client.run(TOKEN)
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system("python restarter.py")
#    system('kill 1')

