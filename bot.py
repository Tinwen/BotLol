import random

import discord
from discord.ext import commands

import lolRank
import postgresql

bot = commands.Bot(command_prefix='!')

# Token discord
token = "Nzk1NTg3MjI2MDk5OTA4NjU5.X_LiVw.nhUhkoAoajBRFZwzglEIH9JcRUA"

mot = ["ABAISSÉ", "ABANDONNÉ", "ABCEDÉ", "ABDIQUÉ", "ABEILLÉ", "ABÉ", "ABERRÉ", "ABHORRÉ", "ABIMÉ", "ABJURÉ", "ABLATÉ",
       "ABLIÉ", "ABLOQUÉ", "ABOMINÉ", "ABONDÉ", "ABONNÉ", "ABORDÉ", "ABORNÉ", "ABOUCHÉ", "ABOULÉ", "ABOUTÉ", "ABOYÉ",
       "ABRASÉ", "ABREGÉ", "ABREUVÉ", "ABRICOTÉ", "ABRICOTIÉ", "ABRIÉ", "ABRITÉ", "ABROGÉ", "ABSENTÉ", "ABSORBÉ",
       "ABUSÉ", "ABUTÉ", "ACAGNARDÉ", "ACCABLÉ", "ACCAPARÉ", "ACCASTILLÉ", "ACCEDÉ", "ACCELERÉ", "ACCENTUÉ", "ACCEPTÉ",
       "ACCESSOIRISÉ", "ACCIDENTÉ", "ACCLAMÉ", "ACCLIMATÉ", "ACCOINTÉ", "ACCOLÉ", "ACCOMMODÉ", "ACCOMPAGNÉ", "ACCONIÉ",
       "ACCORDÉ", "ACCORÉ", "ACCOSTÉ", "ACCOTÉ", "ACCOUCHÉ", "ACCOUDÉ", "ACCOUÉ", "ACCOUPLÉ", "ACCOUTRÉ", "ACCOUTUMÉ",
       "ACCOUVÉ", "ACCREDITÉ", "ACCRETÉ", "ACCROCHÉ", "ACCULÉ", "ACCULTURÉ", "ACCUMULÉ", "ACCUSÉ", "ACENSÉ", "ACERÉ",
       "ACETIFIÉ", "ACETOBACTÉ", "ACETYLÉ", "ACHALANDÉ", "ACHALÉ", "ACHARNÉ", "ACHEMINÉ", "ACHETÉ", "ACHEVÉ", "ACHOPPÉ",
       "ACHROMATISÉ", "ACIDIFIÉ", "ACIDULÉ", "ACIÉ", "ACIERÉ", "ACONIÉ", "ACOQUINÉ", "ACQUIESCÉ", "ACQUITTÉ", "ACTÉ",
       "ACTIONNÉ", "ACTIVÉ", "ACTUALISÉ", "ADAPTÉ", "ADDITIONNÉ", "ADHERÉ", "ADJECTIVÉ", "ADJECTIVISÉ", "ADJUGÉ",
       "ADJURÉ", "ADMINISTRÉ", "ADMIRÉ", "ADMONESTÉ", "ADONNÉ", "ADOPTÉ", "ADORÉ", "ADORNÉ", "ADOSSÉ", "ADOUBÉ",
       "ADRESSÉ", "ADSORBÉ", "ADULÉ", "ADULTERÉ", "ADVERBIALISÉ", "AERÉ", "AEROSTIÉ", "AFFABULÉ", "AFFAIRÉ", "AFFAISSÉ",
       "AFFAITÉ", "AFFALÉ", "AFFAMÉ", "AFFEAGÉ", "AFFECTÉ", "AFFECTIONNÉ", "AFFERÉ", "AFFERMÉ", "AFFICHÉ", "AFFILÉ",
       "AFFILIÉ", "AFFINÉ", "AFFIRMÉ", "AFFLEURÉ", "AFFLIGÉ", "AFFLOUÉ", "AFFLUÉ", "AFFOLÉ", "AFFOUAGÉ", "AFFOUILLÉ",
       "AFFOURAGÉ", "AFFOURCHÉ", "AFFOURRAGÉ", "AFFRETÉ", "AFFRIANDÉ", "AFFRICHÉ", "AFFRIOLÉ", "AFFRONTÉ", "AFFRUITÉ",
       "AFFUBLÉ", "AFFUTÉ", "AFRICANISÉ", "AFRIKAANDÉ", "AFRIKANDÉ", "AFRIKANÉ", "AFTÉ", "AGACÉ", "AGENCÉ", "AGENCIÉ",
       "AGENDÉ", "AGENOUILLÉ", "AGGLOMERÉ", "AGGLUTINÉ", "AGGRAVÉ", "AGIOTÉ", "AGITÉ", "AGNELÉ", "AGONISÉ", "AGRAFÉ",
       "AGRAINÉ", "AGREÉ", "AGREGÉ", "AGREMENTÉ", "AGRESSÉ", "AGRIFFÉ", "AGRIPPÉ", "AGROFORESTIÉ", "AGUICHÉ", "AGUILLÉ",
       "AHANÉ", "AHEURTÉ", "AICHÉ", "AIDÉ", "AIGUILLÉ", "AIGUILLETÉ", "AIGUILLIÉ", "AIGUILLONNÉ", "AIGUISÉ", "AILIÉ",
       "AILLÉ", "AIMANTÉ", "AIMÉ", "AIRÉ", "AISSELIÉ", "AJOINTÉ", "AJOURÉ", "AJOURNÉ", "AJOUTÉ", "AJUSTÉ", "ALAMBIQUÉ",
       "ALANDIÉ", "ALARMÉ", "ALBATRIÉ", "ALBERGIÉ", "ALCALINISÉ", "ALCOOLIÉ", "ALCOOLISÉ", "ALERTÉ", "ALESÉ", "ALEVINÉ",
       "ALEVINIÉ", "ALFATIÉ", "ALIBOUFIÉ", "ALIENÉ", "ALIGNÉ", "ALIMENTÉ", "ALISIÉ", "ALITÉ", "ALIZIÉ", "ALLAITÉ",
       "ALLECHÉ", "ALLEGÉ", "ALLEGORISÉ", "ALLEGUÉ", "ALLÉ", "ALLEUTIÉ", "ALLIÉ", "ALLONGÉ", "ALLOUCHIÉ", "ALLOUÉ",
       "ALLUMÉ", "ALLUMETTIÉ", "ALLUVIONNÉ", "ALOUCHIÉ", "ALPAGUÉ", "ALPÉ", "ALPHABETISÉ", "ALTÉ", "ALTERÉ", "ALTERNÉ",
       "ALTIÉ", "ALUMINÉ", "ALUMINIÉ", "ALUNÉ", "ALZHEIMÉ", "AMADOUÉ", "AMADOUVIÉ", "AMALGAMÉ", "AMANCHÉ", "AMANDIÉ",
       "AMARINÉ", "AMARRÉ", "AMASSÉ", "AMBIANCÉ", "AMBIFIÉ", "AMBITIONNÉ", "AMBLÉ", "AMBRÉ", "AMBULANCIÉ", "AMELANCHIÉ",
       "AMELIORÉ", "AMENAGÉ", "AMENDÉ", "AMENÉ", "AMENUISÉ", "AMÉ", "AMERICANISÉ", "AMEULONNÉ", "AMEUTÉ", "AMIDONNÉ",
       "AMIDONNIÉ", "AMNISTIÉ", "AMOCHÉ", "AMODIÉ", "AMONCELÉ", "AMORCÉ", "AMORDANCÉ", "AMOUILLÉ", "AMOURACHÉ",
       "AMPLIFIÉ", "AMPUTÉ", "AMURÉ", "AMUSÉ", "AMYLOBACTÉ", "ANACARDIÉ", "ANALYSÉ", "ANASTOMOSÉ", "ANATHEMATISÉ",
       "ANATHEMISÉ", "ANATOMISÉ", "ANCRÉ", "ANDAINÉ", "ANDOUILLÉ", "ANECDOTIÉ", "ANECDOTISÉ", "ANEMIÉ", "ANESTHESIÉ",
       "ANGELISÉ", "ANGIOSCANNÉ", "ANGLAISÉ", "ANGLEDOZÉ", "ANGLICISÉ", "ANGOISSÉ", "ANHELÉ", "ANIÉ", "ANIMALIÉ",
       "ANIMALISÉ", "ANIMÉ", "ANISÉ", "ANKYLOSÉ", "ANNELÉ", "ANNEXÉ", "ANNIHILÉ", "ANNONCÉ", "ANNONCIÉ", "ANNONIÉ",
       "ANNOTÉ", "ANNUALISÉ", "ANNULÉ", "ANODISÉ", "ANONIÉ", "ANONNÉ", "ANONYMISÉ", "ANTAGONISÉ", "ANTEPOSÉ",
       "ANTHROPISÉ", "ANTIBELIÉ", "ANTICIPÉ", "ANTIDATÉ", "ANTIPARASITÉ", "AOUTÉ", "APAISÉ", "APANAGÉ", "APETISSÉ",
       "APEURÉ", "APIGEONNÉ", "APIQUÉ", "APITOYÉ", "APLOMBÉ", "APOSTASIÉ", "APOSTÉ", "APOSTILLÉ", "APOSTROPHÉ",
       "APPAIRÉ", "APPAREILLÉ", "APPARENTÉ", "APPARIÉ", "APPATÉ", "APPELÉ", "APPERTISÉ", "APPLIQUÉ", "APPOINTÉ",
       "APPONTÉ", "APPORTÉ", "APPOSÉ", "APPRECIÉ", "APPREHENDÉ", "APPRETÉ", "APPRIVOISÉ", "APPROCHÉ", "APPROPRIÉ",
       "APPROUVÉ", "APPROVISIONNÉ", "APPUYÉ", "APURÉ", "AQUARELLÉ", "ARABISÉ", "ARACHIDIÉ", "ARASÉ", "ARBALETRIÉ",
       "ARBITRÉ", "ARBORÉ", "ARBORISÉ", "ARBOUSIÉ", "ARBRIÉ", "ARCBOUTÉ", "ARCHÉ", "ARCHETIÉ", "ARCHICHANCELIÉ",
       "ARCHITECTURÉ", "ARCHIVÉ", "ARCONNÉ", "ARDOISÉ", "ARDOISIÉ", "AREQUIÉ", "ARETIÉ", "ARGANIÉ", "ARGENTÉ",
       "ARGENTIÉ", "ARGOTIÉ", "ARGOUSIÉ", "ARGUÉ", "ARGUMENTÉ", "ARISÉ", "ARMÉ", "ARMORIÉ", "ARMURIÉ", "ARNAQUÉ",
       "AROMATISÉ", "ARPEGÉ", "ARPENTÉ", "ARQUEBUSIÉ", "ARQUÉ", "ARRACHÉ", "ARRAISONNÉ", "ARRANGÉ", "ARRENTÉ",
       "ARRERAGÉ", "ARRETÉ", "ARRIERÉ", "ARRIMÉ", "ARRISÉ", "ARRIVÉ", "ARROGÉ", "ARROSÉ", "ARSOUILLÉ", "ARTHROSCANNÉ",
       "ARTICULÉ", "ARTIFICIALISÉ", "ARTIFICIÉ", "ARYANISÉ", "ASCENSIONNÉ", "ASEPTISÉ", "ASPERGÉ", "ASPHALTÉ",
       "ASPHALTIÉ", "ASPHYXIÉ", "ASPIRÉ", "ASSAISONNÉ", "ASSARMENTÉ", "ASSASSINÉ", "ASSECHÉ", "ASSEMBLÉ", "ASSENÉ",
       "ASSERMENTÉ", "ASSIBILÉ", "ASSIEGÉ", "ASSIGNÉ", "ASSIMILÉ", "ASSISTÉ", "ASSOCIÉ", "ASSOIFFÉ", "ASSOLÉ",
       "ASSOMMÉ", "ASSONÉ", "ASSUMÉ", "ASSURÉ", "ASTÉ", "ASTICOTÉ", "ASTIQUÉ", "ATELIÉ", "ATERMOYÉ", "ATOCATIÉ",
       "ATOMISÉ", "ATROPHIÉ", "ATTABLÉ", "ATTACHÉ", "ATTAQUÉ", "ATTARDÉ", "ATTELÉ", "ATTENTÉ", "ATTENUÉ", "ATTERRÉ",
       "ATTESTÉ", "ATTIÉ", "ATTIFÉ", "ATTIGÉ", "ATTINÉ", "ATTIRÉ", "ATTISÉ", "ATTITRÉ", "ATTOQUÉ", "ATTRAPÉ",
       "ATTREMPÉ", "ATTRIBUÉ", "ATTRIQUÉ", "ATTRISTÉ", "ATTROUPÉ", "AUBIÉ", "AUBINÉ", "AUDIENCÉ", "AUDIENCIÉ",
       "AUDIOGUIDÉ", "AUDITÉ", "AUDITIONNÉ", "AUGMENTÉ", "AUGURÉ", "AUMONIÉ", "AUNÉ", "AUREOLÉ", "AURIFIÉ", "AUSCULTÉ",
       "AUTHENTIFIÉ", "AUTHENTIQUÉ", "AUTOANALYSÉ", "AUTOCENSURÉ", "AUTOCRITIQUÉ", "AUTODETERMINÉ", "AUTOEVALUÉ",
       "AUTOFECONDÉ", "AUTOFINANCÉ", "AUTOFLAGELLÉ", "AUTOFORMÉ", "AUTOGERÉ", "AUTOGRAPHIÉ", "AUTOMATISÉ",
       "AUTOMEDIQUÉ", "AUTOMUTILÉ", "AUTONOMISÉ", "AUTOPROCLAMÉ", "AUTOPSIÉ", "AUTOREGULÉ", "AUTOREPLIQUÉ", "AUTORISÉ",
       "AUTOROUTIÉ", "AUTOURSIÉ", "AVALÉ", "AVALISÉ", "AVANCÉ", "AVANTAGÉ", "AVARIÉ", "AVELINIÉ", "AVENTURÉ",
       "AVENTURIÉ", "AVERÉ", "AVEUGLÉ", "AVINÉ", "AVIRONNÉ", "AVISÉ", "AVITAILLER"]


@bot.command()
async def louis(ctx):
    nb = random.randrange(0, len(mot) - 1)
    await ctx.send("Je suis " + str(mot[nb]).lower() + " de rire")


tableName = "PIPIGANG"

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
