import os
import discord
import responses

import duel
import lost_tournament

tournament = []
duels = {}

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if response == '':
            return
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = os.environ['DISCORD_TOKEN']
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    global duels

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_reaction_add(reaction, user):
        emoji = reaction.emoji

        if user.bot:
            return

        if emoji == "✅":
            print(user, reaction, emoji)
            tournament.append((user.name, 'Ace', 'Sword'))
            return
        elif emoji == "⚔️":
            opponent = duels[reaction.message]
            print("duel? {} vs {}".format(user.name, opponent))

            print(reaction.message)
            sep = '#'
            opp = opponent.split(sep, 1)[0]

            embed = discord.Embed(title="{} has accepted {}'s duel request!".format(user.name, opp), description="")
            await reaction.message.channel.send(embed=embed)
            # fixed_channel = bot.get_channel(channel_id)
            # await fixed_channel.send(embed=embed)

            await reaction.message.delete()
            await duel.run_duel(user, opponent, reaction.message.channel)
        else:
            return

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(message)
        print(f"{username} said: '{user_message}' ({channel})")

        match user_message:
            case '/start':
                print(f'{username} has started the Lost Tournament!')
                # await message.channel.send(f'{username} has started the Lost Tournament!')
                embed = discord.Embed(title="{} has started the Lost Tournament!".format(username), description="")
                await message.channel.send(embed=embed)
                await lost_tournament.run_tourney(message, tournament)
            case '/create':
                print(f'{username} has created the Lost Tournament!')
                embed = discord.Embed(title="{} has created the Lost Tournament!".format(username), description="")
                embed.add_field(name="Click the ✅ below to enter!", value="")

                message = await message.channel.send(embed=embed)
                await message.add_reaction("✅")
            case '/duel':
                print(f'{username} has started a duel')
                embed = discord.Embed(title="{} has requested a duel!".format(username), description="Click ⚔️ to accept the challenge!")
                message = await message.channel.send(embed=embed)
                duels[message] = username
                await message.add_reaction("⚔️")
            case _:
                print('hit that default')

    client.run(TOKEN)
