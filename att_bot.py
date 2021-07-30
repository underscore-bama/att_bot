import asyncpraw
import discord
from discord import Embed
from discord.colour import Color

client = discord.Client()

@client.event
async def on_ready():
    print('discord on')

    #settings   
    reddit = asyncpraw.Reddit(
        client_id = " ",
        client_secret = " ",
        password = " ",
        user_agent = " ",
        username = " ",
    )
    sub = 'att' # subreddit set
    discord_channel_id = 000000000000000000 # set to the channel id for script output
    discordCap = 1800 # arbitrary discord character cutoff; errors will be raised if
                      # character count if over 1900 as discord has a maximum char-
                      # acter count ouf 2048 per embed. lengthy comment/submission
                      # bodies in modlog will be removed from the embedd

    channel = client.get_channel(discord_channel_id)
    subreddit = await reddit.subreddit(sub)
    print('reddit on')
    async def modqueue():
        async for submission in subreddit.mod.stream.modqueue():
            if hasattr(submission, 'crosspost_parent'): # is xpost
                embeded = discord.Embed(
                    title = 'removed xpost submission',
                    color = Color.red(),
                    description = '\n'.join(
                        [
                            f'[link to submission](https://reddit.com/{submission.permalink}',
                            f'**by:** `{submission.author}`',
                            f'**title:** `{submission.title}`',
                            f'**from:** `{submission.domain}`'
                        ]
                    )
                )
                await channel.send(embed = embeded)
            else: # removed submission
                if submission.num_reports == 0:
                    if hasattr(submission, 'title'): 
                        if len(submission.selftext) <= discordCap:
                            embeded = discord.Embed(
                                title = 'removed submission',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to submission](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'**title:** `{submission.title}`',
                                        f'**content:**',
                                        f'>>> {submission.selftext}'
                                    ]
                                )
                            )
                            await channel.send(embed = embeded)
                        else:
                            embeded = discord.Embed(
                                title = 'removed submission',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to submission](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'**title:** `{submission.title}`',
                                        f'_notice: lengthy post: exceeds discord character count_'
                                    ]
                                )
                            )
                    else: #removed comment
                        if len(submission.body) <= discordCap:
                            embeded = discord.Embed(
                                title = 'removed comment',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to comment](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'**content:**',
                                        f'>>> {submission.body}'
                                    ]
                                )
                            )
                            await channel.send(embed = embeded)
                        else:
                            embeded = discord.Embed(
                                title = 'removed comment',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to comment](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'_notice: lengthy comment: exceeds discord character count_'
                                    ]
                                )
                            )
                            await channel.send(embed = embeded)
                else: #submission reported
                    if hasattr(submission, 'title'):
                        if len(submission.selftext) <= discordCap:
                            reports = submission.user_reports
                            for i in reports:
                                userReport = i[0]
                            embeded = discord.Embed(
                                title = 'submission reported!',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to item](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'**reason:** `{userReport}`',
                                        f'**content:**',
                                        f'>>> {submission.selftext}'
                                    ]
                                )
                            )
                            await channel.send(embed = embeded)

                        else:
                            reports = submission.user_reports
                            for i in reports:
                                userReport = i[0]
                            embeded = discord.Embed(
                                title = 'submission reported!',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to item](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'**reason:** `{userReport}`',
                                        f'_notice: lengthy submission: exceeds discord character count._'
                                    ]
                                )
                            )
                            await channel.send(embed = embeded)
                    else: #comment reported
                        if len(submission.body) <= discordCap:
                            reports = submission.user_reports
                            for i in reports:
                                userReport = i[0]
                            embeded = discord.Embed(
                                title = 'comment reported!',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to item](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'**reason:** `{userReport}`',
                                        f'**content:**',
                                        f'>>> {submission.body}'
                                    ]
                                )
                            )
                            await channel.send(embed = embeded)
                        else:
                            reports = submission.user_reports
                            for i in reports:
                                userReport = i[0]
                            embeded = discord.Embed(
                                title = 'comment reported!',
                                color = Color.red(),
                                description = '\n'.join(
                                    [
                                        f'[link to item](https://reddit.com/{submission.permalink})',
                                        f'**by:** `{submission.author}`',
                                        f'**reason:** `{userReport}`',
                                        f'_notice: lengthy comment: exceeds discord character count._'
                                    ]
                                )
                            )
                            await channel.send(embed = embeded)

    async def modmail():
        async for message in subreddit.modmail.conversations(state='inbox'):
            if message.last_mod_update == None:
                embeded = discord.Embed(
                    title = 'new modmail recieved',
                    color = Color.red(),
                    description = '\n'.join(
                        [
                            f'[link to mail](https://mod.reddit.com/mail/all/{message.id})',
                            f'**from:** `{message.participant}`',
                            f'**subject:** `{message.subject}`',

                        ]
                    )
                )
                await channel.send(embed = embeded)
            else:
                embeded = discord.Embed(
                    title = 'modmail response recieved',
                    color = Color.red(),
                    description = '\n'.join(
                        [
                            f'[link to mail](https://mod.reddit.com/mail/all/{message.id})',
                            f'**from:** `{message.participant}`',
                            f'**subject:** `{message.subject}`',

                        ]
                    )
                )
                await channel.send(embed = embeded)

    await modmail()
    await modqueue()
    
client.run('token')