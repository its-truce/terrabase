import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import string
import bs4
import utils.scrape as scrape
from colorthief import ColorThief
from io import BytesIO
from urllib.request import urlopen
import urllib.request
import asyncio


def main_info(embed: discord.Embed, soup: bs4.BeautifulSoup):
    title = soup.find(id="firstHeading")
    pre = soup.find(id="mw-content-text").find("p")
    desc = scrape.markdown_links(pre)
    img = soup.find(id="mw-content-text").find_all("img")
    src = None
    url = None
    embed.title = f"{title.text}"
    for image in img:
        if (image.get("alt") != "Console version" and image.get("alt") != "Mobile version" and image.get("alt") != "Desktop version" 
            and image.get("alt") != "First Fractal.png" and image.get("alt") != "Old-gen console version" and image.get("alt") != "Nintendo 3DS version" 
            and image.get("alt") != "Japanese Console version" and image.get("alt") != "Expert mode icon.png" and image.get("alt") != "Master mode icon.png" 
            and image.get("alt") != "Journey mode icon.png"):
            src = image.get("src")
            url = f"https://terraria.wiki.gg{src}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            respi = urllib.request.urlopen(req)
            f = BytesIO(respi.read())
            dominant = ColorThief(f).get_color(quality=1)
            embed.color = discord.Color.from_rgb(r=dominant[0], g=dominant[1], b=dominant[2])
            break
        else:
            embed.color = 0x5865f2
    embed.add_field(name="Description", value=desc.strip(), inline=False)
    embed.set_thumbnail(url=url)
    embed.set_footer(text="ⓘ you can visit the wiki page by clicking on the embed title")
    tooltip_target = soup.find("th", text="Tooltip")
    if tooltip_target is not None:
        tooltip = tooltip_target.find_next_sibling("td")
        embed.add_field(name="Tooltip", value=tooltip.text, inline=False)
    else:
        pass
    damage_target = soup.find("th", text="Damage")
    if damage_target is not None:
        damage = damage_target.find_next_sibling("td")
        normal = damage.find("span", class_="m-normal")
        if normal is not None:
            embed.add_field(name="Damage", value=f"{normal.text} (Normal)", inline=False)
        else:
            embed.add_field(name="Damage", value=damage.text, inline=False)
    else:
        pass
    kb_target = soup.find("th", text="Knockback")
    if kb_target is not None:
        kb = kb_target.find_next_sibling("td")
        embed.add_field(name="Knockback", value=kb.text, inline=False)
    else:
        pass
    crit_target = soup.find("th", text="Critical chance")
    if crit_target is not None:
        crit = crit_target.find_next_sibling("td")
        embed.add_field(name="Critical chance", value=crit.text, inline=False)
    else:
        pass
    use_target = soup.find("th", text="Use time")
    if kb_target is not None:
        use = use_target.find_next_sibling("td")
        embed.add_field(name="Use time", value=use.text, inline=False)
    else:
        pass
    velo_target = soup.find("th", text="Velocity")
    if kb_target is not None:
        velo = velo_target.find_next_sibling("td")
        embed.add_field(name="Velocity", value=velo.text, inline=False)
    else:
        pass
    life_target = soup.find("th", text="Max Life")
    if life_target is not None:
        life = life_target.find_next_sibling("td")
        normal = life.find("span", class_="m-normal")
        if normal is not None:
            embed.add_field(name="Max Life", value=f"{normal.text} (Normal)", inline=False)
        else:
            embed.add_field(name="Max Life", value=life.text, inline=False)
    else:
        pass
    def_target = soup.find("th", text="Defense")
    if def_target is not None and def_target.find("a") is not None and def_target.find("a")["title"] == "Defense":
        defe = def_target.find_next_sibling("td")
        embed.add_field(name="Defense", value=defe.text, inline=False)
    else:
        pass
    notes = soup.find("h2", text="Notes")
    trivia = soup.find("h2", text="Trivia")
    return_list = [embed, notes, trivia]
    return return_list


def notes_info(soup: bs4.BeautifulSoup):
    notes_list = soup.find("h2", text="Notes").find_next_sibling("ul")
    content = ""
    for i, note in enumerate(notes_list.find_all("li")):
        content += f"**{i+1}**. {scrape.markdown_links(note)}\n"
    return content


def trivia_info(soup: bs4.BeautifulSoup):
    trivia_list = soup.find("h2", text="Trivia").find_next_sibling("ul")
    content = ""
    for i, note in enumerate(trivia_list.find_all("li")):
        content += f"**{i+1}**. {scrape.markdown_links(note)}\n"
    return content


class WikiDropdown(discord.ui.Select):
    def __init__(self, notes, trivia, soup, embed):
        self.notes = notes
        self.trivia = trivia
        self.soup = soup
        self.embed: discord.Embed = embed
        options = [discord.SelectOption(label="Main Info", description="Displays the main info available on the wiki.", default=True)]
        if notes is True:
            options.append(discord.SelectOption(label="Notes", description="Displays the notes about the page available on the wiki."))
        if trivia is True:
            options.append(discord.SelectOption(label="Trivia", description="Displays the trivia about the page available on the wiki."))
        super().__init__(min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.values[0] == "Notes":
            blocking_notes = asyncio.to_thread(notes_info, self.soup)
            result = await blocking_notes
            notes_content = result
            notes_embed = discord.Embed(color=self.embed.color, title=self.embed.title, url=self.embed.url, 
                                        description=notes_content[:4095] if len(notes_content) > 4096 else notes_content)
            notes_embed.set_thumbnail(url=self.embed.thumbnail.url)
            self.options[0].default = False
            if self.trivia:
                self.options[2].default = False
                self.options[1].default = True
            if not self.trivia and self.notes:
                self.options[1].default = True
            await interaction.edit_original_response(embed=notes_embed, view=self.view)
        if self.values[0] == "Trivia":
            blocking_trivia = asyncio.to_thread(trivia_info, self.soup)
            result = await blocking_trivia
            trivia_content = result
            trivia_embed = discord.Embed(color=self.embed.color, title=self.embed.title, url=self.embed.url, 
                                         description=trivia_content[:4095] if len(trivia_content) > 4096 else trivia_content)
            trivia_embed.set_thumbnail(url=self.embed.thumbnail.url)
            self.options[0].default = False
            if self.notes:
                self.options[1].default = False
                self.options[2].default = True
            if not self.notes and self.trivia:
                self.options[1].default = True                
            await interaction.edit_original_response(embed=trivia_embed, view=self.view)
        if self.values[0] == "Main Info":
            if not self.notes and self.trivia:
                self.options[1].default = False
            if not self.trivia and self.notes:
                self.options[1].default = False
            if self.trivia and self.notes:
                self.options[1].default = False
                self.options[2].default = False
            self.options[0].default = True
            await interaction.edit_original_response(embed=self.embed, view=self.view)             


class WikiView(discord.ui.View):
    def __init__(self, soup, embed, notes=False, trivia=False):
        super().__init__()
        self.notes = notes
        self.trivia = trivia
        if self.notes is not None:
            self.notes = True
        if self.notes is None:
            self.notes = False
        if self.trivia is not None:
            self.trivia = True
        if self.trivia is None:
            self.trivia = False
        self.soup = soup
        self.embed = embed
        dropdown = WikiDropdown(notes=self.notes, trivia=self.trivia, soup=self.soup, embed=self.embed)
        if self.notes is True or self.trivia is True:
            self.add_item(dropdown)


class Wiki(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Sends a wiki.gg link to the item or mechanic you specified.")
    @app_commands.describe(search="The page to search for.")
    async def wiki(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer()
        caps = string.capwords(search, sep=None)
        page = caps.replace(" ", "_")
        URL = "https://terraria.wiki.gg/wiki/Special:Search"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{URL}/{page}", allow_redirects=True) as response:
                redirect = response.url
                async with session.get(redirect) as redirect_response:
                    body = await redirect_response.text()
        soup = bs4.BeautifulSoup(body, "html.parser")
        wiki_embed = discord.Embed(color=0x5865f2, url=f"{URL}/{page}")
        blocking_main = asyncio.to_thread(main_info, wiki_embed, soup)
        result = await blocking_main
        wiki_embed = result[0]
        notes = result[1]
        trivia = result[2]
        view = WikiView(notes=notes, trivia=trivia, soup=bs4.BeautifulSoup(body, "html.parser"), embed=wiki_embed)
        if notes is not None or trivia is not None:
            await interaction.followup.send(embed=wiki_embed, view=view)
        else:
            await interaction.followup.send(embed=wiki_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Wiki(bot))
