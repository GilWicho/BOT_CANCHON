# BOT CANCHÓN

Bot de Discord con reproducción de música mediante Lavalink 4, búsquedas de
Spotify y audio de YouTube.

## Configuración

1. Instala las dependencias de Python:

   ```powershell
   py -m pip install -r requirements.txt
   ```

2. Completa `.env`:

   ```env
   DISCORD_TOKEN=token_del_bot
   BOT_PREFIX=!

   LAVALINK_URI=http://127.0.0.1:2333
   LAVALINK_PASSWORD=una_clave_larga_y_privada

   SPOTIFY_CLIENT_ID=id_de_la_app_de_spotify
   SPOTIFY_CLIENT_SECRET=secreto_de_la_app_de_spotify
   ```

   El `LAVALINK_PASSWORD` debe ser el mismo para el bot y el contenedor.
   Docker Compose transmite automáticamente estas variables a Lavalink.

3. Crea una aplicación en
   [Spotify for Developers](https://developer.spotify.com/dashboard) y copia
   su Client ID y Client Secret. Spotify solo proporciona metadatos; LavaSrc
   busca el audio correspondiente en YouTube.

4. Inicia Lavalink:

   ```powershell
   docker compose up -d lavalink
   ```

   La primera ejecución tarda un poco más porque descarga los plugins de
   YouTube y LavaSrc.

5. Inicia el bot:

   ```powershell
   py main.py
   ```

Para ver el registro de Lavalink:

```powershell
docker compose logs -f lavalink
```

Para detenerlo:

```powershell
docker compose down
```

## Uso

- `!play nombre` busca primero en Spotify.
- `!play URL` acepta canciones, álbumes y playlists de Spotify, además de
  videos y playlists de YouTube.
- `!play yt:nombre` fuerza una búsqueda de YouTube.
- `!queue`, `!nowplaying`, `!pause`, `!resume`, `!skip`, `!stop`.
- `!shuffle`, `!remove 2`, `!move 5 1`, `!clear`.
- `!loop off`, `!loop song`, `!loop queue`.
- `!volume 70`.
- `!musichelp` muestra la ayuda dentro de Discord.

Los botones incluidos en el mensaje de reproducción permiten pausar, saltar,
mezclar, ver la cola y detener. Solo funcionan para usuarios que estén en el
mismo canal de voz.

## Recursos

`compose.yml` limita Lavalink a 1 GB de RAM, con un heap Java máximo de
768 MB y 1.5 vCPU. La cola se limita por defecto a 500 canciones. Estos valores
son adecuados para un servidor de 2 vCPU y 4 GB de RAM que también ejecute el
bot.
