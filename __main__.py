import player_character
import mapmodule
if __name__ == '__main__':
	print("Time to start the game!")
	name = input("What is your name?")
	chartype = int(input("What character type are you? (1 only)"))
	yourcharacter = player_character.PlayerCharacter(name, chartype, 1)
	#yourcharacter.print_stats()
	# yourcharacter.add_exp(800)
	yourcharacter.print_stats()
	game_player = mapmodule.GamePlayer(5, yourcharacter)
	game_player.walk_map()
	game_player.print_map()

