# Design Diary - Pygame Space Invaders

I decided to get an early start on this project since I feel like I didn't put in enough time to be satisfied
with the final product of my last assignment. On the first day, I decided to go through the entire ~2 hour 
YouTube tutorial about the given game code so I would have an understanding of the basic game features
for me to expand upon. I decided that a fun version of this game would be one with multiple bullets per screen
and different firing modes. Once I implemented this, I found that the game was no longer challenging; I could
easily slaughter all of the enemies by just pressing and holding the fire button in auto firing mode. So, I 
decided the next step would be to make an accuracy counter to keep track of how many bullets hit their target.
From this point, I found that the game was not very fun since I could not easily loop back and play another
round from the game-over screen. I decided to add a main menu to give the game screen something to loop-back
to after a game is finished. At this point, I was getting tired of hearing the background music playing and I was
also sick of commenting/uncommenting the audio code to make it mute, so I decided to add mute/unmute hotkeys for
the background music. Once this was all working well, I realized that a pause screen would be nice for the player
to mute/unmute without the game actively playing, as well as the option to surrender if the player would like to
go back to the main menu. When everything was working correctly between the different screens, I decided that I
wanted a transitional screen for the surrender option; this screen would indicate that the player has been captured
and then time-delay switch to the main menu. I wanted a game that was actually playable over and over again, with
more emphasis on making it fun-ish rather than being detail-rich.

![PygameSpaceInvaderDemo](https://github.com/rja45/Space-Invaders-Pygame/blob/master/SpaceInvadersDemo3.gif)





