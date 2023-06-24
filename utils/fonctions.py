# Import 
import discord
from .config import COLORS
from typing import Optional, Union
from discord.app_commands.errors import *


def embed_format_description(embed: discord.Embed, dictionary: dict) -> discord.Embed:
    """Formatter la description d'un embed en actualisant son contenu."""
    
    embed.description = embed.description.format(**dictionary)
    return embed


def create_embed(*, couleur=None, 
                    titre=None, 
                    url=None, 
                    description=None, 
                    time=None, 
                    auteur_name=None, 
                    auteur_image_url=None, 
                    footer_texte=None, 
                    footer_icon_url=None, 
                    image_url=None) -> discord.Embed:
    """Création d'un embed pour discord."""
    
    embed = discord.Embed(colour=COLORS[couleur], title=titre, url=url, description=description, timestamp=time)
    
    if auteur_name: 
        embed.set_author(name=auteur_name, icon_url=auteur_image_url)
    if footer_texte:
        embed.set_footer(text=footer_texte, icon_url=footer_icon_url)
    if image_url:
        embed.set_image(url=image_url)

    return embed
