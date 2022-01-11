import json

import discord
from discord.ext import commands

import lolRank
import postgresql

bot = commands.Bot(command_prefix='!')

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    token = file["discord"]["token"]
    tableName = file["tableName"]


@bot.command()
async def rank(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(args, False))


@bot.command()
async def flex(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(args, True))


@bot.event
async def on_ready():
    postgresql.createTable(tableName)
    await bot.change_presence(status=discord.Status.online)


@bot.command()
async def add(ctx, *args):
    pseudo = " ".join(args)
    if len(args) == 0:
        msg = "Invalid value"
    else:
        try:
            postgresql.insert(tableName, pseudo)
            msg = "Successfully added in database"
        except:
            msg = pseudo + " already in database"
    await ctx.send(msg)


@bot.command()
async def delete(ctx, *args):
    pseudo = " ".join(args)
    if len(args) == 0:
        msg = "Invalid value"
    else:
        try:
            postgresql.delete(tableName, pseudo)
            msg = "Successfully removed from database"
        except:
            msg = pseudo + " doesn't exist in database"
    await ctx.send(msg)


@bot.command()
async def h(ctx):
    msg = "- !rank <pseudo> => pseudo is optional\n" \
          "- !flex <pseudo> => pseudo is optional\n" \
          "- !add <pseudo> => add a pseudo in database\n" \
          "- !delete <pseudo> => remove a pseudo from database\n" \
          "- !opgg <pseudo> => pseudo is optional"
    await ctx.send(msg)


def sortByWinRate(pseudo, isFlex=False):
    players = []
    for item in pseudo:
        players.append(lolRank.stats(item, isFlex))
    players.sort(key=lambda x: x.winRate, reverse=True)
    result = []
    for player in players:
        result.append(player.__str__())
    return "\n".join(result)


def getMessage(args, isFlex=False):
    players = postgresql.getAllPseudo(tableName)
    if len(args) != 0:
        msg = lolRank.stats(" ".join(args), isFlex).__str__()
    elif len(players) == 0:
        msg = "No pseudo found in db add them before trying to do " + "!flex" if isFlex else "!rank"
    else:
        msg = sortByWinRate(players, isFlex)

    return msg


bot.run(token)
