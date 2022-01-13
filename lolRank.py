from riotwatcher import LolWatcher
import json
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='example.log')

with open("keys.json") as json_data_file:
    file = json.load(json_data_file)
    api_key = file["riot"]["token"]

lol_watcher = LolWatcher(api_key)
region = 'EUW1'


def stats(pseudo, isFlex=False):
    player = Player(pseudo)
    player.queueType = "RANKED_SOLO_5x5"
    if isFlex:
        player.queueType = "RANKED_FLEX_SR"
    try:
        summoners = lol_watcher.summoner.by_name(region, pseudo)
        ranked_stats = lol_watcher.league.by_summoner(region, summoners['id'])
        if ranked_stats is not None and len(ranked_stats) > 0:
            for i in range(len(ranked_stats)):
                if ranked_stats[i]["queueType"] == player.queueType:
                    player.found = True
                    player.rank = ranked_stats[i]["rank"]
                    player.tier = ranked_stats[i]["tier"]
                    player.leaguePoints = ranked_stats[i]["leaguePoints"]
                    player.nbGame = int(ranked_stats[i]["wins"]) + int(ranked_stats[i]["losses"])
                    player.winRate = round(int(ranked_stats[i]["wins"]) / player.nbGame * 100, 2)
    except:
        player.exist = False
    finally:
        return player


class Player:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.found = False
        self.leaguePoints = 0
        self.queueType = "RANKED_SOLO_5x5"
        self.winRate = 0
        self.nbGame = 0
        self.rank = ""
        self.tier = ""
        self.exist = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self.found:
            if self.exist:
                return "Not enough ranked game played on this account __" + self.pseudo + "__."
            else:
                return "Invalid/Non-existing username (__" + self.pseudo + "__)."
        else:
            queueName = "Solo/Duo Q" if self.queueType == "RANKED_SOLO_5x5" else "Flex"
            return "__"+self.pseudo + "__ is currently **" + self.tier.capitalize() + " " + self.rank + "** (" + str(
                self.leaguePoints) + " LP) in " + queueName + ". ( **" + str(
                self.winRate) + " %** for *" + str(self.nbGame) + " games*)"
