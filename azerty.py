# Import for '.env' 
import os
from dotenv import load_dotenv 

# Import for discord.py
import discord
from typing import Optional
from datetime import timedelta
from discord.ui import Button, Select, View
from discord import app_commands

# Import for other thing
import asyncio
import re

# My import 
from utils.config import *
from utils.fonctions import *

# Load '.env' file 
load_dotenv('.env') 

# Setup the bot 
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for GUILD in SLASH_COMMANDS_GUILDS:
            self.tree.copy_global_to(guild=GUILD)
            await self.tree.sync(guild=GUILD)

# Create Client
intents = discord.Intents.all()
client = MyClient(intents=intents)

# ======================================================================================= #
# When the bot is ready 
@client.event
async def on_ready():
    print(SEPARATOR + f'\nName : {client.user} \nId : {client.user.id}\n' + SEPARATOR)

# ======================================================================================= #
# When the bot intercept a message 
@client.event
async def on_message(message: discord.Message):
    # Anti bot
    if message.author.bot == True:
        return

    # React coucou
    if " coucou " in (' ' + message.content.lower() + ' '):
        print('Reaction coucou')
        await message.add_reaction("👋")
        print(SEPARATOR)

# ======================================================================================= #
@client.tree.command()
@app_commands.describe(texte='Texte à envoyer.')
async def message(interaction: discord.Interaction, texte: str):
    """Envoyer un message dans le salon actuel."""
    print(f'| Send message ("{texte}")')

    await interaction.response.send_message(texte)

    print(SEPARATOR)

######### ======================================================================================= #########
######### ======================================================================================= #########


@client.tree.command(name='mute', description='Mute un membre sur le serveur pendant un certaint temps.')
@app_commands.rename(member='membre')
@app_commands.describe(member='Membre à mute.')
@app_commands.rename(reason='raison')
@app_commands.describe(reason='Pourquoi ce membre va être mute ?')
@app_commands.describe(jours='Combien de jours ?')
@app_commands.describe(heures='Combien de heures ?')
@app_commands.describe(minutes='Combien de minutes ?')
@app_commands.describe(secondes='Combien de secondes ?')
#@app_commands.checks.bot_has_permissions(mute_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "Aucune raison n'a été donnée.", jours: Optional[int] = 0, heures: Optional[int] = 0, minutes: Optional[int] = 0, secondes: Optional[int] = 0):
    print(f'Try to mute {member.name}')

    # Default 1 minute of mute 
    if (jours == 0) and (heures == 0) and (minutes == 0) and (secondes == 0):
        minutes = 1
        
    # Not Admin or Modo 
    if not((interaction.user.get_role(ADMIN_ROLE) != None) or (interaction.user.get_role(MODERATOR_ROLE) != None)):
        embed = create_embed(
            couleur="red", 
            description=MESSAGE['no_perm']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    # Wrong value 
    elif not (jours <= 27 and heures <= 24 and minutes <= 60 and secondes <= 60 and jours >= 0 and heures >= 0 and minutes >= 0 and secondes >= 0):
        embed = create_embed(
            couleur="red", 
            description=MESSAGE['error_valeur']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    # Mute yourself
    elif interaction.user.id == member.id:
        embed = create_embed(
            couleur="red", 
            description=MESSAGE['mute_yourself']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    # Mute a bot
    elif member.bot:
        embed = create_embed(
            couleur="red", 
            description=MESSAGE['mute_bot']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Mute admin 
    elif member.guild_permissions.administrator:
        embed = create_embed(
            couleur="red", 
            description=MESSAGE['mute_admin']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    else: 
        # Calculate duration of mute  
        duree = timedelta(
            days=jours, 
            hours=heures,
            minutes=minutes, 
            seconds=secondes
        )
        
        # Mute over limit (28 days)
        if duree >= timedelta(days=28):
            embed = create_embed(
                couleur="red", 
                description=MESSAGE['mute_over_limit']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        # Mute the people 
        else:
            embed = create_embed(
                couleur="green", 
                description=MESSAGE['mute_valid'],
                footer_texte=interaction.user.display_name, 
                footer_icon_url=interaction.user.avatar.url
            )
            embed_format_description(embed, {
                "id_member": member.id, 
                "jours": jours, 
                "heures": heures, 
                "minutes": minutes, 
                "secondes": secondes, 
                "reason": reason, 
            })
            await member.timeout(duree, reason=reason)
            await interaction.response.send_message(embed=embed)
            print(f"Mute {member.name} \nDuartion: {jours} jour(s) / {heures} heure(s) / {minutes} minute(s) / {secondes} seconde(s).\nRaison: '{reason}'")
        
    print(SEPARATOR)

######### ======================================================================================= #########
######### ======================================================================================= #########


@client.tree.command(name="unmute", description="Supprime le mute d'un membre")
@app_commands.rename(member='membre')
@app_commands.describe(member='Membre à unmute.')
@app_commands.rename(reason='raison')
@app_commands.describe(reason='Pourquoi faut-il unmute ce membre?')
@app_commands.checks.bot_has_permissions(mute_members=True)
async def unmute(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "Aucune raison n'a été donnée."):
    print(f'Unmute {member.name}')

    # Not Admin or Modo 
    if not((interaction.user.get_role(ADMIN_ROLE) != None) or (interaction.user.get_role(MODERATOR_ROLE) != None)):
        embed = create_embed(
            couleur="red", 
            description=MESSAGE['no_perm']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    else: 
        await member.timeout(None)
        embed = create_embed(
            couleur="green", 
            description=MESSAGE['unmute_valid'],
            footer_texte=interaction.user.display_name, 
            footer_icon_url=interaction.user.avatar.url
        )
        embed_format_description(embed, {
            "id_member": member.id, 
            "reason": reason, 
        })
        await interaction.response.send_message(embed=embed)

    print(SEPARATOR)


######### ======================================================================================= #########
######### ======================================================================================= #########


@client.tree.command(name="ping", description="Ping le bot.")
async def ping(interaction: discord.Interaction):
    print(f'| Ping ({interaction.user.name})')

    embed = create_embed(
        couleur="green", 
        description="🏓 Pong !"
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

    print(SEPARATOR)


######### ======================================================================================= #########
######### ======================================================================================= #########


@client.tree.error
async def on_error(interaction: discord.Interaction, error):
    print("| Erreur: ", error)
    embed = create_embed(
        couleur="rouge", description=f"❌ **Une erreur inattendue est survenue !**\n```{error}``` \nVous ne devriez jammais recevoir une erreur comme celle-ci. \nVeuillez en faire part à <@689064395501994018>. ")
    if interaction.response.is_done() == False:
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.channel.send(embed=embed)

######### ======================================================================================= #########
######### ======================================================================================= #########

# Run bot
client.run(os.getenv('TOKEN'))
