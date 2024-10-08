import discord
import requests
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from view.github_view import Pagenation_System_View


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
tree = client.tree

load_dotenv()

@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"Bot Logged As {client.user}\nSynced {len(synced)} guild command(s)")

class APIRateLimitError(Exception):
    pass


@tree.command(name="github_user_info", description="get github user info by his name")
@app_commands.describe(user_name="who is the user who you want to know its info")
async def _github_info(interaction: discord.Interaction, user_name: str) -> None:
    try:
        page = 0
        user_repos_json_data = requests.get(f"https://api.github.com/users/{user_name}/repos").json()
        link = requests.get(f"https://api.github.com/users/{user_name}")
        json_link = link.json()

        if not json_link.get("message", None) is None and "API rate limit" in json_link.get("message"):
            raise APIRateLimitError("API rate limit exceeded. Please try again later.")


        bio = json_link.get("bio" , "Therse Is No Bio")
        user_id = json_link["id"]
        avatar_url = json_link["avatar_url"]

        followers = json_link["followers"]
        following = json_link["following"]

        public_repos = json_link["public_repos"]
        name = json_link.get("name" , "There Is No Name")
        joined_at = str(json_link["created_at"]).split("T")[0]
        updated_at = str(json_link["updated_at"]).split("T")[0]

        embed = discord.Embed(title=f"{user_name} Github Info", description=f"> User Bio : {bio}\n> User Id : {user_id}\n> Followers : {followers}\n> Following : {following}\n> Public Repos : {public_repos}\n> Name : {name}\n> Joined at : {joined_at}\n> Updated At : {updated_at}", color=discord.Colour.dark_gold())
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(
            text=f"Requested By : {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url
        )
        
        view = Pagenation_System_View(page,user_name,user_repos_json_data,interaction.user.id) if int(public_repos) != 0 else None
        await interaction.response.send_message(embed=embed,view=view)



    except APIRateLimitError as error:
        await interaction.response.send_message(error, ephemeral=True)

    except KeyError as error:
        await interaction.response.send_message("user not found" , ephemeral=True)

    except :
        return


client.run(os.getenv("TOKEN"))
