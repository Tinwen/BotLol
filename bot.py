import discord
from discord.ext import commands
import json

import lolRank
import postgresql

bot = commands.Bot(command_prefix='!')

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    token = file["discord"]["token"]
    tableName = file["tableName"]+str("oui")

urlOPGG = "https://euw.op.gg/summoner/userName="

@bot.command()
async def rank(ctx, *args):
    msg = ""
    players = postgresql.getAllPseudo(tableName)
    if len(args) != 0:
        msg, winRate = lolRank.stats(" ".join(args))
    elif len(players) == 0:
        msg = "No pseudo found in db add them before trying to do !rank"
    else:
        msg += sortByWinRate(players)
    await ctx.send(msg)


@bot.command()
async def flex(ctx, *args):
    msg = ""
    players = postgresql.getAllPseudo(tableName)
    if len(args) != 0:
        msg, winRate = lolRank.stats(" ".join(args), True)
    elif len(players) == 0:
        msg = "No pseudo found in db add them before trying to do !flex"
    else:
        msg += sortByWinRate(players, True)

    await ctx.send(msg)


@bot.event
async def on_ready():
    print("Connected")
    postgresql.createTable(tableName)
    await bot.change_presence(status=discord.Status.idle)


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
async def opgg(ctx, *args):
    msg = ""
    players = postgresql.getAllPseudo(tableName)
    if len(args) != 0:
        pseudo = " ".join(args).replace(" ", "+")
        msg = "**" + str(" ".join(args)) + "** : " + urlOPGG + str(pseudo) + "\n"
    elif len(players) == 0:
        msg = "No pseudo found in database"
    else:
        for i in range(len(players)):
            pseudo = players[i].replace(" ", "+")
            msg += "**" + str(players[i]) + "** : " + urlOPGG + str(pseudo) + "\n"

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
    res = dict()
    result = ""
    for item in pseudo:
        stats, winRate = lolRank.stats(item, isFlex)
        res[stats] = winRate
    res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}
    t = []
    for item in list(res.items()):
        t.append(item[0])
    t.reverse()
    for msg in t:
        result += msg
    return result


bot.run(token)
