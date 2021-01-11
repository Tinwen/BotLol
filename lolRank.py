from riotwatcher import LolWatcher

api_key = 'RGAPI-0816d219-d31d-4d11-b472-78d252bb887e'
lol_watcher = LolWatcher(api_key)
region = 'EUW1'


def stats(pseudo, isFlex=False):
    res =""
    ranked_stats = None
    rankedType = "RANKED_SOLO_5x5"
    queueType = "Solo/Duo Q"
    found = False
    if isFlex:
        rankedType = "RANKED_FLEX_SR"
        queueType = "Flex"
    try:
        ranked_stats = lol_watcher.league.by_summoner(region, lol_watcher.summoner.by_name(region, pseudo)['id'])
    except:
        res = "Invalid/Non-existing username ( " + pseudo + " )\n"

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
    return res