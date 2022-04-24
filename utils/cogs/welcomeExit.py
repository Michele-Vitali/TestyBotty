from email import message
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from urllib.request import urlopen
import os
from io import BytesIO

import settings

class WelcomeExitImage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Welcome-Goodbye image cog loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #Ottengo il server dove il membro è appena joinato dall'ID
        guild = next((i for i in settings.servers if i['ID'] == member.guild.id), None)
        #Se il server ha un immagine di welcome settata allora la ottengo
        print(guild)  
        if guild['welcome_image']:
            #Faccio una richiesta http e ottengo la response
            response = requests.get(guild['welcome_image'])
            #Apro la response come dati binari e poi come immagine convertita infine in formato RGBA
            banner = Image.open(BytesIO(response.content)).convert('RGBA')
            #Controllo se il server ha un welcome message settato
            if guild['welcome_image_message']:
                image_message = guild['welcome_image_message']
            #Salvo il percorso file per dove salvare l'eventuale foto modificata del membro
            image_path = './utils/images/welcome/' / f'welcome_{member.name}.png'
        #Ottengo il canale dove mandare poi il messaggio di benvenuto
        channel = self.bot.get_channel(guild['welcome_channel'])
        #Ottengo il messaggio di welcome
        text_message = guild['welcome_text_message']
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Inserisci la personalizzazione dei vari parametri
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        await self.custom_image(self, member, banner, image_message, image_path, channel, text_message)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        #Ottengo i server dove il membero è appena joinato dall'ID
        guild = [i for i in settings.servers if (['ID']) == member.guild.id]
        #Se il server ha un immagine di addio settata allora la ottengo
        if guild['goobye_image']:
            #Faccio una richiesta http e ottengo la response
            response = requests.get(guild['goodbye_image'])
            #Apro la response come dati binari e poi come immagine convertita infine in formato RGBA
            banner = Image.open(BytesIO(response.content)).convert('RGBA')
            #Controllo se il server ha un goodbye message settato
            if guild['goodbye_image_message']:
                message = guild['goodbye_image_message']

            #Salvo il percorso file per dove salvare l'eventuale foto modificata del membro
            image_path = './utils/images/goodbye/' / f'goodbye_{member.name}.png'
        #Ottengo il canale dove mandare poi il messaggio di addio
        channel = self.bot.get_channel(guild['goodbye_channel'])
        #Ottengo il messaggio di addio
        text_message = guild['goodbye_text_message']
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Inserisci la personalizzazione dei vari parametri
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        await self.custom_image(self, member, banner, message, image_path, channel, text_message)

    async def custom_image(self, member, banner, image_message, image_path, channel, text_message):
        #Faccio la richiesta https al link dell'immagine dell'avatar del membro senza però scaricarla, 
        #la tengo in stream e la ottengo in modalità raw (tutti i caratteri vengono considerati)
        avatar_bytes = requests.get(member.avatar_url, stream = True).raw
        #Apro l'immagine in formato RGB
        avatar = Image.open(avatar_bytes).convert('RGB')
        #Creo una nuova immagine in modalità "L" (8 bit per pixel, bianco e nero) di grandezza dell'avatar,
        # con colore 0 (ovvero nero)
        alpha = Image.new('L', avatar.size, 0)
        #Creo l'oggetto per poter disegnare nell'immagine
        draw = ImageDraw.Draw(alpha)
        #Disegno un ellisse di color bianco nel "box" che parte da X0 = 0 e Y0 = 0 fino a 
        #X1 = avatar.size.x e Y1 = avatar.size.y (larghezza e altezza dell'avatar)
        draw.ellipse([(0, 0), avatar.size], fill = 255)
        #Aggiungo lo strato alpha (alpha) all'avatar
        avatar.putalpha(alpha)
        #Resizoe l'avatar a 400x400 pixel
        avatar.resize((400, 400))
        #Creo un immagine im modalità "RGBA" (4x8 bit per ogni pixel, true-color con trasparenza) di grandezza
        #del banner di colore 0 (nero) 
        overlay = Image.new("RGBA", banner.size, 0)
        #Divido la tuple banner.size in W (larghezza) e H (altezza) per comodità
        W, H = banner.size
        #Incollo l'overlay sopra l'avatar in posizione (W/2)-200 e 100
        overlay.paste(avatar, (int(W/2) - 200, 100))
        #Metto lo strato alfa di overlayt sopra quello di banner
        banner.alpha_composite(overlay)
        #Divido il messaggio in una lista in base alle linee
        lines = message.splitlines()
        #Salvo l'url della repo su github del font utilizzato per scrivere nella foto
        truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true'
        #Creo l'oggetto per poter disegnare sull'immagine banner
        draw = ImageDraw.Draw(banner)
        #Inizializzo l'altezza dove si inizierà a scrivere sull'immagine
        y_text = 500
        #Setto la grandezza del font con cui scrivo
        font_size = 110

        for line in lines:
            #Ottengo il font con la grandezza deisderata
            font = ImageFont.truetype(urlopen(truetype_url), size = font_size)
            #Ottengo la larghezza e altezza in pixel del testo (linea)
            #width, height = font.getsize(line)
            #Scrivo il testo sulla foto in modo che sia centrato, con il font scelto e di colore nero
            draw.text(((W - width) / 2, y_text), line, font = font, fill = (0, 0, 0))
            #Abbasso la prossima scritta nella foto
            y_text += 100
            #Diminuisco la grandezza del font
            font_size -= 10

        #Riconverto banne rin formato RGB e salvo l'immagine al percorso file specificato
        banner.convert("RGB".save(image_path))
        #Mando l'immagine personalizzata nel canale
        await channel.send(file = discord.File(f"{image_path}"))
        #Mando il messaggio personalizzato nel canale
        await channel.send(text_message)

        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print("There's no image to delete at that file path")

def setup(bot):
    bot.add_cog(WelcomeExitImage(bot))