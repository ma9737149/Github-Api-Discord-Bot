import discord
import aiohttp
import asyncio
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from view.github_view import Pagenation_System_View

class Bot(commands.Bot):
    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()

    async def close(self) -> None:
        await self.session.close()
        await super().close()

client = Bot(command_prefix="!", intents=discord.Intents.all())

tree = client.tree

load_dotenv()


@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"Bot Logged As {client.user}\nSynced {len(synced)} guild command(s)")

class APIRateLimitError(Exception):
    pass


async def fetch_data(session :  aiohttp.ClientSession ,url : str):
    async with session.get(url) as response:
        return await response.json()

@tree.command(name="github_user_info", description="get github user info by his name")
@app_commands.describe(user_name="who is the user who you want to know its info")
async def _github_info(interaction: discord.Interaction, user_name: str) -> None:
    try:
        page = 0

        url1 = f"https://api.github.com/users/{user_name}/repos"
        url2 = f"https://api.github.com/users/{user_name}"

        user_repos_json_data , get_user_data = await asyncio.gather(fetch_data(interaction.client.session , url1),
                                                                    fetch_data(interaction.client.session , url2))


        if not get_user_data.get("message", None) is None and "API rate limit" in get_user_data.get("message"):
            raise APIRateLimitError("API rate limit exceeded. Please try again later.")


        bio = get_user_data.get("bio" , "Therse Is No Bio")
        user_id = get_user_data["id"]
        avatar_url = get_user_data["avatar_url"]

        followers = get_user_data["followers"]
        following = get_user_data["following"]

        public_repos = get_user_data["public_repos"]
        name = get_user_data.get("name" , "There Is No Name")
        joined_at = str(get_user_data["created_at"]).split("T")[0]
        updated_at = str(get_user_data["updated_at"]).split("T")[0]

        embed = discord.Embed(title=f"{user_name} Github Info", description=f"> User Bio : {bio}\n> User Id : {user_id}\n> Followers : {followers}\n> Following : {following}\n> Public Repos : {public_repos}\n> Name : {name}\n> Joined at : {joined_at}\n> Updated At : {updated_at}", color=discord.Colour.dark_gold())
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(
            text=f"Requested By : {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url
        )

        view = Pagenation_System_View(page,user_name,user_repos_json_data,interaction.user.id , interaction.client.session) if int(public_repos) != 0 else None
        await interaction.response.send_message(embed=embed,view=view)



    except APIRateLimitError as error:
        await interaction.response.send_message(error, ephemeral=True)

    except KeyError as error:
        await interaction.response.send_message("user not found" , ephemeral=True)

    except Exception as e:
        print(e)
        return


client.run(os.getenv("TOKEN"))
