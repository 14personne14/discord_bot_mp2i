import discord

SLASH_COMMANDS_GUILDS = [
    discord.Object(id=694582273005322241),
    discord.Object(id=1122178069524905995),
]

SEPARATOR = '----------------------------------------------------------'

MESSAGE = {
    "no_perm": "❌ Vous n'avez pas les permissions necessaires pour réaliser cette commande !", 
    "error_valeur": "❌ Vous avez rentré de mauvaises valeurs !\n\n__Rappel:__ Vous ne pouvez pas dépasser 28 jours de mute !",
    "mute_yourself": "❌ Vous ne pouvez pas vous mute vous-même !",
    "mute_bot": "❌ Vous ne pouvez pas mute un bot !", 
    "mute_admin": "Vous ne pouvez pas mute un administrateur du serveur ! \n\nJustement...\nCette tentative de mute pourrait te causer beaucoup ennuis !!!",
    "mute_over_limit": "❌ Vous ne pouvez pas mute une personne plus de 28 jours !", 
    "mute_valid": "### ✅ <@{id_member}> viens d'etre mute \n\n- **Durée:** \n`{jours} jour(s)` \n`{heures} heure(s)` \n`{minutes} minute(s)` \n`{secondes} seconde(s)`\n- **Raison:** \n`{reason}`",
    "unmute_valid": "### ✅ <@{id_member}> a bien été unmute \n\n- **Raison:** `{reason}`", 
}

ADMIN_ROLE = 1122178212504547481
MODERATOR_ROLE = 1122214808343822406

COLORS = {
    "red": discord.Colour.from_rgb(255, 0, 0),
    "green": discord.Colour.from_rgb(0, 255, 0),
    "blue": discord.Colour.from_rgb(0, 0, 255),
    "yellow": discord.Colour.from_rgb(255, 255, 0),
    "sky blue": discord.Colour.from_rgb(0, 255, 255),
    "violet": discord.Colour.from_rgb(255, 0, 255),
    "black": discord.Colour.from_rgb(0, 0, 0),
    "white": discord.Colour.from_rgb(255, 255, 255),
    "gray": discord.Colour.from_rgb(128, 128, 128)
}
