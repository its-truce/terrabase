# Imports
import discord
from discord.ext import commands
import config


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content= True
        activity = discord.Game(name="Terraria")
        super().__init__(command_prefix=commands.when_mentioned_or(config.prefix), intents=intents, activity=activity, status=discord.Status.idle, owner_id = config.owner_id)

    async def setup_hook(self):
        for ext in config.initial_extensions:
            try:
                await self.load_extension(ext)
            except Exception as e:
                print(f"Failed to load extension {ext}.\nException:\n{e}")

# Initializing the bot
bot = Bot()

# Functionality
@commands.is_owner()
@bot.command()
async def sync(ctx: commands.Context):
    await bot.tree.sync()
    await ctx.send(content="Commands have been synced.")


@commands.is_owner()
@bot.command()
async def reload(ctx: commands.Context, extarg: str = None, folder: str = "extensions"):
    if extarg is not None:
        try:
            await bot.reload_extension(f"{folder}.{extarg}")
            await ctx.send(content=f"Successfully reloaded `{extarg}`.")
        except Exception as e:
            await ctx.send(content=f"```py\n{e}\n```")
    else:
        try:
            for ext in config.initial_extensions:
                await bot.reload_extension(ext)
            await ctx.send(content="Successfully reloaded all extensions.")
        except Exception as e:
            await ctx.send(content=f"```py\n{e}\n```")


# Running
if __name__ == "__main__":
    bot.run(config.token)
