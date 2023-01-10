import discord
import os
os.system("pip install git+https://github.com/ItzYourHacker/discord.py")
os.system("pip install git+https://github.com/ItzYourHacker/jishaku")
os.system("pip install wavelink")
os.system("pip install asyncio")
os.system("pip install typing")
import wavelink
from discord.ext import commands
import asyncio
import typing
import jishaku

Hacker=[1033055689427406928]
async def get_prefix(bot, message):
    idk = discord.utils.get(message.guild.roles, id=1036338882335215616)
    if message.author.id in Hacker:
        return ["","."]
    elif idk in message.author.roles:
        return ["","."]
    else:
        return "."


token=""

OWNER_IDS= [1033055689427406928]

bot = commands.AutoShardedBot(command_prefix=get_prefix,intents=discord.Intents.all(),owner_ids=OWNER_IDS,case_insensitive=True,strip_after_prefix=True,replied_user=False,shard_count=1, sync_commands_debug= True, sync_commands=True)

import os
os.system("pip install jishaku")


async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot,host="lavalink.oops.wtf", port=443, password="www.freelavalink.ga", https=True)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(bot.guilds)} Guilds!'))
    print("Loaded & Online!")
    print(f"Logged in as: {bot.user}")
    print(f"Connected to: {len(bot.guilds)} guilds")
    print(f"Connected to: {len(bot.users)} users")
    bot.loop.create_task(node_connect())
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print (e)


@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")


@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client
    if vc.loop:
        return await vc.play(track)
    next_song = vc.queue.get()
    await vc.play(next_song)
    emb = discord.Embed(title="**Now Playing**",
                         description=f"\n{next_song.title}", color=0x00fffb)
    await ctx.send(embed=emb)


async def play_next(ctx):
    if not ctx.voice_client.is_playing():
        next_song = ctx.voice_client.queue.get()
        await ctx.voice_client.play(next_song)
        emb = discord.Embed(title="**Now Playing**",
                             description=f"\n{next_song.title}", color=0x00fffb)
        await ctx.send(embed=emb)
    else:
        await ctx.voice_client.stop()
        return ctx.send("Queue is empty")





  
@bot.hybrid_command(name="play",aliases=["p"])
async def play(ctx, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = discord.Embed(
            description=f"{ctx.author.mention}: No song(s) are playing.", color=0x00fffb)
        return await ctx.send(embed=embed)
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and vc.is_connected and vc._source is None:
        await vc.play(search)
        embe = discord.Embed(
            description=f"\n [{search.title}]({search.uri}) ", color=0x00fffb)
        embe.set_author(name=f"|  Now Playing", icon_url=f"{ctx.author.avatar}")
        embe.set_image(url=search.thumbnail)
        await ctx.send(embed=embe)
    else:
        print("Added to queue")
        await vc.queue.put_wait(search)
        emb = discord.Embed(
            description=f"\n [{search.title}]({search.uri}) **to the queue.**", color=0xF181FF)
        emb.set_author(name=f"|  Track queued", icon_url=f"{ctx.author.avatar}")
        emb.set_thumbnail(url=search.thumbnail)
	#emb.set_footer(name=f"Requested By {ctx.author.name}", icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=emb)
    vc.ctx = ctx
    setattr(vc, "loop", False)

@bot.hybrid_command(name="queue")
async def queue(ctx):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = discord.Embed(
            description=f"{ctx.author.mention}: No song(s) are playing.", color=0x00fffb)
        return await ctx.send(embed=embed)

    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
        emb = discord.Embed(
            description=f"**{ctx.author.mention}: The queue is empty. Try adding songs.**",color=0x00fffb)
        return await ctx.send(embed=emb)
    lp = discord.Embed(title="Queue",color=0xF181FF)
    queue = vc.queue.copy()
    song_count = 0
    for song in queue:
        song_count += 1
        lp.add_field(name=f"[{song_count}] Song", value=f"{song.title}")
        return await ctx.send(embed=lp)


@bot.hybrid_command(name="stop")
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.stop()
    await ctx.send("Stopped playing.")


@bot.hybrid_command(name="pause")
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.pause()
    await ctx.send("Paused the player.")


@bot.hybrid_command(name="resume", aliases=["unpause", "continue"])
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.resume()
    await ctx.send("Resumed the player.")


@bot.hybrid_command(name="skip", pass_context=True)
async def skip(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.pause()
    await play_next(ctx)
    await ctx.send("Skipped the song.")


@bot.hybrid_command(name="disconnect", aliases=["dc"])
async def disconnect(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.disconnect()
    await ctx.send("Disconnected from the voice channel.")

@bot.hybrid_command(name="seek")
async def seek(ctx: commands.Context, time: int):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.seek(time)
    await ctx.send(f"Seeked to {time} seconds.")

@bot.hybrid_command(name="connect",aliases=["j"])
async def join(ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
    if channel is None:
        channel = ctx.author.voice.channel
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)

    if player is not None:
        if player.is_connected():
            return await ctx.send("bot is already connected to a voice channel")
    await channel.connect(cls=wavelink.Player)
    mbed=discord.Embed(title=f"Connected to {channel.name}", color=0x00fffb)
    await ctx.send(embed=mbed)
  
  
async def main () :
    await bot.load_extension("jishaku")
    os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
    os.environ["JISHAKU_HIDE"] = "True"
    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
    await bot.start(token)


asyncio.run(main())
