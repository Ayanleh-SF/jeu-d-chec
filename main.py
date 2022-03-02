"""
			JEU D'ECHEC - Ayanleh - Dec.2021

Ce fichier gère le programme dans sa globalité et appel
	tous les autres fichiers

"""
import sys
from mainMenu import *
from chess import *



window = tkinter.Tk()
window.title("Chess Game") 

screen_x = int(window.winfo_screenwidth())
screen_y = int(window.winfo_screenheight())
window_x = 1100
window_y = 700

posX = (screen_x // 2) - (window_x // 2)
posY = (screen_y // 2) - (window_y // 2) - 40

geo = "{}x{}+{}+{}".format(window_x, window_y, posX, posY)

window.geometry(geo) 
window.resizable(width=False, height=False) 
window.update()


screen = MainMenu(window)
screen.mainCanvas()

window.mainloop()

if screen.exitProgram == True:
	print("Jeu quitté")
	sys.exit(0)

if screen.oldGame:
	args = [screen.name1,screen.name2,screen.timeGame,\
			screen.themeGame,screen.chessColor,screen.oldGame,screen.otherInfos,\
			screen.chessBoard,screen.allPosition, screen.eatW, screen.eatB]
else:
	args = [screen.name1,screen.name2,screen.timeGame,\
			screen.themeGame,screen.chessColor,screen.oldGame]

game = Window(args)

game.chess_board()

game.games_infos()

if screen.oldGame:
	player1 = Pieces(game, screen.oldGame, screen.chessBoard)
else:
	player1 = Pieces(game, screen.oldGame, None)

game.players_infos()

game.infos_buttons()

game.retrieveOldGame()

game.window.mainloop()

print("Partie terminée")
