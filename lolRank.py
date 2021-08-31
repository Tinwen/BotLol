from riotwatcher import LolWatcher
import json
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='example.log')

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    api_key = file["riot"]["token"]

lol_watcher = LolWatcher(api_key)
region = 'EUW1'


def stats(pseudo, isFlex=False):
    res = ""
    rankedType = "RANKED_SOLO_5x5"
    queueType = "Solo/Duo Q"
    winRate = 0
    found = False
    if isFlex:
        rankedType = "RANKED_FLEX_SR"
        queueType = "Flex"
    try:
        summoners = lol_watcher.summoner.by_name(region, pseudo)  # can throw error here (invalid pseudo)
        ranked_stats = lol_watcher.league.by_summoner(region, summoners['id'])
        if ranked_stats is not None and len(ranked_stats) > 0:
            for i in range(len(ranked_stats)):
                if ranked_stats[i]["queueType"] == rankedType:
                    found = True
                    totalGame = int(ranked_stats[i]["wins"]) + int(ranked_stats[i]["losses"])
                    winRate = round(int(ranked_stats[i]["wins"]) / totalGame * 100, 2)
                    res += (str(ranked_stats[i]["summonerName"]) +
                            " is currently **" + str(ranked_stats[i]["tier"]).capitalize() + " " +
                            str(ranked_stats[i]["rank"]) + "** (" + str(
                                ranked_stats[i]["leaguePoints"]) + " LP) in " + str(
                                queueType)) + ". ( **" + str(winRate) + " %** for *" + str(totalGame) + " games* )\n"
        if not found:
            res = "Not enough ranked game played on this account " + str(pseudo) + ".\n"
    except Exception as inst:
        logging.error(inst)
        res = "Invalid/Non-existing username ( " + pseudo + " )\n"
    return res, winRate