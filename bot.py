import discord
from discord.ext import commands

import postgresql
import lolRank

bot = commands.Bot(command_prefix='!')

# Token discord
token = "Nzk1NTg3MjI2MDk5OTA4NjU5.X_LiVw.nhUhkoAoajBRFZwzglEIH9JcRUA"

tableName = "PIPIGANG"

urlOPGG = "https://euw.op.gg/summoner/userName="


@bot.command()
async def rank(ctx, *args):
    global t
    msg = ""
    players = postgresql.getAllPseudo(tableName)
    if len(args) != 0:
        msg = lolRank.stats(" ".join(args))
    elif len(players) == 0:
        msg = "No pseudo found in db add them before trying to do !rank"
    else:
        for i in range(len(players)):
            msg += lolRank.stats(players[i])
    await ctx.send(msg)


@bot.command()
async def flex(ctx, *args):
    msg = ""
    players = postgresql.getAllPseudo(tableName)
    if len(args) != 0:
        msg = lolRank.stats(" ".join(args), True)
    elif len(players) == 0:
        msg = "No pseudo found in db add them before trying to do !flex"
    else:
        for i in range(len(players)):
            msg += lolRank.stats(players[i], True)

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


bot.run(token)
