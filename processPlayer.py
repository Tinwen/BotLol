import enum
import lolRank
import postgresql

class Sort(enum.Enum):
    WINRATE = 0
    GAME = 1
    ELO = 2

def processPlayers(pseudo, sortType=Sort.WINRATE, isFlex=False):
  players = retrievePlayers(pseudo,isFlex)
  if sortType == Sort.WINRATE:
    players = sortByWinRate(players)
  elif sortType == Sort.GAME:
    players= sortByGameAmount(players)
  elif sortType == Sort.ELO:
    players= sortByElo(players)
  result = []
  for player in players:
        result.append(player.__str__())
  return "\n".join(result)

def retrievePlayers(pseudo, isFlex=False):
  players = []
  for item in pseudo:
      players.append(lolRank.stats(item, isFlex))
  return players

def sortByWinRate(players): 
    players.sort(key=lambda x: x.winRate, reverse=True)
    return players

def sortByGameAmount(players):
    players.sort(key=lambda x: x.nbGame, reverse=True)
    return players

def sortByElo(players):
  raise NotImplementedError
  players.sort(key=lambda x: x.winRate, reverse=True)
  return players


print(processPlayers(postgresql.getAllPseudo(), Sort.GAME, False))