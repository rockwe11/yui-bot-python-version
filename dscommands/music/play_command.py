import asyncio

import discord
import wavelink
from discord.ext import commands
import youtube_dl
from dscommands.command_context import CommandContext
from dscommands.music.player import Player

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class PlayCommand:

    async def handle(self, ctx: CommandContext):
        if len(ctx.get_args()) == 0:
            await ctx.send_message("Введите название трека")
            return
        search = await wavelink.YouTubeTrack.search(query=" ".join(ctx.get_args()), return_first=True)
        vc = ctx.get_message().guild.voice_client
        if not vc:
            player = Player()
            voice = ctx.get_message().author.voice
            if not voice:
                await ctx.send_message("Вы не подключены к голосовому каналу")
                return
            vc: Player = await voice.channel.connect(cls=player)
        if vc.is_playing():
            vc.queue.put(item=search)
            await ctx.send_message("", embed=discord.Embed(
                title=search.title,
                url=search.uri,
                description=f"Queued {search.title} in {vc.channel}"))
        else:
            await vc.play(search)

            await ctx.send_message("", embed=discord.Embed(
                title=search.title,
                url=search.uri,
                description=f"Queued {search.title} in {vc.channel}"))

        # filename = await YTDLSource.from_url(ctx.get_args()[0], loop=ctx.client.loop)
        # voice_channel.play(discord.FFmpegPCMAudio(executable='', source=filename))
        # await ctx.send_message(f'Сейчас играет: {filename}')

    def getName(self):
        return "play"

    def get_help(self):
        return "Музыкальный плеер.\n\n" \
               "Использование: {prefix}play [ссылка на клип YouTube/название трека]"


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
