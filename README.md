# Aram-Bot
Discord bot to show a players ARAM mmr

based on the API by https://whatismymmr.com
licencing and documentation at: https://dev.whatismymmr.com/

Usage:

The !mmr command in any discord text channel will look up a players ARAM mmr.
parameters:
name - case insensitive, whitespace sensitive summoner name.
region - case insensitive region of the player, can either be euw, eune, or na. Region is euw by default.
response:
mmr, deviation and closest rank of that player, as well, as any errors that occur.

The !multi command looks up multiple players ARAM mmr similar to the "!mmr" command.
parameters:
Same as "!mmr", multiple names aswell as the region need to be seperated by either " joined the lobby" or ", ".
response:
same as "!mmr" but for every name.
