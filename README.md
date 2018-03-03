# Alienz
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/amaurilopez90/GameDev/Alienz/master/LICENSE)

Alienz is a 2-D survival game which challengs the player to fend off against waves of aliens using only 3 projectile weapons and a limited ammunition supply.
The longer you survive, the more difficult the game becomes as enemies begin to increase movement speed as well as spawn rate. Be careful not to pick up consumables too early,
because they won't last long!

# Inspiration
I've always been quite interested in game development and wanted to tackle a project idea that I've had for a long time. I was just learning the Python programming language and 
figured this would be a great challenge to improve my skills a bit. I wanted to create a simple game that would be great to play whenever I wanted to just pass the time.

# How It Works
Alienz is a tile-based game, that is the game map is sectioned off into small 32x32-pixel tiles with a total game map size of 800x608-pixels containing 475 tiles. The tiles themselves fall into two categories: valid and invalid tiles. A tile being valid or invalid simply means whether or not the player is able to walk over it, and these were strategically placed such as to fit the outline of my custom-made game map using TileD and some downloaded textures.

Processing user input from the keyboard simply involves moving the player sprite 32 pixels into the inputted direction, as well as changing the player's currently selected weapon by re-blitting the image of the weapon being selected over the sprite.
