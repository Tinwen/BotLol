import json

import discord
from discord.ext import commands

import lolRank
import postgresql
from processPlayer import Sort, processPlayers
    
bot = commands.Bot(command_prefix='!')

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    token = file["discord"]["token"]


@bot.command()
async def rank(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(args, Sort.WINRATE, False))

@bot.command()
async def chomage(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(args, Sort.GAME, False))

@bot.command()
async def flex(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(args, Sort.WINRATE, True))


@bot.event
async def on_ready():
    postgresql.createTable()
    await bot.change_presence(status=discord.Status.online)


@bot.command()
async def update(ctx, *args):
    if len(args) != 2:
        message = "Only 2 arguments expected !"
    else:
        pseudoToDelete = args[0]
        pseudoToInsert = args[1]
        postgresql.delete(pseudoToDelete)
        postgresql.insert(pseudoToInsert)
        message = "Pseudo " + pseudoToDelete + " updated to " + pseudoToInsert + "."
    await ctx.send(message)


@bot.command()
async def add(ctx, *args):
    pseudo = " ".join(args)
    if len(args) == 0:
        msg = "Invalid value"
    else:
        try:
            postgresql.insert(pseudo)
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
            postgresql.delete(pseudo)
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
          "- !opgg <pseudo> => pseudo is optional\n" \
          "- !chomage <pseudo> => same as !rank/!flex but sort by game amount" 

    await ctx.send(msg)

def getMessage(args, sortType = Sort.WINRATE ,isFlex=False):
    if len(args) != 0:
        msg = lolRank.stats(" ".join(args), isFlex).__str__()
    else:
        players = postgresql.getAllPseudo()
        if len(players) == 0:
            msg = "No pseudo found in db add them before trying to do " + "!flex" if isFlex else "!rank"
        else:
            msg = processPlayers(players, sortType, isFlex)

    return msg

bot.run(token)