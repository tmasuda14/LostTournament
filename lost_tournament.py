import time
import os
import discord
import math
import random

async def run_tourney(message, tournament):
    # global tournament

    if len(tournament) < 3:
        tournament.append(('Hurklover#6969', 'Hurk', 'Mace'))
        tournament.append(('Flynn4theWin#4201', 'Flynn', 'Staff'))
        tournament.append(('BetOnChet#1337', 'Chet', 'Axe'))

    i = math.floor(len(tournament) / 2)
    if i == 0:
        await message.channel.send('Sorry, you need at least 2 people to play.')
        return
    if i % 2 != 0:
        tournament.append(('Mysterious Troll', 'Troll', 'Club'))

    contestants = []
    for i in tournament:
        contestants.append(i[0])

    # await message.channel.send(f'\nContestants are:  \n {contestants}')

    round_num = 1
    this_round = tournament
    next_round = []
    match_num = 1
    cur_winner = None
    while len(this_round) > 1 or len(next_round) > 1:
        cur_winner = None
        embed_intro = discord.Embed(title="===== ROUND {} =====".format(round_num), color=0x00ff00)
        await message.channel.send(embed=embed_intro)
        time.sleep(2)

        while len(this_round) > 1:
            player1 = this_round.pop()
            player2 = this_round.pop()

            winner = None
            p1hp = 10
            p2hp = 10
            embed_match_intro = discord.Embed(
                title="⚔️ Match [{}]: {} verses {}... FIGHT!".format(match_num, player1[0], player2[0]),
                description="", )
            await message.channel.send(embed=embed_match_intro)
            time.sleep(2)

            embed_match = discord.Embed()
            # embed_match.add_field(name="", value="", inline=True)
            # embed_match.add_field(name="", value="", inline=True)

            if player1[0] == 'Mysterious Troll':
                embed_match.add_field(name="", value="{} easily defeated 1the {}".format(player2[0], player1[0]),
                                      inline=False)

                next_round.append(player2)
                match_num += 1
                await message.channel.send(embed=embed_match)
                time.sleep(4)

            elif player2[0] == 'Mysterious Troll':
                embed_match.add_field(name="", value="{} easily defeated 2the {}".format(player1[0], player2[0]),
                                      inline=False)
                next_round.append(player1)
                match_num += 1
                await message.channel.send(embed=embed_match)
                time.sleep(4)

            else:

                while p1hp > 0 or p2hp > 0:
                    embed_indv_match = discord.Embed()
                    p1_attack = random.randint(1, 6)
                    p2_attack = random.randint(1, 6)
                    # p1_block = random.randint(1, 6)
                    # p2_block = random.randint(1, 6)
                    #
                    # p1_final = p1_attack - p2_block
                    # p2_final = p2_attack - p1_block

                    # if p1_final < 0:
                    #     p1_final = 0
                    # if p2_final < 0:
                    #     p2_final = 0
                    #
                    # p1hp -= p2_final
                    # p2hp -= p1_final
                    p1hp -= p2_attack
                    p2hp -= p1_attack

                    if p1hp < 0:
                        p1hp = 0
                    if p2hp < 0:
                        p2hp = 0

                    p1_health_bar = ("❤️ " * p1hp) + ("♡ " * (10 - p1hp))
                    p2_health_bar = ("❤️ " * p2hp) + ("♡ " * (10 - p2hp))

                    if random.random() > 0.5:
                        embed_indv_match.add_field(name="",
                                                   value="**{}** attacked **{}** for **{}** damage!"
                                                         "\n**{}** attacked **{}** for **{}** damage!".format(
                                                       player1[0],
                                                       player2[0],
                                                       p1_attack,
                                                       player2[0],
                                                       player1[0],
                                                       p2_attack),
                                                   inline=False)
                        embed_indv_match.add_field(name="".format(),
                                                   value="**{}**\n[{}]\n==========\n**{}**\n[{}] ".format(player1[0],
                                                                                                          p1_health_bar,
                                                                                                          player2[0],
                                                                                                          p2_health_bar),
                                                   inline=False)
                    else:
                        embed_indv_match.add_field(name="",
                                                   value="**{}** attacked **{}** for **{}** damage!"
                                                         "\n**{}** attacked **{}** for **{}** damage!".format(
                                                       player2[0],
                                                       player1[0],
                                                       p2_attack,
                                                       player1[0],
                                                       player2[0],
                                                       p1_attack),
                                                   inline=False)
                        embed_indv_match.add_field(name="".format(),
                                                   value="**{}**\n[{}]\n==========\n**{}**\n[{}] ".format(player2[0],
                                                                                                       p2_health_bar,
                                                                                                       player1[0],
                                                                                                       p1_health_bar),
                                                   inline=False)

                    await message.channel.send(embed=embed_indv_match)
                    time.sleep(4)

                    if p2hp == 0 or p1hp == 0:
                        break

                if p1hp == 0 and p2hp == 0:
                    p1_attack = random.randint(1, 6)
                    p2_attack = random.randint(1, 6)
                    while p1_attack == p2_attack:
                        p1_attack = random.randint(1, 6)
                        p2_attack = random.randint(1, 6)

                    if p1_attack > p2_attack:
                        winner = player1
                    else:
                        winner = player2
                    embed_match.add_field(name="Sudden Death!", value="{} hit for {}, {} hit for {}!".format(
                        player1[0], p1_attack, player2[0], p2_attack
                    ))
                else:
                    if p1hp == 0:
                        winner = player2
                    elif p2hp == 0:
                        winner = player1
                    else:
                        print("error shouldnt get here?")

                embed_match.add_field(name="{} wins match {}!".format(winner[0], match_num), value="", inline=False)
                await message.channel.send(embed=embed_match)
                cur_winner = winner
                next_round.append(winner)
                match_num += 1
                time.sleep(2)

        round_num += 1
        this_round = next_round

    embed = discord.Embed(title="CHAMPION!!!", description="🗡️ 👑 🛡️", color=0x00ff00)
    embed.add_field(name="{} wins the tournament!".format(cur_winner[0]), value="", inline=False)
    await message.channel.send(embed=embed)
    # tournament.clear()
    tournament = [('Hurklover#6969', 'Hurk', 'Mace'), ('Flynn4theWin#4201', 'Flynn', 'Staff'),
                  ('BetOnChet#1337', 'Chet', 'Axe')]



