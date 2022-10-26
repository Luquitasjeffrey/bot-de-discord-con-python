import discord
from discord.ext import commands

class process:

    class mensaje_mas_popular():
        freq : int
        data : str
        def __init__(self):
            self.freq=0
            self.data=''

        def alter(self, fr: int, msg: str):
            if(self.freq<fr):
                self.data=msg
                self.freq=fr
            return self
        
    def listmsg(arr, arrsize:int):
        arr.sort()
        coincidences=process.mensaje_mas_popular()
        count=1
        for i in range(1, arrsize-1, 1):
            if(arr[i]==arr[i-1]):
                count+=1
                continue
            coincidences=process.mensaje_mas_popular.alter(coincidences, count, arr[i-1])
            count=1
        coincidences=process.mensaje_mas_popular.alter(coincidences, count+1, arr[arrsize-1])
        return coincidences
        
TOKEN=str(input('copia y pega aca el token de tu bot: '))
intents=discord.Intents.default()
intents.message_content=True
bot=discord.Client(intents=intents)
@bot.event
async def on_ready():
    print('entramos como {0.user}'.format(bot))

@bot.event
async def on_message(message):
    username=str(message.author)
    msg=str(message.content)
    chat=str(message.channel.name)
    print(f'"{username}/{chat}": {msg}')
    if message.author==bot.user:
        return

    if msg.lower()=='~$ recopilar estadisticas/c':
        canal=discord.utils.get(bot.get_all_channels(), name=chat)
        id=int(canal.id)
        history=bot.get_channel(id)
        arr=[]
        msgcount=0
        async for i in history.history(limit=None):
            if(str(i.content).startswith('https:')):
                arr.append(str(i.content))
                msgcount+=1
        
        if(msgcount==0):
            await canal.send('no fue enviada ninguna cancion \n')
            return

        resultado=process.listmsg(arr, msgcount)
        print(f'{resultado.data} (freq={resultado.freq})')
        await canal.send(str(f'la cancion mas popular fue: "{resultado.data}" con una aparicion de {resultado.freq} veces en el chat con una prevalencia del {100*(resultado.freq/msgcount)}% de los mensajes enviados'))
    
    if msg.lower()=='~$ recopilar estadisticas/msg':
        canal=discord.utils.get(bot.get_all_channels(), name=chat)
        id=int(canal.id)
        history=bot.get_channel(id)
        arr=[]
        msgcount=0
        async for i in history.history(limit=None):           
            arr.append(str(i.content))
            msgcount+=1

        resultado=process.listmsg(arr, msgcount)
        print(f'{resultado.data} (freq={resultado.freq})')
        await canal.send(str(f'el mensaje mas popular fue: "{resultado.data}" con una aparicion de {resultado.freq} veces en el chat con una prevalencia del {100*(resultado.freq/msgcount)}% de los mensajes enviados'))
    

    if msg.lower()=='~$ recopilar estadisticas/a':
        canal=discord.utils.get(bot.get_all_channels(), name=chat)
        id=int(canal.id)
        history=bot.get_channel(id)
        arr=[]
        msgcount=0
        async for i in history.history(limit=None):
            arr.append(str(i.author))
            msgcount+=1

        resultado=process.listmsg(arr, msgcount)
        print(f'{resultado.data} (freq={resultado.freq})')
        await canal.send(str(f'el que mando mas mensajes fue "{resultado.data}" con una aparicion de {resultado.freq} veces en el chat con una prevalencia del {100*(resultado.freq/msgcount)}% de los mensajes enviados'))
    


    if msg.lower()=='exit pybot':
        canal=discord.utils.get(bot.get_all_channels(), name=chat)
        await canal.send('bueno me voy vieja')
        exit()

bot.run(TOKEN)
