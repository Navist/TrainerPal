import asyncio
import traceback

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

import consolePrint


class ExtensionManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='extension_controller', description="Function for managing modules.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(action_type=[
        Choice(name='Reload', value='reload'),
        Choice(name='Load', value='load'),
        Choice(name='Unload', value='unload')
    ])
    async def extension_controller(self, inter: discord.Interaction, module_name: str, action_type: Choice[str]):

        if action_type.value == 'load':
            await self.client.load_extension(module_name)

        elif action_type.value == 'reload':
            await self.client.reload_extension(module_name)

        elif action_type.value == 'unload':
            await self.client.unload_extension(module_name)

        await self.ex_controller(module_name, action_type.value, inter)

    async def ex_controller(self, module_name, action_type, inter):
        await consolePrint.console_print(f"module-{action_type}", f"{module_name}")
        await inter.response.send_message(f"{module_name} has been {action_type}ed.", ephemeral=True)

    @extension_controller.error
    async def extension_controller_error(self, inter, error):
        await inter.response.send_message(error, ephemeral=True)


async def setup(client):
    await client.add_cog(ExtensionManager(client))
