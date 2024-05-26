import discord
import requests
from discord.ext import commands
from discord import app_commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
tree = client.tree


@client.event
async def on_ready():
    sync = await tree.sync()
    print(f"Bot Logged As {client.user}\nSynced {len(sync)} command(s)")


class Pagenation_System_View(discord.ui.View):
    def __init__(self,page:int,user_name,user_repos_json_data:dict,user_id):
        super().__init__(timeout=None)
        self.p = page
        self.r = user_repos_json_data
        self.n = user_name
        self.id = user_id

    def calc_perecentege(self,dictionary:dict) -> list:
        values_sum = sum(list(dictionary.values()))
        languages = [key for key,val in  dictionary.items()]
        
        values_with_precentege = []
        
        for i in range(len(languages)):
            values_with_precentege.append(f"{languages[i]} : {int((dictionary[languages[i]]/values_sum)*100)}%")
            
        return values_with_precentege




    async def return_to_first_page_func(self,interaction:discord.Interaction,embed:discord.Embed):
        user_repos_json_data = requests.get(f"https://api.github.com/users/{self.n}/repos").json()
        link = requests.get(f"https://api.github.com/users/{self.n}")
        json_link = link.json()
        bio = "Therse Is No Bio" if json_link["bio"] == None else json_link["bio"]
        user_id = json_link["id"]
        avatar_url = json_link["avatar_url"]
        followers = json_link["followers"]
        following = json_link["following"]
        public_repos = json_link["public_repos"]
        name = json_link["name"] if json_link["name"] != None else "There Is No Name"
        joined_at = str(json_link["created_at"]).split("T")[0]
        updated_at = str(json_link["updated_at"]).split("T")[0]
        embed.title = f"{name} Github Info"
        embed.description = f"> User Bio : {bio}\n> User Id : {user_id}\n> Followers : {followers}\n> Following : {following}\n> Public Repos : {public_repos}\n> Name : {name}\n> Joined at : {joined_at}\n> Updated At : {updated_at}"
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(
            text=f"Requested By : {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        await interaction.message.edit(embed=embed)
            
        return



    @discord.ui.button(label="<-",style=discord.ButtonStyle.blurple)
    async def _back(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.user.id != self.id:
            await interaction.response.send_message(f"You can't use this embed because it's controlled by <@{self.id}>",ephemeral=True)
            return

        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        self.p -= 1

        if self.p < 0:
            self.p = len(self.r)

        if self.p == 0:
            await self.return_to_first_page_func(interaction,embed)

        name = self.r[self.p - 1]["name"]
        url = self.r[self.p - 1]["svn_url"]
        created_at = str(self.r[self.p - 1]["created_at"]).split("T")[0]
        size = self.r[self.p - 1]["size"] / 1000
        language = self.r[self.p - 1]["language"]
        stars = self.r[self.p - 1]["stargazers_count"]

        my_data = self.calc_perecentege(requests.get(f"https://api.github.com/repos/{self.n}/{name}/languages").json())


        embed.description = f"Name : {name}\nRepo Url : {url}\nCreated At : {created_at}\nSize : {size}MB\nLanguage : {language}\nStars : {stars}\n" + "\n".join(my_data)
        embed.set_footer(text=f"Page : {self.p} / {len(self.r)}")

        await interaction.message.edit(embed=embed)

    @discord.ui.button(label="->",style=discord.ButtonStyle.blurple)
    async def _next(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.user.id != self.id:
            await interaction.response.send_message(f"You can't use this embed because it's controlled by <@{self.id}>",ephemeral=True)
            return
        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        self.p += 1

        if self.p > len(self.r):
            self.p = 0

        if self.p == 0:
            await self.return_to_first_page_func(interaction,embed)



        name = self.r[self.p - 1]["name"]
        url = self.r[self.p - 1]["svn_url"]
        created_at = str(self.r[self.p - 1]["created_at"]).split("T")[0]
        size = self.r[self.p - 1]["size"] / 1000
        language = self.r[self.p - 1]["language"]
        stars = self.r[self.p - 1]["stargazers_count"]
        my_data = self.calc_perecentege(requests.get(f"https://api.github.com/repos/{self.n}/{name}/languages").json())


        embed.description = f"Name : {name}\nRepo Url : {url}\nCreated At : {created_at}\nSize : {size}MB\nLanguage : {language}\nStars : {stars}\n" + "\n".join(my_data)
        embed.set_footer(text=f"Page : {self.p} / {len(self.r)}")

        await interaction.message.edit(embed=embed)








@tree.command(name="github_user_info", description="get github user info by his name")
@app_commands.describe(user_name="who is the user who you want to know its info")
async def _github_info(interaction: discord.Interaction, user_name: str) -> None:
    try:
        page = 0
        user_repos_json_data = requests.get(f"https://api.github.com/users/{user_name}/repos").json()
        link = requests.get(f"https://api.github.com/users/{user_name}")
        json_link = link.json()
        bio = "Therse Is No Bio" if json_link["bio"] == None else json_link["bio"]
        user_id = json_link["id"]
        avatar_url = json_link["avatar_url"]
        followers = json_link["followers"]
        following = json_link["following"]
        public_repos = json_link["public_repos"]
        name = json_link["name"] if json_link["name"] != None else "There Is No Name"
        joined_at = str(json_link["created_at"]).split("T")[0]
        updated_at = str(json_link["updated_at"]).split("T")[0]
        embed = discord.Embed(title=f"{user_name} Github Info", description=f"> User Bio : {bio}\n> User Id : {user_id}\n> Followers : {followers}\n> Following : {following}\n> Public Repos : {public_repos}\n> Name : {name}\n> Joined at : {joined_at}\n> Updated At : {updated_at}", color=discord.Colour.dark_gold())
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(
            text=f"Requested By : {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed,view=Pagenation_System_View(page,user_name,user_repos_json_data,interaction.user.id))



    except Exception as e:
        await interaction.response.send_message(f"Failled To Get This User Info", ephemeral=True)


client.run(
    "TOKEN")
