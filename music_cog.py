import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download = False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
       
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name = "play", help = "Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        global voice_channel
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            global song
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send(f"{song['title']} added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()
    
    @commands.command(name = "remove", help = "removes most recently added song from queue")
    async def remove(self, ctx):
        await ctx.send(f"{song['title']} removed from queue")
        self.music_queue.pop([song, voice_channel])

    @commands.command(name = "clear", help = "removes everything from the queue")
    async def remove_all(self, ctx):
        await ctx.send("Queue cleared")
        self.music_queue.clear()

    @commands.command(name = "pause", help = "Pauses the current song thats playing")
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("paused")

    @commands.command(name = "resume", help = "Resumes the current song that was paused")
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("resumed")
    
    @commands.command(name = "stop", help = "Stops the current song")
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("stopped")

    @commands.command(name = "queue", help = "Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            if (x for x in self.music_queue if self.music_queue.count(x) > 1):
                await ctx.send(retval[0:len(self.music_queue[i][0]['title'])] + " (looped 10 times)")
            else:
                await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name = "skip", help = "Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()
    
    @commands.command(name = "loop", help = "Loops the current song")
    async def loop(self, ctx):
        count = 0
        while count < 10:
            count += 1
            self.music_queue.append([song, voice_channel])
        
        loop_message = await ctx.send("looped")
        await loop_message.add_reaction("✅")
