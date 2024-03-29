import json

import discord
from discord.ext import commands

import lolRank
import postgresql
from processPlayer import Sort, processPlayers
    

# from discord import app_commands
# class aclient(discord.Client):
#     def __init__(self):
#         super().__init__(intents=discord.Intents.default())
#         self.synced = False

#     async def on_ready(self):
#         await self.wait_until_ready()
#         if not self.synced:
#             await tree.sync()
#             self.synced = True

# client = aclient()
# tree = app_commands.CommandTree(client)

# @tree.command(name="rank", description="Display rank of all user registered")
# async def self(interaction: discord.Interaction):
#     await interaction.response.send_message("Hello")
# client.run(token)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    token = file["discord"]["token"]


@bot.command()
async def rank(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(str(ctx.message.guild.id), args, Sort.WINRATE, False))

@bot.command()
async def chomage(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(str(ctx.message.guild.id),args, Sort.GAME, False))

@bot.command()
async def flex(ctx, *args):
    message = await ctx.send("Processing data...")
    await message.edit(content=getMessage(str(ctx.message.guild.id),args, Sort.WINRATE, True))


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)


@bot.command()
async def update(ctx, *args):
    if len(args) != 2:
        message = "Only 2 arguments expected !"
    else:
        pseudoToDelete = args[0]
        pseudoToInsert = args[1]
        postgresql.delete(pseudoToDelete, str(ctx.message.guild.id))
        postgresql.insert(pseudoToInsert, str(ctx.message.guild.id))
        message = "Pseudo " + pseudoToDelete + " updated to " + pseudoToInsert + "."
    await ctx.send(message)


@bot.command()
async def add(ctx, *args):
    pseudo = " ".join(args)
    if len(args) == 0:
        msg = "Invalid value"
    else:
        try:
            postgresql.insert(pseudo, str(ctx.message.guild.id))
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
            postgresql.delete(pseudo, str(ctx.message.guild.id))
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

def getMessage(serverId, args, sortType = Sort.WINRATE ,isFlex=False):
    if len(args) != 0:
        msg = lolRank.stats(" ".join(args), isFlex).__str__()
    else:
        players = postgresql.getAllPseudo(serverId)
        if len(players) == 0:
            msg = "No pseudo found in db add them before trying to do "
            msg+= "!flex" if isFlex else "!rank"
        else:
            msg = processPlayers(players, sortType, isFlex)

    return msg

bot.run(token)