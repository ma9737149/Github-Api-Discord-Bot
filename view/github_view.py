import discord
import requests

class Pagenation_System_View(discord.ui.View):
    def __init__(self,page:int,user_name,user_repos_json_data:dict,user_id):
        super().__init__(timeout=None)
        self.page = page
        self.repos = user_repos_json_data
        self.name = user_name
        self.id = user_id

    def calc_perecentege(self,dictionary:dict) -> list:
        values_sum = sum(list(dictionary.values()))
        languages = [key for key,val in dictionary.items()]
        
        values_with_precentege = []
        
        for i in range(len(languages)):
            values_with_precentege.append(f"{languages[i]} : {int((dictionary[languages[i]]/values_sum)*100)}%")
            
        return values_with_precentege




    async def return_to_first_page_func(self,interaction:discord.Interaction,embed:discord.Embed) -> None:
        user_repos_json_data = requests.get(f"https://api.github.com/users/{self.name}/repos").json()
        link = requests.get(f"https://api.github.com/users/{self.name}")
        json_link = link.json()

        bio = json_link.get("bio" , "Therse Is No Bio")
        user_id = json_link["id"]
        avatar_url = json_link["avatar_url"]

        followers = json_link["followers"]
        following = json_link["following"]
        public_repos = json_link["public_repos"]
        name = json_link.get("name" , "There Is No Name")
        joined_at = str(json_link["created_at"]).split("T")[0]
        updated_at = str(json_link["updated_at"]).split("T")[0]

        embed.title = f"{name} Github Info"
        embed.description = f"> User Bio : {bio}\n> User Id : {user_id}\n> Followers : {followers}\n> Following : {following}\n> Public Repos : {public_repos}\n> Name : {name}\n> Joined at : {joined_at}\n> Updated At : {updated_at}"
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(
            text=f"Requested By : {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await interaction.message.edit(embed=embed)




    @discord.ui.button(label="<-",style=discord.ButtonStyle.blurple)
    async def _back(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.user.id != self.id:
            await interaction.response.send_message(f"You can't use this embed because it's controlled by <@{self.id}>",ephemeral=True)
            return

        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        self.page -= 1

        if self.page < 0:
            self.page = len(self.repos)

        elif self.page == 0:
            await self.return_to_first_page_func(interaction,embed)
            return


        name = self.repos[self.page - 1]["name"]
        url = self.repos[self.page - 1]["svn_url"]
        created_at = str(self.repos[self.page - 1]["created_at"]).split("T")[0]
        size = self.repos[self.page - 1]["size"] / 1000
        language = self.repos[self.page - 1]["language"]
        stars = self.repos[self.page - 1]["stargazers_count"]

        my_data = self.calc_perecentege(requests.get(f"https://api.github.com/repos/{self.name}/{name}/languages").json())


        embed.description = f"Name : {name}\nRepo Url : {url}\nCreated At : {created_at}\nSize : {size}MB\nLanguage : {language}\nStars : {stars}\n" + "\n".join(my_data)
        embed.set_footer(text=f"Page : {self.page} / {len(self.repos)}")

        await interaction.message.edit(embed=embed)

    @discord.ui.button(label="->",style=discord.ButtonStyle.blurple)
    async def _next(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.user.id != self.id:
            await interaction.response.send_message(f"You can't use this embed because it's controlled by <@{self.id}>",ephemeral=True)
            return

        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        self.page += 1

        if self.page > len(self.repos):
            self.page = 0

        if self.page == 0:
            await self.return_to_first_page_func(interaction,embed)
            return



        name = self.repos[self.page - 1]["name"]
        url = self.repos[self.page - 1]["svn_url"]
        created_at = str(self.repos[self.page - 1]["created_at"]).split("T")[0]
        size = self.repos[self.page - 1]["size"] / 1000
        language = self.repos[self.page - 1]["language"]
        stars = self.repos[self.page - 1]["stargazers_count"]
        my_data = self.calc_perecentege(requests.get(f"https://api.github.com/repos/{self.name}/{name}/languages").json())


        embed.description = f"Name : {name}\nRepo Url : {url}\nCreated At : {created_at}\nSize : {size}MB\nLanguage : {language}\nStars : {stars}\n" + "\n".join(my_data)
        embed.set_footer(text=f"Page : {self.page} / {len(self.repos)}")

        await interaction.message.edit(embed=embed)
