"""
			JEU D'ECHEC - Ayanleh - Dec.2021

Ce fichier gère tout ce qui concerne la fenêtre affichant 
   le menu principal

"""

import tkinter
from tkinter import font as font
import random

class MainMenu:

	def __init__(self, window):
		self.window = window
		self.controlVar = tkinter.StringVar(value="1")
		self.exitProgram = False
		self.oldGame = False
		self.filesImg = []
		self.otherInfos = []
		name_pieces = ["king","queen","bishop","knight","rock"]

		for x in name_pieces:
			self.filesImg.append(tkinter.PhotoImage(file="image_pieces/w_"+x+".png"))
			self.filesImg.append(tkinter.PhotoImage(file="image_pieces/b_"+x+".png"))

		height = lambda : random.randint(36,1069)
		width = lambda : random.randint(36,669)
		self.canvas = tkinter.Canvas(self.window, width=1100, height=700, bg='#F3ECE3')
		self.images = dict()

		for i in self.filesImg:
			imgcanva = self.canvas.create_image(height(), width(), image=i, tag="img1")
			self.images[imgcanva] = [random.choice([1,-1]),random.choice([1,-1])]

		self.canvas.place(x=0,y=0)
		self.window.update()
		self.window.after(1000, self.movePictures)


	def movePictures(self):
		# Bouge les pièces dans le fond
		for k,v in self.images.items():

			if self.canvas.coords(k)[0] < 36:
				self.images[k][0] = 1

			if self.canvas.coords(k)[1] < 36:
				self.images[k][1] = 1

			if self.canvas.coords(k)[0] > 1069:
				self.images[k][0] = -1

			if self.canvas.coords(k)[1] > 669:
				self.images[k][1] = -1

			self.canvas.move(k,self.images[k][0],self.images[k][1])

		self.ID = self.window.after(10, self.movePictures)


	def mainCanvas(self):
		# On crée le canvas du milieu en gris
		self.mainCanva = tkinter.Canvas(self.window, width=650, height=450, bg='#312E2B')
		self.mainCanva.place(x=230,y=120)

		# On affiche le titre
		self.mainCanva.create_text(324,60,text="Jeu d'échecs",font=('Calibri',38),fill="white")

		# On crée le bouton qui permet de lancer la partie
		self.play = tkinter.Button(self.mainCanva, text="Jouer", command=self.playClic)
		self.play["width"] = 17
		self.play["bg"] = '#6E4A1C'
		self.play["fg"] = "white"
		self.play["font"] = font.Font(family='Calibri', size=22, weight="bold")
		self.play.place(x=190, y=130)

		# On crée le bouton d'options
		self.play = tkinter.Button(self.mainCanva, text="Options", command=self.settingsClic)
		self.play["width"] = 17
		self.play["bg"] = '#6E4A1C'
		self.play["fg"] = "white"
		self.play["font"] = font.Font(family='Calibri', size=22, weight="bold")
		self.play.place(x=190, y=230)

		# On crée le bouton qui permet de quitter
		self.play = tkinter.Button(self.mainCanva, text="Quitter", command=self.quitClic)
		self.play["width"] = 17
		self.play["bg"] = '#6E4A1C'
		self.play["fg"] = "white"
		self.play["font"] = font.Font(family='Calibri', size=22, weight="bold")
		self.play.place(x=190, y=330)


	def beginGame(self):
		# On récupère le nom des joueurs
		if self.namePlayer1.get() == "":
			name1 = "Joueur 1"
		else:
			name1 = self.namePlayer1.get()

		if self.namePlayer2.get() == "":
			name2 = "Joueur 2"
		else:
			name2 = self.namePlayer2.get()

		if self.controlVar2.get() == "":
			timeGame = "10"
		else:
			timeGame = self.controlVar2.get()

		# On récupère la couleur du thème
		themeGame = self.canvas["bg"]

		# On récupère la couleur de l'échiquier
		try:
			self.variable.get() == ""

		except AttributeError:
			chessColor = "Vert"

		else:
			chessColor = self.variable.get()


		self.name1 = name1
		self.name2 = name2
		self.timeGame = timeGame
		self.themeGame = themeGame
		self.chessColor = chessColor

		self.window.after_cancel(self.ID)
		self.window.destroy()


	def beginOldGame(self):
		# On charge les infos de la partie précedente
		with open("savedGame.txt","r") as file:
		    liste = [line.split(" | ") for line in file]

		for x in [0, 1, 6, 7,8, 10,14]:
		    liste[x].pop(-1)

		for y in [2,3,4,5,9,11,12,13,15,16]:
		    liste[y] = liste[y][0].replace("\n","")

		self.name1 = liste[4]
		self.name2 = liste[5]
		self.timeGame = [liste[2],liste[3]]
		self.themeGame = liste[16]
		self.chessColor = liste[15]
		self.chessBoard = liste[0]
		self.allPosition = liste[1]
		self.eatW = liste[6]
		self.eatB = liste[7]
		colorp = liste[9]
		freeze = liste[12]
		prise = liste[10]
		old_pos = liste[8]
		letPass = liste[11]
		click = liste[13]
		helpMove = liste[14]
		self.oldGame = True
		self.otherInfos = [colorp,freeze,prise,old_pos,letPass,click,helpMove]

		self.window.after_cancel(self.ID)
		self.window.destroy()


	def playClic(self):
		# On efface les boutons
		for w in self.mainCanva.winfo_children():
			w.destroy()

		# Message indiquant d'entrer des noms
		text = self.mainCanva.create_text(185,140,text="Nom du joueur 1",font=('Calibri',20),fill="white")
		text2 = self.mainCanva.create_text(185,280,text="Nom du joueur 2",font=('Calibri',20),fill="white")

		# Saisie des noms des joueurs
		self.namePlayer1 = tkinter.StringVar()
		entryName1 = tkinter.Entry(self.mainCanva, width=20,textvariable=self.namePlayer1)
		entryName1["font"] = ("Calibri", 20)
		entryName1["bg"] = "#A7B39D"
		entryName1.place(x=50,y=170)

		self.namePlayer2 = tkinter.StringVar()
		entryName2 = tkinter.Entry(self.mainCanva, width=20,textvariable=self.namePlayer2)
		entryName2["font"] = ("Calibri", 20)
		entryName2["bg"] = "#A7B39D"
		entryName2.place(x=50,y=310)

		# Entrée du temps de la partie
		msg = "Temps de la partie"
		timeText = self.mainCanva.create_text(500, 120, text=msg,font=('Calibri',20),fill="white")
		self.controlVar2 = tkinter.StringVar()

		# Bouton 1 min
		self.radio_widget2 = tkinter.Radiobutton(self.mainCanva,text="1 min",font=('Calibri',20),value=1)
		self.radio_widget2["width"] = 10
		self.radio_widget2["bg"] = '#A7B39D'
		self.radio_widget2["indicatoron"] = False
		self.radio_widget2["selectcolor"] = "#F3ECE3"
		self.radio_widget2["variable"] = self.controlVar2		
		self.radio_widget2.place(x=425,y=150)

		# Bouton 3 min
		self.radio_widget2 = tkinter.Radiobutton(self.mainCanva,text="3 min",font=('Calibri',20),value=3)
		self.radio_widget2["width"] = 10
		self.radio_widget2["bg"] = '#A7B39D'
		self.radio_widget2["indicatoron"] = False
		self.radio_widget2["selectcolor"] = "#F3ECE3"
		self.radio_widget2["variable"] = self.controlVar2		
		self.radio_widget2.place(x=425,y=230)

		# Bouton 10 min
		self.radio_widget2 = tkinter.Radiobutton(self.mainCanva,text="10 min",font=('Calibri',20),value=10)
		self.radio_widget2["width"] = 10
		self.radio_widget2["bg"] = '#A7B39D'
		self.radio_widget2["indicatoron"] = False
		self.radio_widget2["selectcolor"] = "#F3ECE3"
		self.radio_widget2["variable"] = self.controlVar2		
		self.radio_widget2.place(x=425,y=310)

		# Bouton jouer
		playButton = tkinter.Button(self.mainCanva,text="Jouer",command=self.beginGame)
		playButton["font"] = ('Calibri',14)
		playButton["width"] = 12
		playButton["bg"] = '#6E4A1C'
		playButton["fg"] = "white"

		playButton.place(x=480,y=390)

		# Bouton reprendre partie
		playBackButton = tkinter.Button(self.mainCanva,text="Reprendre partie",command=self.beginOldGame)
		playBackButton["font"] = ('Calibri',14)
		playBackButton["width"] = 17
		playBackButton["bg"] = '#6E4A1C'
		playBackButton["fg"] = "white"

		with open("savedGame.txt","r") as file:
			if file.readlines()[0] == "None":
				playBackButton["state"] = "disabled"

		playBackButton.place(x=233,y=390)

		# Bouton retour
		backButton = tkinter.Button(self.mainCanva,text="Retour",command=self.backToMain)
		backButton["font"] = ('Calibri',14)
		backButton["width"] = 12
		backButton["bg"] = '#6E4A1C'
		backButton["fg"] = "white"

		backButton.place(x=40,y=390)

	def quitClic(self):
		self.exitProgram = True
		for x in self.window.winfo_children():
			x.destroy()
			
		self.window.after_cancel(self.ID)
		self.window.destroy()

	
	def change_chessColor(self,*args):
		self.colorChessImg = tkinter.PhotoImage(file="couleur_echiquier/"+self.variable.get()+".png")
		self.mainCanva.itemconfigure(self.imgShown, image=self.colorChessImg)

	
	def changeThemeColor(self):
		if self.controlVar.get() == "1":
			self.canvas["bg"] = "#F3ECE3"

		elif self.controlVar.get() == "0":
			self.canvas["bg"] = "#8F908E"

		self.canvas.update()


	def backToMain(self):
		# On efface les boutons
		for w in self.mainCanva.winfo_children():
			w.destroy()

		#self.mainCanva.destroy()
		self.mainCanvas()


	def settingsClic(self):
		# On efface les boutons
		for w in self.mainCanva.winfo_children():
			w.destroy()

		# Changement couleur de l'échiquier
		self.settingsText1 = self.mainCanva.create_text(150,160,text="Echiquier",font=('Calibri',26),fill="#9DB3B2")
		
		# Menu déroulant
		colors = ["Vert","Bleu","Brun"]
		try:
			self.variable = self.variable
		except AttributeError:
			self.variable = tkinter.StringVar(self.mainCanva)
			self.variable.set(colors[0])	

		
		opt = tkinter.OptionMenu(self.mainCanva, self.variable, *colors)
		opt.config(width=12, font=('Calibri', 12), bg="#A7B39D")
		opt.place(x=270, y=146)
		self.variable.trace("w", self.change_chessColor)


		# Image liée au menu déroulant
		self.colorChessImg = tkinter.PhotoImage(file="couleur_echiquier/"+self.variable.get()+".png")
		self.imgShown = self.mainCanva.create_image(530, 160, image=self.colorChessImg)

		# Theme de la partie
		self.controlVar = tkinter.StringVar()
		self.settingsText2 = self.mainCanva.create_text(150,300,text="Thème",font=('Calibri',26),fill="#9DB3B2")
		
		# Bouton <clair>
		self.radio_widget = tkinter.Radiobutton(self.mainCanva,text="Clair",font=('Calibri',20),value=1)
		self.radio_widget["width"] = 10
		self.radio_widget["bg"] = '#A7B39D'
		self.radio_widget["indicatoron"] = False
		self.radio_widget["selectcolor"] = "#F3ECE3"
		self.radio_widget["command"] = self.changeThemeColor
		self.radio_widget["variable"] = self.controlVar
		self.radio_widget.place(x=230,y=280)

		# Bouton <sombre>
		self.radio_widget2 = tkinter.Radiobutton(self.mainCanva,text="Sombre",font=('Calibri',20),value=0)
		self.radio_widget2["width"] = 10
		self.radio_widget2["bg"] = '#A7B39D'
		self.radio_widget2["indicatoron"] = False
		self.radio_widget2["selectcolor"] = "#8F908E"
		self.radio_widget2["command"] = self.changeThemeColor
		self.radio_widget2["variable"] = self.controlVar		
		self.radio_widget2.place(x=450,y=280)

		# Bouton pour revenir au menu principal
		backButton = tkinter.Button(self.mainCanva,text="Retour",command=self.backToMain)
		backButton["font"] = ('Calibri',14)
		backButton["width"] = 17
		backButton["bg"] = '#6E4A1C'
		backButton["fg"] = "white"

		backButton.place(x=40,y=380)
