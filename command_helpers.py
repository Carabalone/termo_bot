import discord
from discord.ext import commands
import io
import aiohttp
import json
import datetime

standard = {
    "rodrigo": {
        "termooo": 0,
        "dueto": 0,
        "quarteto": 0,
        "letreco": 0,
        "pontuação-geral": 0,
        "4x0": 0
    },
    "caraba": {
        "termooo": 0,
        "dueto": 0,
        "quarteto": 0,
        "letreco": 0,
        "pontuação-geral": 0,
        "4x0": 0
    },
    "streaks": {
        "termooo": {
            "player": "bot",    
            "count": 0
        },
        "dueto": {
            "player": "bot",    
            "count": 0
        },
        "quarteto": {
            "player": "bot",    
            "count": 0
        },
        "letreco": {
            "player": "bot",   
            "count": 0
        },
        "pontuação-geral": {
            "player": "bot",
            "count": 0
        }
    }
}

points_guide = {
    "termooo": 3,
    "dueto": 3,
    "quarteto": 3,
    "letreco": 3,
    "pontuação-geral": 1
}

players = ('caraba', 'rodrigo')

channels = tuple(x for x in points_guide.keys())

def build_move(player: str, channel: str, ts: int, four_zero=False):
    return {
        "player": player,
        "channel": channel,
        "4x0": four_zero,
    }

def stringify(data, channel, extra=""):
    points = sorted([(player, data[player][channel], data[player]["4x0"])
                     for player in players],
                    key=lambda pt: pt[1],
                    reverse=True)
    if (channel == "pontuação-geral"):
        return f'Season 3:\n{points[0][0]} - {points[0][1]} pts ({points[0][2]})\n{points[1][0]} - {points[1][1]} pts ({points[1][2]})', extra
    else:
        return f'Season 3:\n{points[0][0]} - {points[0][1]} pts\n{points[1][0]} - {points[1][1]} pts', extra


def contagem(ctx, player):
    extra = ""
    with open("contagem.json", "r") as fd:
        data = json.load(fd)
        data[player][ctx.channel.name] += points_guide[ctx.channel.name]
        channel = ctx.channel.name

        if (data["streaks"][ctx.channel.name]["player"] != player):
            if (data["streaks"][ctx.channel.name]["player"] != 'bot'):
                old_player = data["streaks"][channel]["player"].capitalize()
                old_streak = data["streaks"][channel]["count"]
                if (old_streak >= 3):
                    extra = f"{old_player}'s streak of {old_streak} days was stopped 🤚🚫"

            data["streaks"][ctx.channel.name]["player"] = player
            data["streaks"][ctx.channel.name]["count"] = 1
        else:
            data["streaks"][ctx.channel.name]["count"] += 1
        
    with open("contagem.json", "w") as fd:
        json.dump(data, fd)
        return stringify(data, ctx.channel.name, extra = extra)


def four_zero(ctx, player):
    with open("contagem.json", "r") as fd:
        data = json.load(fd)
        data[player]["pontuação-geral"] += 1
        data[player]["4x0"] += 1
    with open("contagem.json", "w") as fd:
        json.dump(data, fd)
        return stringify(data, ctx.channel.name)


def open_points():
    with open("contagem.json", "r") as fd:
        data = json.load(fd)
    return data


def reset_helper():
    with open("contagem.json", "w") as fd:
        print(standard)
        json.dump(standard, fd)

def empate_helper(ctx):
    channel = ctx.channel.name
    old_player = ""
    old_streak = ""
    once = True
    extra = ""

    for player in players:
        with open("contagem.json", "r") as fd:
            data = json.load(fd)
            if once:
                old_player = data["streaks"][channel]["player"].capitalize()
                old_streak = data["streaks"][channel]["count"]
                once = False
            data[player][ctx.channel.name] += 1

            data["streaks"][ctx.channel.name]["player"] = "bot"
            data["streaks"][ctx.channel.name]["count"] = 0

        with open("contagem.json", "w") as fd:
            json.dump(data, fd)

    print(old_player)
    print(old_streak)
    if (old_player != "" and old_player.lower() != "bot" and old_streak >= 3):
        extra = f"{old_player}'s streak of {old_streak} days was stopped 🤚🚫"

    return stringify(data, ctx.channel.name, extra=extra)

def streak_helper(channel):
    string = ""

    with open("contagem.json", "r") as fd:
        data = json.load(fd)
        player = data["streaks"][channel]["player"].capitalize()
        days = data["streaks"][channel]["count"]

        if (player != "bot" and days >= 3):
            return f"{player} has been winning for {days} days straight 🔥"
        elif (player == "bot"):
            return "There is no streak"
        else:
            return ""

def streaks_helper():

    string = ""

    with open("contagem.json", "r") as fd:
        data = json.load(fd)
        for channel in points_guide.keys():
            player = data["streaks"][channel]["player"].capitalize()
            days = data["streaks"][channel]["count"]
            if player == "Bot":
                continue
            string += f"{channel.capitalize()}: {player} has a streak of {days} days\n"
    return string
