# A RESTful Adventure (Use Cases)

## Goal: Safely navigate a dungeon from start to finish
**Level:** Summary

### Resources

* Character
* Dungeon
* Room

### State transitions

* Add a character to the world
* Remove a character from the world
* Move a character to a dungeon entrance
* Move a character from one room to another within a dungeon
* Move a character to a dungeon exit

### Main success scenario

1. Player chooses a character.
2. Player chooses a dungeon.
3. Player enters the dungeon.
4. Player chooses from a set of doorways leading out of the room.
5. Player repeats step (4) until they find the exit.
6. Player wins.
8. Game resets the Player's character.
9. Game asks the player if they would like to play again.
10. Play resumes at (1).

### Extensions


1a. Game has no characters, or Player does not wish to use any
    of the existing characters in the Game:

    1a1. Player creates a character.
    1a2. Player chooses whether to use the newly-created character, or to
         create another one.

1b. Player has too many characters to choose from, or no longer wishes
    to use a particular character:

    1b1. Player removes one or more characters from the Game.

1c. Player has already chosen a character from a previous round:

    1c1. Player chooses whether to use the same character again.

2a. Game has no dungeons:

    2a1. Administrator adds one or more dungeons to Game.
    2a2. Player chooses a dungeon.

2b. Player's character is already in a dungeon:

    2b1. Player chooses whether to enter a new dungeon, start over, or keep
         playing from the character's current position.

4a. Player quits:

    4a1. Game remembers the last location of the Player's character.
    4a2. Game resumes at step (1) when Player returns.

4b. Player tries to cheat by teleporting to a room to which there is no 
    doorway:

    4b1. Game denies the request.
    4b2. Game displays a message.

5a. Player has entered a dead-end (a room with no other doorways besides the
    one just used to arrive in the room):

    5a1. Game displays message.
    5a2. Player retreats into previous room.

9a. Player does not wish to play another round:

    9a1. Proceed as in (4a).






