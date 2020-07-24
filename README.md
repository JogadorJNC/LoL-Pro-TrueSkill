# LoL-Pro-TrueSkill
TrueSkill applied to all official competition games of League of Legends. 

This whole thing is very janky, I created it as a side-project completely for fun. 
I didn't even intend to publish it anywhere at first, but it may end up being useful for other people.

Every match is counted as having 12 "players", the 5 players on each team and the teams themselves. I wanted to account for orgs finding success even with worse players.

TrueSkill(TM) is a rating system developed by Microsoft, commercial use of it is restricted to Xbox Live games.   
This project uses the trueskill package made by Heungsub Lee, more info on it can be found at https://trueskill.org/.    
All the data is gathered using Leaguepedia's API, more info on it can be found at https://lol.gamepedia.com/Help:API_Documentation.   
There is also a Leaguepedia API discord server, https://discord.gg/m3SCJhs.

Props to River for helping me figure out cargo queries.
