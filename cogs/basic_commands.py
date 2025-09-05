import discord
from discord.ext import commands
import time
import random
from collections import defaultdict, deque

class BasicCommands(commands.Cog):
    """Comandos básicos del bot"""
    
    def __init__(self, bot):
        self.bot = bot
        # Almacena timestamps por usuario con tamaño limitado para ahorrar memoria
        self.message_tracker = defaultdict(lambda: deque(maxlen=20))
        self.spam_limit = 5  # Mensajes límite
        self.time_window = 10  # Ventana de tiempo en segundos
        # Límite de entradas de usuarios en el tracker para evitar crecimiento ilimitado
        self.tracker_user_limit = 400

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignora mensajes del propio bot
        if message.author == self.bot.user:
            return
        
        # Responde a "hola" sin prefijo (si contiene "hola" en cualquier parte)
        if "hola" in message.content.lower():
            await message.channel.send("sho")
        
        # Mensaje personalizado para usuario específico en canal específico
        if (message.author.name.lower() == "neryflowydembow" and 
            message.channel.name == "「💬」𝐆eneral"):
            # 25% de probabilidad de responder
            if random.randint(1, 100) <= 25:
                await message.channel.send("sho mixqueño cerote")
        
        # Nueva: 5% de probabilidad de responder "Shooo" a cualquier mensaje
        if random.randint(1, 100) <= 5:
            await message.channel.send("Shooo")
        
        # Sistema anti-spam para todos los usuarios
        current_time = time.time()
        user_id = message.author.id
        
        # Agregar timestamp del mensaje actual (deque con maxlen lo recorta automáticamente)
        self.message_tracker[user_id].append(current_time)

        # Limpiar mensajes antiguos (fuera de la ventana de tiempo)
        # Reemplazamos el deque por uno nuevo con los timestamps válidos
        valid = [t for t in self.message_tracker[user_id] if current_time - t <= self.time_window]
        self.message_tracker[user_id] = deque(valid, maxlen=20)

        # Poda global simple si el dict crece demasiado
        if len(self.message_tracker) > self.tracker_user_limit:
            # eliminar usuarios cuyo deque esté vacío primero
            keys = [k for k, v in self.message_tracker.items() if not v]
            for k in keys[:50]:
                del self.message_tracker[k]
            # si aún es grande, eliminar entradas al azar (primeras n)
            if len(self.message_tracker) > self.tracker_user_limit:
                for k in list(self.message_tracker.keys())[:50]:
                    del self.message_tracker[k]
        
        # Verificar si excede el límite de spam
        if len(self.message_tracker[user_id]) > self.spam_limit:
            # Buscar el rol "Muted"
            muted_role = discord.utils.get(message.guild.roles, name="Muted")
            
            if muted_role:
                # Verificar si ya tiene el rol
                if muted_role not in message.author.roles:
                    try:
                        await message.author.add_roles(muted_role)
                        await message.channel.send(f"Ya sho vos, payaso de mrd 🤡")
                        # Limpiar el tracker después de aplicar el mute
                        self.message_tracker[user_id] = []
                    except discord.Forbidden:
                        print(f"No tengo permisos para asignar roles a {message.author}")
                    except Exception as e:
                        print(f"Error asignando rol: {e}")
            else:
                print("Rol 'Muted' no encontrado")

    @commands.command(name='avatar')
    async def avatar_command(self, ctx, member: discord.Member = None):
        """Muestra el avatar del usuario mencionado o el tuyo"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"Avatar de {member.display_name}",
            color=0x00ff00
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='checkperms')
    async def check_permissions(self, ctx):
        """Verifica los permisos del bot"""
        bot_member = ctx.guild.me
        permissions = bot_member.guild_permissions
        
        embed = discord.Embed(title="Permisos del Bot", color=0x00ff00)
        embed.add_field(name="Gestionar roles", value="Si" if permissions.manage_roles else "No", inline=True)
        embed.add_field(name="Gestionar mensajes", value="Si" if permissions.manage_messages else "No", inline=True)
        embed.add_field(name="Kickear miembros", value="Si" if permissions.kick_members else "No", inline=True)
        
        # Verificar jerarquía con rol Muted
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role:
            can_manage = bot_member.top_role > muted_role
            embed.add_field(name="Puede gestionar rol Muted", value="Si" if can_manage else "No", inline=True)
        else:
            embed.add_field(name="Rol Muted", value="No encontrado", inline=True)
        
        await ctx.send(embed=embed)

    # Aquí puedes agregar comandos básicos

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
