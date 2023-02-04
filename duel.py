import time
import os
import discord
import math
import random


async def run_duel(player1, player2, message):
    embed = discord.Embed(title="Lost Duel")
    embed.add_field(name="", value="{} vs {}".format(player1, player2))
    await message.send(embed=embed)
    p1hp = 10
    p2hp = 10

    while p1hp > 0 or p2hp > 0:

        embed_indv_match = discord.Embed()
        p1_attack = random.randint(1, 4)
        p2_attack = random.randint(1, 4)

        p1hp -= p2_attack
        p2hp -= p1_attack

        if p1hp < 0:
            p1hp = 0
        if p2hp < 0:
            p2hp = 0

        p1_health_bar = ("❤️ " * p1hp) + ("♡ " * (10 - p1hp))
        p2_health_bar = ("❤️ " * p2hp) + ("♡ " * (10 - p2hp))

        embed_indv_match.add_field(name="",
                                   value="**{}** attacked **{}** for **{}** damage!"
                                         "\n**{}** attacked **{}** for **{}** damage!".format(
                                       player1,
                                       player2,
                                       p1_attack,
                                       player2,
                                       player1,
                                       p2_attack),
                                   inline=False)
        embed_indv_match.add_field(name="".format(),
                                   value="**{}**\n[{}]\n==========\n**{}**\n[{}] ".format(player1,
                                                                                       p1_health_bar,
                                                                                       player2,
                                                                                       p2_health_bar),
                                   inline=False)

        await message.send(embed=embed_indv_match)
        time.sleep(3)

        if p2hp == 0 or p1hp == 0:
            break
    embed_final = discord.Embed()
    if p1hp == 0 and p2hp == 0:
        p1_attack = random.randint(1, 4)
        p2_attack = random.randint(1, 4)
        while p1_attack == p2_attack:
            p1_attack = random.randint(1, 4)
            p2_attack = random.randint(1, 4)

        if p1_attack > p2_attack:
            winner = player1
        else:
            winner = player2
        embed_final.add_field(name="Sudden Death!", value="{} hit for {}, {} hit for {}!".format(
            player1, p1_attack, player2, p2_attack
        ))
    else:
        if p1hp == 0:
            winner = player2
        elif p2hp == 0:
            winner = player1
        else:
            print("error shouldnt get here?")

    embed_final.add_field(name="{} wins!".format(winner), value="", inline=False)
    await message.send(embed=embed_final)
