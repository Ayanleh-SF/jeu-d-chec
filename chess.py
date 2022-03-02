"""
			JEU D'ECHEC - Ayanleh - Dec.2021

Ce fichier gère tout ce qui concerne la fenêtre affichant 
   l'échiquier

"""

import tkinter
import tkinter.font as font
import rules
import time

class Window:

	click_backup = 'dark'
	img_saved = None
	old_position = []
	color_who_plays = "w"
	checkmate = "jeu"
	pris_en_passant = []
	letPass = True
	gameTime = "10:00"
	timer1 = "10:00"
	timer2 = "10:00"
	name1 = "Joueur 1"
	name2 = "Joueur 2"
	chessColor = "Vert"
	helpMove = []
	args = []
	freeze = None

	def __init__(self,args):
		# Création de la fenetre
		self.window = tkinter.Tk()
		self.window.title("Chess Game") 
		self.allPosition = []
		self.pieceWhiteEaten = [0,0]
		self.pieceBlackEaten = [0,0]
		self.saveEatenPieceW = []
		self.saveEatenPieceB = []

		if type(args[2]) == list and args[5] == True:
			Window.timer1 = args[2][0]
			Window.timer2 = args[2][1]
		else:
			Window.gameTime = args[2]+":00"
			Window.timer1 = args[2]+":00"
			Window.timer2 = args[2]+":00"

		Window.name1 = args[0]
		Window.name2 = args[1]
		Window.themeColor = str(args[3])
		Window.chessColor = str(args[4])
		Window.args = args

		screen_x = int(self.window.winfo_screenwidth())
		screen_y = int(self.window.winfo_screenheight())
		window_x = 1100
		window_y = 700

		posX = (screen_x // 2) - (window_x // 2)
		posY = (screen_y // 2) - (window_y // 2) - 40

		geo = "{}x{}+{}+{}".format(window_x, window_y, posX, posY)

		self.window.geometry(geo) 
		self.window.resizable(width=False, height=False) 
		self.window.bind("<Button-1>", self.onClic)
		self.window.update()
		self.underCanvas = tkinter.Canvas(self.window, width=1100, height=700, bg=Window.themeColor)
		self.underCanvas.place(x=0,y=0)
		ready_createImage()

	def retrieveOldGame(self):
		# On charge l'ancienne partie
		if Window.args[5] == True:
			args = Window.args[6]
			Window.color_who_plays = args[0]
			Window.freeze = args[1]
			Window.pris_en_passant = args[2]
			Window.old_position = args[3]
			Window.letPass = args[4]
			Window.click_backup = args[5]
			Window.helpMove = args[6]

			self.allPosition = Window.args[8]
			self.games_infos()

			for pieceWhite in Window.args[9]:
				self.pieceEaten(pieceWhite[2:4])

			for pieceBlack in Window.args[10]:
				self.pieceEaten(pieceBlack[2:4])


	def clicPromotion(self, event):
		# On change le pion avec la pièce selectionnée
		for element in self.canvasPromotion:
			if element == event.widget:
				img = self.get_image(element)[1][0]
				self.promote(img, self.posPromote)
				self.posPromote = []
				self.window2.destroy()
				Window.checkmate = Window.freeze
				Window.freeze = None
				self.updateTimer()


	def promotion(self, posx, posy, old_pos, pos, color):
		# On propose une promotion du pion
		Window.freeze = Window.checkmate
		Window.checkmate = "fini"
		self.window2 = tkinter.Toplevel(self.window)
		x_old, y_old = old_pos

		self.window2.geometry("500x200+500+200")
		self.window2.resizable(width=False, height=False)
		self.window2.configure(bg="#F0ECE7")
		self.window2.bind("<Button-1>", self.clicPromotion)
		self.window2.overrideredirect(1) # retire la barre de titre

		# On charge les images des pièces
		img_queen = [element for element,name in pieces_dict.items() if str(name) == str(color+"Q")]
		img_rock = [element for element,name in pieces_dict.items() if str(name) == str(color+"r")]
		img_knight = [element for element,name in pieces_dict.items() if str(name) == str(color+"k")]
		img_bishop = [element for element,name in pieces_dict.items() if str(name) == str(color+"b")]
		img = [img_queen,img_rock,img_knight,img_bishop]

		# On affiche les images des pièces dans la fenêtre
		self.canvasPromotion = [] 
		if color == "w":
			bgColor = "#00081B"
		else:
			bgColor = "#F0ECE7"
		for x in range(0,4):
			self.canvasPromotion.append(tkinter.Canvas(self.window2, width=80, height=80, bg=bgColor))
			self.canvasPromotion[x].place(x=30+(x*120), y=60)
			self.canvasPromotion[x].create_image(42, 40, image=img[x], tag="get_image")

		# On affiche un message sur la fenêtre
		canvaMsg = tkinter.Canvas(self.window2, width=450, height=30, bg="#F0ECE7")
		msg = "Choisissez une pièce"
		canvaMsg.create_text(220,20,text=msg,font=('Calibri',15),fill="black")
		canvaMsg.place(x=20,y=15)

		# On affiche le nom des pièces
		canvaPiece = tkinter.Canvas(self.window2, width=470, height=30, bg="#F0ECE7")
		canvaPiece.create_text(296,15,text="Cavalier",font=('Calibri',15),fill="black")
		canvaPiece.create_text(56,15,text="Reine",font=('Calibri',15),fill="black")
		canvaPiece.create_text(176,15,text="Tour",font=('Calibri',15),fill="black")
		canvaPiece.create_text(416,15,text="Cheval",font=('Calibri',15),fill="black")
		canvaPiece.place(x=15,y=150)
		
		# On détecte la case cliquée et on transforme le pion
		self.board[x_old][y_old].delete("all")
		self.posPromote = pos


	def set_help(self, move):
		Window.helpMove.append(move)

	def showHelp(self):
		if Window.helpMove == []:
			self.allPosition.append("Aucune aide disponible")
		else:
			self.allPosition.append("---------- AIDE ------------")
			for element in Window.helpMove:
				piece = [name for name,nme in vrai_nom.items() if str(nme) == str(element[:2])]
				txt = piece[0]+str(element[2:])
				self.allPosition.append(txt)
			self.allPosition.append("-------- FIN DE L'AIDE -------")

		self.games_infos()

	def chess_board(self):
		# Création du plateau d'échecs
		self.canvas = tkinter.Canvas(self.window, width=560, height=560, bg='blue')
		self.canvas.place(x=30, y=30)
		
		# Création d'une grille de case
		self.board = []
		count = 0
		for y_pos in range(0, 561, 80):
			canvas_test = []
			for x_pos in range(0, 561, 80):
				if count % 2:
					if Window.chessColor == "Vert":
						color = '#EEEED2'
					if Window.chessColor == "Bleu":
						color = '#EAE9D2'
					if Window.chessColor == "Brun":
						color = '#F0D9B5'
				else:
					if Window.chessColor == "Vert":
						color = '#769656'
					if Window.chessColor == "Bleu":
						color = '#4B7399'
					if Window.chessColor == "Brun":
						color = '#B58863'
				count += 1
				canvas_test.append(tkinter.Canvas(self.window, width=80, \
					height=80, bg=color))

				canvas_test[-1].place(x=x_pos+30, y=y_pos+30)
			self.board.append(canvas_test)

			x_pos = 0
			count += 1
		
	def onClic(self, event):
		condition = True
		count_x_ancien = -1
		# On remet la couleur par défaut
		if Window.click_backup != 'dark' and Window.checkmate != "fini": 
			for yellow_element2 in self.board:
				count_x_ancien += 1 # Coordonnée x de la pos initiale de la pièce
				count_y_ancien = -1 # # Coordonnée y de la pos initiale de la pièce
				for yellow_element in yellow_element2:
					count_y_ancien += 1
					if yellow_element["bg"] == 'yellow' \
							or yellow_element["bg"] == "#BACA2B":

						Window.old_position.append([count_x_ancien, count_y_ancien])
						yellow_element["bg"] = Window.click_backup[1]
						Window.click_backup = 'dark'
						condition = False

		
		# Changement de la couleur de la case en cas de clic
		if Window.click_backup == 'dark' and condition and Window.checkmate != "fini": 
			for element2 in self.board:
				for element in element2:
					if element == event.widget:
						# On vérifie qu'il y a une image sur la case cliquée
						if self.get_image(element)[0] != "":
							if self.get_image(element)[1][0][0] == Window.color_who_plays:
								Window.img_saved = self.get_image(element)[0]
								Window.old_position = []
								Window.click_backup = [event.widget, event.widget["bg"]]

								# Modification de la couleur de la case sélectionnée
								if element["bg"] in ["#769656","#4B7399","#B58863"]:
									element.config(bg='#BACA2B')
								elif element["bg"] in ["#EEEED2","#EAE9D2","#F0D9B5"]:
									element.config(bg='yellow')

		count_x = -1
		# Affichage des coordonneés de la pièce cliquée
		if condition == False and Window.checkmate != "fini": 
			for k in self.board:
				count_x += 1
				count_y = -1
				for j in k:
					count_y += 1

					if j == event.widget and Window.checkmate not in ["fini","jeu"]: 
						# Ici, il y a echec et on vérifie si le déplacement va annuler l'échec
						x_pos, y_pos = Window.old_position[0]
						img = self.get_image(self.board[x_pos][y_pos])[0]
						
						if rules.testBoard(self, self.board, img, Window.old_position[0], [count_x,count_y]) == True:
							Window.checkmate = "jeu"
							Window.helpMove = []
							self.deplacement(count_x, count_y)
							break

						else:
							checkmate = rules.checkmate(self, self.board)
							if checkmate != None:
								self.change_Color(checkmate)
								
								
							

					if j == event.widget and Window.checkmate == "jeu":
						# On fait un déplacement de pièce
						self.deplacement(count_x, count_y)

	
	def deplacement(self, x_pos, y_pos):
		# On vérifie qu'il n'y a rien dans la case sélectionnée
		if self.get_image(self.board[x_pos][y_pos])[0] == "":
			#Vérifier que les règles permettent le déplacement
			x_case = Window.old_position[0][0]
			y_case = Window.old_position[0][1]
			img = self.get_image(self.board[x_case][y_case])[0]
			img_name = self.get_image(self.board[x_case][y_case])[1]
	
			if rules.which_piece(img_name, self, [x_pos, y_pos],\
				 Window.old_position[0]):

				if rules.testBoard(self, self.board, img,Window.old_position[0],[x_pos, y_pos], mode=1):

					# Va nous permettre d'afficher des infos
					pieceName = [name for name,element in vrai_nom.items() if element == img_name[0]][0]
					piecePosition = ">  "+pieceName+" : "+str(chr(65+y_case))+str(x_case+1)+" -> "+str(chr(65+y_pos))+str(x_pos+1)
					self.allPosition.append(piecePosition)
					self.games_infos()

					# On crée une pièce à la position sélectionnée par le joueur
					self.board[x_pos][y_pos].create_image(42, 40, image=Window.img_saved,\
						 tag="get_image")

					# On supprime la pièce de la case d'avant son déplacement
					x_pos_old, y_pos_old = Window.old_position[0]
					self.del_image(x_pos_old, y_pos_old)

					# Permet de savoir quel joueur doit jouer
					if Window.color_who_plays == "w":
						Window.color_who_plays = "b"
					else:
						Window.color_who_plays = "w"

					# Vérifie si le déplacement a entraîné un echec ou un echec et mat
					checkmate = rules.checkmate(self, self.board)
					if checkmate != None:
						if rules.help(self, self.board, checkmate[0], checkmate[1]) == False:
							
							if Window.color_who_plays == "b":
								self.allPosition.append("FIN : les blancs gagnent")
							else:
								self.allPosition.append("FIN : les noirs gagnent")

							self.games_infos()
							Window.checkmate = "fini"
						
						else:
							Window.checkmate = "echec"
					else:
						if self.pat():
							self.allPosition.append("Match nul, partie nulle")
							self.games_infos()
							Window.checkmate = "fini"

				else:
					Window.old_position = []

			else:
				Window.old_position = []

		
		else: # Si une collision est rencontrée
			x_case = Window.old_position[0][0]
			y_case = Window.old_position[0][1]
			img = self.get_image(self.board[x_case][y_case])[0]
			img_name = self.get_image(self.board[x_case][y_case])[1]
			
			color_clicked = self.get_image(self.board[x_pos][y_pos])[1][0]
			color_selected = self.get_image(self.board[x_case][y_case])[1][0]

			if rules.which_piece(img_name, self, [x_pos, y_pos],\
				 Window.old_position[0]):

				if color_selected != color_clicked and rules.testBoard(self, self.board, img,Window.old_position[0],[x_pos, y_pos],mode=1):
					self.del_image(x_pos, y_pos, no_clear=0)

					# Va nous permettre d'afficher des infos
					pieceName = [name for name,element in vrai_nom.items() if element == img_name[0]][0]
					piecePosition = ">  "+pieceName+" : "+str(chr(65+y_case))+str(x_case+1)+" -> "+str(chr(65+y_pos))+str(x_pos+1)
					self.allPosition.append(piecePosition)
					self.games_infos()

					self.board[x_pos][y_pos].create_image(42, 40, image=Window.img_saved,\
					 tag="get_image")

					# On supprime la pièce de la case d'avant son déplacement
					x_pos_old, y_pos_old = Window.old_position[0]
					self.del_image(x_pos_old, y_pos_old)

					if Window.color_who_plays == "w":
						Window.color_who_plays = "b"
					else:
						Window.color_who_plays = "w"

					checkmate = rules.checkmate(self, self.board)
					
					if checkmate != None:
						if rules.help(self, self.board, checkmate[0], checkmate[1]) == False:
							if Window.color_who_plays == "b":
								self.allPosition.append("FIN : les blancs gagnent")
							else:
								self.allPosition.append("FIN : les noirs gagnent")

							self.games_infos()
							Window.checkmate = "fini"
						else:
							Window.checkmate = "echec"
					else:
						if self.pat():
							self.allPosition.append("Match nul, partie nulle")
							self.games_infos()
							Window.checkmate = "fini"

				else:
					Window.old_position = []

			else:
				Window.old_position = []

			
	def get_image(self, canva):
		img = canva.itemcget("get_image", "image")
		img_name = [name for element,name in pieces_dict.items() if str(element) == img]
		
		return img, img_name


	def del_image(self, x_pos, y_pos, no_clear=1):
		# supprime l'image qui est sur la case selectionnée
		canvas = self.board[x_pos][y_pos]
		canvas.delete("all")
		if no_clear == 1:
			Window.old_position = []


	def pat(self):
		# Permet de savoir si il y a pat
		for x in range(0,8):
			for y in range(0,8):
				if rules.check_is_empty(self,[x,y]) == False:
					img = self.get_image(self.board[x][y])[0]
					img_name = self.get_image(self.board[x][y])[1]
					if Window.color_who_plays == img_name[0][0]:
						for i in range(0,8):
							for j in range(0,8):
								if rules.which_piece(img_name,self,[i,j],[x,y], checkmate=1):
									if rules.testBoard(self, self.board, img,[x,y],[i,j]):
										return False
		return True

	def change_Color(self, checkmate):
		# Change la couleur du roi si on fait un déplacement qui n'annule pas l'échec
		x_roi, y_roi = checkmate[1]
		color = self.board[x_roi][y_roi]["bg"]

		if color in ["#EEEED2","#EAE9D2","#F0D9B5"]:
			r = 238
			g = 238
			b = 210
			for x in range(0,30):
				r += (1/30)
				g -= (181/30)
				b -= (171/30)
				colorHexa = "#"+("%x"%int(r)).upper()+("%x"%int(g)).upper()+("%x"%int(b)).upper()
				self.board[x_roi][y_roi].config(bg=colorHexa)
				self.window.update()
				time.sleep(0.00001)
			self.board[x_roi][y_roi].config(bg=color)

		if color in ["#769656","#4B7399","#B58863"]:
			r = 118
			g = 150
			b = 86
			for x in range(0,30):
				r += (121/30)
				g -= (93/30)
				b -= (47/30)
				colorHexa = "#"+("%x"%int(r)).upper()+("%x"%int(g)).upper()+("%x"%int(b)).upper()
				self.board[x_roi][y_roi].config(bg=colorHexa)
				self.window.update()
				time.sleep(0.00001)
			self.board[x_roi][y_roi].config(bg=color)

	def promote(self, new_piece, pos):
		# On met la pièce choisi à la bonne position
		img = [element for element,name in pieces_dict.items() if str(name) == new_piece]
		x_pos, y_pos = pos

		self.board[x_pos][y_pos].create_image(42, 40, image=img,\
			tag="get_image")

		#On vérifie si la promotion n'a pas entraîné un échec et mat
		checkmate = rules.checkmate(self, self.board)
					
		if checkmate != None:
			if rules.help(self, self.board, checkmate[0], checkmate[1]) == False:
				print("La partie est finie")
				Window.checkmate = "fini"
			else:
				Window.checkmate = "echec"
		else:
			if self.pat():
				print("Match nul, partie nulle")
				Window.checkmate = "fini"

	def getPassant(self):
		return Window.pris_en_passant

	def setPassant(self,liste):
		Window.pris_en_passant = liste

	def games_infos(self):
		# (Menu infomation) Affichage des coordonnées des pièces jouées
		for element in self.allPosition:
			oldVersion = element
			element.lstrip()
			while len(element) != 36:
				element += " "
			self.allPosition[self.allPosition.index(oldVersion)] = element

		self.infos = tkinter.Canvas(self.window, width=370, height=300, bg='#00081B')
		x = 280
		for msg in self.allPosition[::-1]:
			self.infos.create_text(115, x,text=msg,font=('Calibri',12),fill="white")
			x -= 20

		self.infos.place(x=700, y=170)

	def players_infos(self):
		# Affichage des infos sur les joueurs

		self.player1_canva = tkinter.Canvas(self.window, width=370, height=120, bg='#312E2B')
		# Ajouter le nom du joueur
		number1 = (len(Window.name1) * 60) / 8
		self.player1_canva.create_text(number1,30,text=Window.name1,font=('Calibri',20),fill="white")
		# Ajouter un timer
		self.timerPlayer1 = self.player1_canva.create_text(300,30,text=Window.timer1,font=('Calibri',20),fill="white")
		
		self.player1_canva.place(x=700, y=550)

		self.player2_canva = tkinter.Canvas(self.window, width=370, height=120, bg='#312E2B')
		# Ajouter le nom du joueur
		number2 = (len(Window.name2) * 60) / 8
		self.player2_canva.create_text(number2,30,text=Window.name2,font=('Calibri',20),fill="white")
		# Ajouter un timer
		self.timerPlayer2 = self.player2_canva.create_text(300,30,text=Window.timer2,font=('Calibri',20),fill="white")

		self.player2_canva.place(x=700, y=30)

		if Window.letPass:
			self.window.after(1000, self.updateTimer)

	def updateTimer(self):
		# Permet d'afficher le temps écoulé
		Window.letPass = False

		if Window.color_who_plays == "w":
			minutes = Window.timer1
			if minutes == "0:00":
				print("Temps écoulé, les noirs gagnent !")
				Window.checkmate = "fini"

		if Window.color_who_plays == "b":
			minutes = Window.timer2
			if minutes == "0:00":
				print("Temps écoulé, les blancs gagnent !")
				Window.checkmate = "fini"

		if Window.checkmate != "fini":
			minute, secondes = minutes.split(":")
			secondes = str(int(secondes) - 1)
			if int(secondes) == -1:
			    secondes = "59"
			    minute = str(int(minute) - 1)

			if len(secondes) == 1:
			    secondes = "0"+secondes

			minutes = minute+":"+secondes
			if Window.color_who_plays == "w":
				Window.timer1 = minutes
				self.player1_canva.itemconfigure(self.timerPlayer1, text=Window.timer1)

			if Window.color_who_plays == "b":
				Window.timer2 = minutes
				self.player2_canva.itemconfigure(self.timerPlayer2, text=Window.timer2)

			
			self.window.after(1000, self.updateTimer)

	def pieceEaten(self, piece):
		# Enregistre les pièces mangées pour les afficher par la suite
		img = [element for element,name in littlePieces_dict.items() if str(name) == piece]
		img_name = [name for element,name in littlePieces_dict.items() if str(name) == piece]

		if piece[0] == "w":
			self.saveEatenPieceW.append(img_name)

			if piece[1] == "p":
				self.pieceWhiteEaten[0] += 1
				self.player1_canva.create_image(20+(self.pieceWhiteEaten[0]*20), 70, image=img)
			else:
				self.pieceWhiteEaten[1] += 1
				self.player1_canva.create_image(20+(self.pieceWhiteEaten[1]*22), 100, image=img)

			self.player1_canva.update()


		if piece[0] == "b":
			self.saveEatenPieceB.append(img_name)
			if piece[1] == "p":
				self.pieceBlackEaten[0] += 1
				self.player2_canva.create_image(20+(self.pieceBlackEaten[0]*20), 70, image=img)
			else:
				self.pieceBlackEaten[1] += 1
				self.player2_canva.create_image(20+(self.pieceBlackEaten[1]*22), 100, image=img)

			self.player2_canva.update()
		
	def quit(self):
		print("Partie quittée !")
		with open("savedGame.txt", "w") as file:
			file.write("None")
		self.window.destroy()

	def saveGame(self):
		with open("savedGame.txt","w") as file:

			[file.write(str(self.get_image(lelement))+" | ") for element in self.board for lelement in element]
			file.write("\n")
			[file.write(pos+" | ") for pos in self.allPosition]
			file.write("\n")
			file.write(self.timer1+"\n")
			file.write(self.timer2+"\n")
			file.write(self.name1+"\n")
			file.write(self.name2+"\n")
			[file.write(str(pw)+" | ") for pw in self.saveEatenPieceW]
			file.write("\n")
			[file.write(str(pb)+" | ") for pb in self.saveEatenPieceB]
			file.write("\n")
			[file.write(str(pos)+" | ") for pos in Window.old_position]
			file.write("\n")
			file.write(Window.color_who_plays+"\n")
			[file.write(str(x)+" | ") for x in Window.pris_en_passant]
			file.write("\n")
			file.write(str(Window.letPass)+"\n")
			file.write(Window.freeze+"\n")
			file.write(Window.click_backup+"\n")
			[file.write(str(i)+" | ") for i in Window.helpMove]
			file.write("\n")
			file.write(Window.chessColor+"\n")
			file.write(Window.themeColor+"\n")

		print("Partie sauvegardée !")
		self.window.destroy()


	def quitChess(self):
		Window.freeze = Window.checkmate
		Window.checkmate = "fini"
		self.helpButton["state"] = "disabled"
		self.pauseButton["state"] = "disabled"
		
		# On propose de sauvegarder la partie
		self.saveCanva = tkinter.Canvas(self.window, width=500, height=400, bg='#00081B')
		text = "Sauvegarder la partie ?"
		self.saveCanva.create_text(250,50,text=text,font=('Calibri',24),fill="white")
		self.saveCanva.place(x=300,y=100)

		self.saveB = tkinter.Button(self.saveCanva, text="Sauvegarder",command=self.saveGame)
		self.saveB["width"] = 17
		self.saveB["bg"] = '#312E2B'
		self.saveB["fg"] = "white"
		self.saveB["font"] = font.Font(family='Calibri', size=15, weight="bold")
		self.saveB.place(x=170, y=150)

		self.quitB = tkinter.Button(self.saveCanva, text="Quitter",command=self.quit)
		self.quitB["width"] = 17
		self.quitB["bg"] = '#312E2B'
		self.quitB["fg"] = "white"
		self.quitB["font"] = font.Font(family='Calibri', size=15, weight="bold")
		self.quitB.place(x=170, y=250)


	def continueClic(self):
		self.pauseCanvas.destroy()
		Window.checkmate = Window.freeze
		Window.freeze = None
		self.helpButton["state"] = "normal"
		self.quitButton["state"] = "normal"
		self.updateTimer()


	def restart(self):
		for w in self.window.winfo_children():
			if w != self.underCanvas:
				w.destroy()

		Window.timer1 = Window.gameTime
		Window.timer2 = Window.gameTime

		self.chess_board()
		p1 = Pieces(self,False,None)
		self.players_infos()
		self.infos_buttons()
		Window.checkmate = "jeu"
		self.allPosition = []
		self.helpButton["state"] = "normal"
		self.quitButton["state"] = "normal"
		self.games_infos()
		self.updateTimer()

		Window.img_saved = None
		Window.old_position = []
		Window.color_who_plays = "w"
		Window.pris_en_passant = []
		Window.letPass = True

	def pauseGame(self):
		Window.freeze = Window.checkmate
		Window.checkmate = "fini"
		self.helpButton["state"] = "disabled"
		self.quitButton["state"] = "disabled"
		self.pauseCanvas = tkinter.Canvas(self.window, width=500, height=400, bg='#00081B')
		self.pauseCanvas.place(x=300, y=100)
		txt = "Partie mise en pause"
		self.pauseCanvas.create_text(250,50,text=txt,font=('Calibri',24),fill="white")

		# Bouton reprendre
		self.continueButton = tkinter.Button(self.pauseCanvas, text="Reprendre",command=self.continueClic)
		self.continueButton["width"] = 12
		self.continueButton["bg"] = '#312E2B'
		self.continueButton["fg"] = "white"
		self.continueButton["font"] = font.Font(family='Calibri', size=18, weight="bold")
		self.continueButton.place(x=170, y=150)

		# Bouton reprendre
		self.restartButton = tkinter.Button(self.pauseCanvas, text="Recommencer",command=self.restart)
		self.restartButton["width"] = 12
		self.restartButton["bg"] = '#312E2B'
		self.restartButton["fg"] = "white"
		self.restartButton["font"] = font.Font(family='Calibri', size=18, weight="bold")
		self.restartButton.place(x=170, y=250)


	def infos_buttons(self):
		# Affichage des boutons
		# On crée la zone qui va contenir les boutons
		self.button_canva = tkinter.Canvas(self.window, width=370, height=50, bg='#00081B')
		self.button_canva.place(x=700, y=472)

		# On crée le bouton 'quitter'
		self.quitButton = tkinter.Button(self.button_canva, text="Quitter", command=self.quitChess)
		self.quitButton["width"] = 12
		self.quitButton["bg"] = '#312E2B'
		self.quitButton["fg"] = "white"
		self.quitButton["font"] = font.Font(family='Calibri', size=15, weight="bold")
		self.quitButton.place(x=240, y=7)

		# On crée le bouton aide
		self.helpButton = tkinter.Button(self.button_canva, text="Aide",command=self.showHelp)
		self.helpButton["width"] = 12
		self.helpButton["bg"] = '#312E2B'
		self.helpButton["fg"] = "white"
		self.helpButton["font"] = font.Font(family='Calibri', size=15, weight="bold")
		self.helpButton.place(x=5, y=7)

		# On crée le bouton pause
		self.pauseButton = tkinter.Button(self.button_canva, text="Pause",command=self.pauseGame)
		self.pauseButton["width"] = 8
		self.pauseButton["bg"] = '#312E2B'
		self.pauseButton["fg"] = "white"
		self.pauseButton["font"] = font.Font(family='Calibri', size=14, weight="bold")
		self.pauseButton.place(x=142, y=7)


class Pieces:

	def __init__(self, window, oldGame, oldBoard):
		# On place les pièces
		if oldGame == True:

			countAll = 0
			for x in range(0, 8):
				for y in range(0,8):
					element = oldBoard[countAll].split(",")[1][1:-1]
					if element != "[]":
						img = [elementD for elementD,name in pieces_dict.items() if name == element[2:-2]]
						window.board[x][y].create_image(42, 40, image=img, tag="get_image")			            

					countAll += 1

		else:
			# Placement des pièces blanches
			[window.board[6][x].create_image(42, 40, image=WHITE_PAWN, tag="get_image")\
			 	for x in range(8)]
			window.board[7][0].create_image(42, 40, image=WHITE_ROCK, tag="get_image")
			window.board[7][7].create_image(42, 40, image=WHITE_ROCK, tag="get_image")
			window.board[7][1].create_image(42, 40, image=WHITE_BISHOP, tag="get_image")
			window.board[7][6].create_image(42, 40, image=WHITE_BISHOP, tag="get_image")
			window.board[7][2].create_image(42, 40, image=WHITE_KNIGHT, tag="get_image")
			window.board[7][5].create_image(42, 40, image=WHITE_KNIGHT, tag="get_image")
			window.board[7][4].create_image(42, 40, image=WHITE_KING, tag="get_image")
			window.board[7][3].create_image(42, 40, image=WHITE_QUEEN, tag="get_image")

			# Placement des pièces noires
			[window.board[1][x].create_image(42, 40, image=BLACK_PAWN, tag="get_image")\
				for x in range(8)]
			window.board[0][0].create_image(42, 40, image=BLACK_ROCK, tag="get_image")
			window.board[0][7].create_image(42, 40, image=BLACK_ROCK, tag="get_image")
			window.board[0][1].create_image(42, 40, image=BLACK_BISHOP, tag="get_image")
			window.board[0][6].create_image(42, 40, image=BLACK_BISHOP, tag="get_image")
			window.board[0][2].create_image(42, 40, image=BLACK_KNIGHT, tag="get_image")
			window.board[0][5].create_image(42, 40, image=BLACK_KNIGHT, tag="get_image")
			window.board[0][4].create_image(42, 40, image=BLACK_KING, tag="get_image")
			window.board[0][3].create_image(42, 40, image=BLACK_QUEEN, tag="get_image")

	
	def test(self, window):
		# Permet de tester une situation de jeu en placant les pièces comme on veut
		window.board[3][2].create_image(42, 40, image=WHITE_KING, tag="get_image")
		window.board[1][7].create_image(42, 40, image=WHITE_QUEEN, tag="get_image")
		window.board[0][0].create_image(42, 40, image=BLACK_KING, tag="get_image")
		window.board[1][5].create_image(42, 40, image=WHITE_PAWN, tag="get_image")


# ----------------------------- CODE PRINCIPAL -----------------------------------#

def ready_createImage():
	global WHITE_PAWN
	global WHITE_ROCK
	global WHITE_BISHOP
	global WHITE_KNIGHT
	global WHITE_KING
	global WHITE_QUEEN

	global BLACK_PAWN
	global BLACK_ROCK
	global BLACK_BISHOP
	global BLACK_KNIGHT
	global BLACK_KING
	global BLACK_QUEEN

	# Chargement des images des pièces 
	WHITE_PAWN = tkinter.PhotoImage(file="image_pieces/w_pawn.png")
	WHITE_ROCK = tkinter.PhotoImage(file="image_pieces/w_rock.png")
	WHITE_BISHOP = tkinter.PhotoImage(file="image_pieces/w_bishop.png")
	WHITE_KNIGHT = tkinter.PhotoImage(file="image_pieces/w_knight.png")
	WHITE_KING = tkinter.PhotoImage(file="image_pieces/w_king.png")
	WHITE_QUEEN = tkinter.PhotoImage(file="image_pieces/w_queen.png")

	BLACK_PAWN = tkinter.PhotoImage(file="image_pieces/b_pawn.png")
	BLACK_ROCK = tkinter.PhotoImage(file="image_pieces/b_rock.png")
	BLACK_BISHOP = tkinter.PhotoImage(file="image_pieces/b_bishop.png")
	BLACK_KNIGHT = tkinter.PhotoImage(file="image_pieces/b_knight.png")
	BLACK_KING = tkinter.PhotoImage(file="image_pieces/b_king.png")
	BLACK_QUEEN = tkinter.PhotoImage(file="image_pieces/b_queen.png")

	global white_pawn
	global white_rock
	global white_bishop
	global white_knight
	global white_king
	global white_queen

	global black_pawn
	global black_rock
	global black_bishop
	global black_knight
	global black_king
	global black_queen

	white_pawn = tkinter.PhotoImage(file="image_retrecie/w_pawn.png")
	white_rock = tkinter.PhotoImage(file="image_retrecie/w_rock.png")
	white_bishop = tkinter.PhotoImage(file="image_retrecie/w_bishop.png")
	white_knight = tkinter.PhotoImage(file="image_retrecie/w_knight.png")
	white_king = tkinter.PhotoImage(file="image_retrecie/w_king.png")
	white_queen = tkinter.PhotoImage(file="image_retrecie/w_queen.png")

	black_pawn = tkinter.PhotoImage(file="image_retrecie/b_pawn.png")
	black_rock = tkinter.PhotoImage(file="image_retrecie/b_rock.png")
	black_bishop = tkinter.PhotoImage(file="image_retrecie/b_bishop.png")
	black_knight = tkinter.PhotoImage(file="image_retrecie/b_knight.png")
	black_king = tkinter.PhotoImage(file="image_retrecie/b_king.png")
	black_queen = tkinter.PhotoImage(file="image_retrecie/b_queen.png")

	global pieces_dict
	global littlePieces_dict
	global vrai_nom

	# Dictionnaire qui va nous permettre d'utiliser les images par la suite
	pieces_dict = {WHITE_PAWN:"wp",WHITE_ROCK:"wr",WHITE_BISHOP:"wb",WHITE_KNIGHT:"wk",\
					WHITE_KING:"wK",WHITE_QUEEN:"wQ",BLACK_PAWN:"bp",BLACK_ROCK:"br",\
					BLACK_BISHOP:"bb",BLACK_KNIGHT:"bk",BLACK_KING:"bK",BLACK_QUEEN:"bQ"}

	littlePieces_dict = {white_pawn:"wp",white_rock:"wr",white_bishop:"wb",white_knight:"wk",\
						white_king:"wK",white_queen:"wQ",black_pawn:"bp",black_rock:"br",\
						black_bishop:"bb",black_knight:"bk",black_king:"bK",black_queen:"bQ"}

	vrai_nom = {"Pion blanc":"wp","Tour blanche":"wr","Cheval blanc":"wb","Cavalier blanc":"wk",\
				"Roi blanc":"wK","Reine blanche":"wQ","Pion noir":"bp","Tour noire":"br",\
				"Cheval noir":"bb","Cavalier noir":"bk","Roi noir":"bK","Reine noire":"bQ"}
