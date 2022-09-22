from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import discord
import asyncio
from datetime import datetime
import traceback
from consolePrint import console_print
import qrcode
import typing

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='sync', pass_context=True)
    async def sync_tree(self, ctx):
        synced = await self.client.tree.sync()
        await ctx.send(f"{len(synced)} commands synced.")


    @app_commands.command(name='sync', description='Syncs the command tree.')
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, inter: discord.Interaction):
        try:
            synced = await inter.client.tree.sync()
            await inter.response.send_message(f"Synced {len(synced)} commands.", ephemeral=True)
            await consolePrint.console_print("tree-sync", f"Command Tree Synced by {inter.user}:{inter.user.id}")
        except Exception as e:
            await inter.response.send_message(f"Error: {traceback.print_exception(e)}", ephemeral=True)
            await consolePrint.console_print("tree-sync-error", f"Command Tree Synced by {inter.user}:{inter.user.id} | {e}")

    @sync.error
    async def sync_error(self, interaction, error):
        await interaction.response.send_message(error, ephemeral=True)


    @app_commands.command(name='qr_generate', description='Generates a QR code.')
    @app_commands.describe(teams='Choose your Pokemon Go Team')
    @app_commands.describe(trainer_code='Enter your Trainer code WITHOUT spaces')
    @app_commands.describe(trainer_name='Enter your Trainer name')
    @app_commands.choices(teams=[
        Choice(name='Team Valor (Red)', value='valor'),
        Choice(name='Team Mystic (Blue)', value='mystic'),
        Choice(name='Team Instinct (Yellow)', value='instinct')
    ])
    async def qr_generate(
        self, inter: discord.Interaction,
        trainer_code: int,
        trainer_name: str, teams: Choice[str]
        ):

        team = teams.value
        if team == 'valor':
            em = discord.Embed(
                title=trainer_name, timestamp=datetime.now(), color=16126472)
            em.set_thumbnail(
                url='https://static.wikia.nocookie.net/pokemongo/images/2/22/Team_Valor.png/revision/latest?cb=20160717150715')
        elif team == 'mystic':
            # '0076f2')
            em = discord.Embed(title=trainer_name,
                               timestamp=datetime.now(), color=30450)
            em.set_thumbnail(
                url='https://static.wikia.nocookie.net/pokemongo/images/f/f4/Team_Mystic.png/revision/latest?cb=20160717150716')
        elif team == 'instinct':
            em = discord.Embed(
                title=trainer_name, timestamp=datetime.now(), color=16765697)
            em.set_thumbnail(
                url='https://static.wikia.nocookie.net/pokemongo/images/d/d4/Team_Instinct.png/revision/latest?cb=20200803123751')


        em.set_footer(text=f"{inter.user.id}")

        em.add_field(name='Trainer Code', value=f'{trainer_code}')
        qr_code_file = f"./trainerQRs/{trainer_code}.png"

        qrObject = qrcode.QRCode(version=1, box_size=5)

        qrObject.add_data(trainer_code)
        qrObject.make()
        image = qrObject.make_image()
        image.save(qr_code_file)
        qr_image = discord.File(qr_code_file, filename=f'{trainer_code}.png')
        em.set_image(url=f'attachment://{trainer_code}.png')

        await inter.response.send_message(file=qr_image, embed=em)



async def setup(client):
    await client.add_cog(Commands(client))
