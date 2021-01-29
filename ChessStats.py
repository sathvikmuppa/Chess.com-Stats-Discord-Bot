import discord
from discord.ext import commands
from getStats import Stats
from selenium import webdriver
from info import token


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        usersFile = f'{message.guild} users.txt'
        try:
            f = open(usersFile, 'r')
            f.close()
        except Exception:
            f = open(usersFile, 'x')
            f.close()

        if message.author.id == self.user.id:
            return

        if message.content.startswith('$help'):
            embed = discord.Embed(title="Chess.com Stats Help",
                                  description="A list of commands for this bot")
            embed.add_field(
                name="$help", value="Displays all of the commands for this bot", inline=False)
            embed.add_field(
                name="$addUser@user", value="adds the user to the server's user list (@user = @chess.com username)", inline=False)
            embed.add_field(
                name="$removeUser@user", value="removes the user from the server's user list (@user = @chess.com username)", inline=False)
            embed.add_field(
                name="$clearUsers", value="clears the server's user list", inline=False)
            embed.add_field(
                name="$getScore@user", value="gets the stats for the user (@user = @chess.com user name)", inline=False)
            embed.add_field(
                name="$getAllScores", value="gets the stats for all users in the server's user list", inline=False)
            await message.channel.send(embed=embed)

        elif message.content.startswith('$addUser'):
            if len(message.content) > 9:
                user = message.content[9:]
                f = open(usersFile, 'r')
                add = False
                for line in f:
                    if user in line:
                        await message.channel.send(f'{user} is already added')
                        add = True
                f.close()
                if add == False:
                    f = open(usersFile, 'a')
                    f.write(f'{user}\n')
                    f.close()
                    await message.channel.send(f'Added user {user}')
            else:
                await message.channel.send('Please specify a user')

        elif message.content.startswith('$removeUser'):
            if len(message.content) > 12:
                user = message.content[12:]
                f = open(usersFile, 'r')
                users = []
                exists = False
                for line in f:
                    if user in line:
                        line = line.replace(line, '')
                        exists = True
                    users.append(line)
                f.close()
                if exists:
                    f = open(usersFile, 'w')
                    for line in users:
                        f.write(line)
                    f.close()
                    await message.channel.send(f'Removed user {user}')
                else:
                    await message.channel.send(f'That user has not been added')
            else:
                await message.channel.send('Please specify a user')

        elif message.content.startswith('$clearUsers'):
            f = open(usersFile, 'w')
            f.write('')
            f.close()
            await message.channel.send('Cleared all users')

        elif message.content.startswith('$getScore'):
            m = await message.channel.send('Loading...Give me a second :)')
            if len(message.content) > 10:
                stats = Stats()
                user = message.content[10:]
                if stats.checkExistence(user):
                    score = stats.getScore(user)
                    if score == 1:
                        await m.edit(content="User is unrated")
                    else:
                        await m.edit(content=f"{user}: {score[0]}  {score[1]}/{score[2]}/{score[3]}")
                else:
                    await m.edit(content="User doesn't exist!")
            else:
                await m.edit(content="Please specify a user")

        elif message.content.startswith('$getAllScores'):
            m = await message.channel.send('Loading... This may take a while...')
            stats = Stats()
            embed = discord.Embed(title=f"{message.guild} Rapid Statistics")
            getAllStats = stats.getAllStats(message.guild)
            for index, stat in enumerate(getAllStats[1]):
                embed.add_field(
                    name=getAllStats[0][index], value=stat, inline=False)
            await message.channel.send(embed=embed)


client = MyClient()
client.run(token)
