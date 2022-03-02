"""
			JEU D'ECHEC - Ayanleh - Dec.2021
			
Ce fichier gère tout ce qui concerne les règles des échecs

"""

def which_piece(img_name, self_obj, pos, old_pos, checkmate=0):
	# Permet de savoir de quel type de pièce il s'agit
	# Et va appeler la fonction qui correspond au type de la pièce
	
	pieces = img_name[0][-1]
	color = img_name[0][0]

	if pieces == "p":
		return pawn(self_obj, pos, old_pos, color, checkmate)
	elif pieces == "b":
		return bishop(self_obj, pos, old_pos, color, checkmate)
	elif pieces == "r":
		return rock(self_obj, pos, old_pos, color, checkmate)
	elif pieces == "k":
		return knight(self_obj, pos, old_pos, checkmate)
	elif pieces == "K":
		return king(self_obj, pos, old_pos, color, checkmate)
	elif pieces == "Q":
		return queen(self_obj, pos, old_pos, checkmate)

	# Toutes ces fonctions permettent de savoir si le déplacement
	# tenté est valide

def king(self_obj, pos, old_pos, color, checkmate):
	# on verifie si le déplacement du roi est valide
	x_pos, y_pos = pos
	x_old, y_old = old_pos

	if x_pos == x_old:
		if abs(y_pos-y_old) == 1:
			return horizontal_shift(self_obj, pos, old_pos, checkmate)
		else:
			return False

	if y_pos == y_old:
		if abs(x_pos-x_old) == 1:
			return vertical_shift(self_obj, pos, old_pos, checkmate)
		else:
			return False

	if abs(x_pos-x_old) == abs(y_pos-y_old):
		if abs(x_pos-x_old) == 1 or abs(y_pos-y_old) == 1:
			return other_shift(self_obj, pos, old_pos, checkmate)
		else:
			return False

def queen(self_obj, pos, old_pos, checkmate):
	# On verifie si le daplcement de la reine est valide
	x_pos, y_pos = pos
	x_old, y_old = old_pos

	if x_pos == x_old:
		return horizontal_shift(self_obj, pos, old_pos, checkmate)
	if y_pos == y_old:
		return vertical_shift(self_obj, pos, old_pos, checkmate)
	if abs(x_pos-x_old) == abs(y_pos-y_old):
		return other_shift(self_obj, pos, old_pos, checkmate)


def bishop(self_obj, pos, old_pos, color, checkmate):
	# On verifie si le déplacement du cheval est valide
	x_pos, y_pos = pos
	x_old, y_old = old_pos
	
	if x_pos == x_old + 2 and y_pos == y_old + 1:
		if self_obj.get_image(self_obj.board[x_old + 2][y_old + 1])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True

	if x_pos == x_old + 1 and y_pos == y_old + 2:
		if self_obj.get_image(self_obj.board[x_old + 1][y_old + 2])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True

	if x_pos == x_old - 1 and y_pos == y_old + 2:
		if self_obj.get_image(self_obj.board[x_old - 1][y_old + 2])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True

	if x_pos == x_old + 1 and y_pos == y_old - 2:
		if self_obj.get_image(self_obj.board[x_old + 1][y_old - 2])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True

	if x_pos == x_old - 1 and y_pos == y_old - 2:
		if self_obj.get_image(self_obj.board[x_old - 1][y_old - 2])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True

	if x_pos == x_old - 2 and y_pos == y_old - 1:
		if self_obj.get_image(self_obj.board[x_old - 2][y_old - 1])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True

	if x_pos == x_old - 2 and y_pos == y_old + 1:
		if self_obj.get_image(self_obj.board[x_old - 2][y_old + 1])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True

	if x_pos == x_old + 2 and y_pos == y_old - 1:
		if self_obj.get_image(self_obj.board[x_old + 2][y_old - 1])[0] != "":
			return eat_piece(self_obj, pos, old_pos, checkmate)
		return True
	
	return False

def rock(self_obj, pos, old_pos, color, checkmate):
	# On verifie si le déplacement de la tour est valide
	x_pos, y_pos = pos
	x_old, y_old = old_pos

	if color == "w" and y_pos == y_old:
		return vertical_shift(self_obj ,pos, old_pos, checkmate)

	if color == "w" and x_pos == x_old:
		return horizontal_shift(self_obj ,pos, old_pos, checkmate)

	if color == "b" and y_pos == y_old:
		pos_temporary = [pos[0]+1, pos[1]]
		old_pos_temporary = [old_pos[0]+1, old_pos[1]]
		return vertical_shift(self_obj ,pos, old_pos, checkmate)

	if color == "b" and x_pos == x_old:
		pos_temporary = [pos[0]+1, pos[1]]
		old_pos_temporary = [old_pos[0]+1, old_pos[1]]
		return horizontal_shift(self_obj ,pos, old_pos, checkmate)

	return False


def knight(self_obj, pos, old_pos, checkmate):
	# On vérifie si le déplacement du cavalier est valide
	return other_shift(self_obj, pos, old_pos, checkmate)


def pawn(self_obj, pos, old_pos, color, checkmate):
	# On vérifie si le déplacement du pion est valide
	board = self_obj.board
	x_pos, y_pos = pos
	x_old, y_old = old_pos
	img = self_obj.get_image(board[x_old][y_old])[0]

	# On autorise qu'un déplacement d'une case
	if color == "w": # vers l'avant pour les blancs


		if x_old == 1 and check_is_empty(self_obj, pos):
			# promotion du pion blanc
			if testBoard(self_obj, board, img, old_pos, pos, mode=1):
				x = board[x_old][y_old].winfo_rootx()
				y = board[x_old][y_old].winfo_rooty()
				img_name = self_obj.get_image(board[x_old][y_old])[1][0]
				self_obj.promotion(x,y, [x_old,y_old], pos, "w")
				self_obj.allPosition.append("------PROMOTION---------")
				pieceMoved = ">  "+img_name+" : "+str([x_old,y_old])+" -> "+str([x_pos,y_pos])
				self_obj.allPosition.append(pieceMoved)
				self_obj.games_infos()
				return False
				
		# Règle du pris en passant 
		if self_obj.getPassant() != [] and checkmate == 0:
			if self_obj.getPassant()[2] != "w":
				x_bp, y_bp = self_obj.getPassant()[1]
				if (x_old == x_bp) and abs(y_bp - y_old) == 1:
					if y_pos == y_bp and x_pos == x_bp - 1:
						pieceEaten = self_obj.get_image(board[x_bp][y_bp])[1][0]
						self_obj.setPassant([])
						self_obj.board[x_bp][y_bp].delete("all")
						self_obj.pieceEaten(pieceEaten)

						return True 

			self_obj.setPassant([])

		if x_old == (x_pos + 1) and y_old == y_pos + 1:
			if check_is_empty(self_obj, pos) == False:
				return eat_piece(self_obj, pos, old_pos, checkmate)
				
		# On regarde si les conditions pour manger une pièce sont réunies
		elif x_old == (x_pos + 1) and y_old == y_pos - 1:
			if check_is_empty(self_obj, pos) == False:
				return eat_piece(self_obj, pos, old_pos, checkmate)
		
		if x_old == (x_pos + 1) and y_old == y_pos:
			if check_is_empty(self_obj, pos) and vertical_shift(self_obj ,pos, old_pos, checkmate):
				return True # On vérifie qu'il n'y a pas de pion sur la case
		elif x_old == 6 and x_old == x_pos + 2 and y_old == y_pos:
			if check_is_empty(self_obj, pos) and vertical_shift(self_obj ,pos, old_pos, checkmate):
				self_obj.setPassant([1, pos, "w"])
				return True # un pion peut se déplacer sur 2 cases au début


	if color == "b": # vers l'arrière pour les noirs

		if x_old == 6 and check_is_empty(self_obj, pos):
			# promotion du pion noir
			if testBoard(self_obj, board, img, old_pos, pos, mode=1):
				x = board[x_old][y_old].winfo_rootx()
				y = board[x_old][y_old].winfo_rooty()
				img_name = self_obj.get_image(board[x_old][y_old])[1][0]
				self_obj.promotion(x,y, [x_old,y_old], pos, "b")
				self_obj.allPosition.append("------PROMOTION---------")
				pieceMoved = ">  "+img_name+" : "+str([x_old,y_old])+" -> "+str([x_pos,y_pos])
				self_obj.allPosition.append(pieceMoved)
				self_obj.games_infos()
				return False

		# Règle du pris en passant
		if self_obj.getPassant() != [] and checkmate == 0:
			if self_obj.getPassant()[2] != "b":
				x_wp, y_wp = self_obj.getPassant()[1]
				if (x_old == x_wp) and abs(y_wp - y_old) == 1:
					if y_pos == y_wp and x_pos == x_wp + 1:
						pieceEaten = self_obj.get_image(board[x_wp][y_wp])[1][0]
						self_obj.setPassant([])
						self_obj.board[x_wp][y_wp].delete("all")
						self_obj.pieceEaten(pieceEaten)
						
						return True

			self_obj.setPassant([])
		
		if x_old == (x_pos - 1) and y_old == y_pos + 1:
			if check_is_empty(self_obj, pos) == False:
				return eat_piece(self_obj, pos, old_pos, checkmate)
				
		# On regarde si les conditions pour manger une pièce sont réunies
		elif x_old == (x_pos - 1) and y_old == y_pos - 1:
			if check_is_empty(self_obj, pos) == False:
				return eat_piece(self_obj, pos, old_pos, checkmate)
		
		if x_old == x_pos - 1 and y_old == y_pos:
			if check_is_empty(self_obj, pos) and vertical_shift(self_obj ,pos, old_pos, checkmate):
				return True
		elif x_old == 1 and x_old == x_pos - 2 and y_old == y_pos:
			if check_is_empty(self_obj, pos) and vertical_shift(self_obj ,pos, old_pos, checkmate):
				self_obj.setPassant([1, pos, "b"])
				return True

	return False
	
def vertical_shift(self_obj, pos, old_pos, checkmate):
	# On vérifie si le déplacement sur le haut/bas est possible
	x_pos, y_pos = pos
	x_old, y_old = old_pos
	count_max = abs(x_old - x_pos)

	for x in range(1, count_max):
		# Si il y a une case sur son chemin on retourne False
		if x_pos < x_old: # on vérifie les cases du haut
			x_coord = x_old - x
		elif x_pos > x_old: # on vérifie les cases du bas
			x_coord = x_old + x


		if self_obj.get_image(self_obj.board[x_coord][y_pos])[0] != "":
			return False

	if check_is_empty(self_obj, pos) == False:
		return eat_piece(self_obj, pos, old_pos, checkmate)
		
	return True # Sinon le déplacement est valide


def horizontal_shift(self_obj, pos, old_pos, checkmate):
	# On vérifie si le déplacement de les côtés est possible
	x_pos, y_pos = pos
	x_old, y_old = old_pos
	count_max = abs(y_old - y_pos)


	for y in range(1, count_max):
		# Si il y a une case sur son chemin on retourne False
		if y_pos < y_old: # on vérifie les cases de gauche
			y_coord = y_old - y
		elif y_pos > y_old:# On vérifie les cases de droite
			y_coord = y_old + y

		if self_obj.get_image(self_obj.board[x_pos][y_coord])[0] != "":
			return False

	if check_is_empty(self_obj, pos) == False:
		return eat_piece(self_obj, pos, old_pos, checkmate)
		
	return True # Sinon le déplacement est valide

def other_shift(self_obj, pos, old_pos, checkmate):
	#On vérifie si le déplacement sur la diagonale est possible
	x_pos, y_pos = pos
	x_old, y_old = old_pos

	count_max = abs(x_old - x_pos)-1

	if abs(x_old - x_pos) == 1 and abs(y_old - y_pos) == 1:
		if check_is_empty(self_obj, pos) == True:
			return True
		else:
			return eat_piece(self_obj, pos, old_pos, checkmate)

	if abs(x_pos - x_old) != 0 and abs(y_pos - y_old) != 0:
		if abs(x_pos - x_old) / abs(y_pos - y_old) == 1:

			for x in range(1, count_max+1):
				if x_old > x_pos:
					if (x_old - x_pos) == (y_old - y_pos):
						# haut gauche
						if self_obj.get_image(self_obj.board[x_old-x][y_old-x])[0] != "":
							return False
							
					if (x_old - x_pos) == -(y_old - y_pos) or -(x_old - x_pos) == (y_old - y_pos):
						# haut droite
						if self_obj.get_image(self_obj.board[x_old-x][y_old+x])[0] != "":
							return False
							

				if x_old < x_pos:
					if (x_old - x_pos) == (y_old - y_pos):
						# bas droite
						if self_obj.get_image(self_obj.board[x_old+x][y_old+x])[0] != "":
							return False
							
					if (x_old - x_pos) == -(y_old - y_pos) or -(x_old - x_pos) == (y_old - y_pos):
						 # bas gauche
						if self_obj.get_image(self_obj.board[x_old+x][y_old-x])[0] != "":
							return False

			return True
		
	return False

def checkmate(self_obj, board):
	# On vérifie si il y a un échec
	for x in range(0,8):
		for y in range(0,8):
			if self_obj.get_image(board[x][y])[0] != "": 
				if self_obj.get_image(board[x][y])[1][0] == "bK":
					bk = [x, y]

				if self_obj.get_image(board[x][y])[1][0] == "wK":
					wk = [x, y]

	for x in range(0,8):
		for y in range(0,8):
			if self_obj.get_image(board[x][y])[0] != "": 

				if self_obj.get_image(board[x][y])[1][0][0] == "w":

					img_name = self_obj.get_image(board[x][y])[1][0]
					if which_piece([img_name], self_obj, bk, [x, y], checkmate=1) == True:
						# Le déplacement d'une pièce entraine un echec sur le roi noir
						return ["b", bk, [x,y]]


				if self_obj.get_image(board[x][y])[1][0][0] == "b":

					img_name = self_obj.get_image(board[x][y])[1][0]
					if which_piece([img_name], self_obj, wk, [x, y], checkmate=1) == True:
						# Le déplacement d'une pièce entraine un echec sur le roi blanc
						return ["w", wk, [x,y]]

	return None



def eat_piece(self_obj, pos, old_pos, checkmate):
	# Fonction permettant de manger une piece en se déplaçant
	x_pos, y_pos = pos
	x_old, y_old = old_pos

	if check_is_empty(self_obj, pos) == True:
		return False

	piece_color = self_obj.get_image(self_obj.board[x_pos][y_pos])[1][0][0]
	pieceEaten = self_obj.get_image(self_obj.board[x_pos][y_pos])[1][0]
	piece_color2 = self_obj.get_image(self_obj.board[x_old][y_old])[1][0][0]

	if piece_color[0] != piece_color2[0]:
		if checkmate != 1:
			self_obj.del_image(x_pos, y_pos, no_clear=0)
			self_obj.pieceEaten(pieceEaten)

		return True

	elif (x_pos == x_old) and (y_pos == y_old) and \
		(piece_color[0] != piece_color2[0]):

		if checkmate != 1:
			self_obj.del_image(x_pos, y_pos, no_clear=0)
			self_obj.pieceEaten(pieceEaten)

		return True

	else:
		return False


def check_is_empty(self_obj, pos):
	# Verifie que la case indiquée est vide
	x_pos, y_pos = pos
	if self_obj.get_image(self_obj.board[x_pos][y_pos])[0] == "":
		return True
	else:
		return False

def testBoard(self_obj, board, img, old_pos, pos, mode=0):
	# teste si lorsque la pièce se déplace il y a échec
	x_old, y_old = old_pos
	x_new, y_new = pos
	condition = 0
	changeColor = 0
	piece_color = self_obj.get_image(board[x_old][y_old])[1]

	if check_is_empty(self_obj, pos) == False:
		# remettre la piece mange apres
		condition = 1
		if piece_color[0][0] == self_obj.get_image(board[x_new][y_new])[1][0][0]:
			return False
		img_piece_eaten = self_obj.get_image(board[x_new][y_new])[0]
		board[x_new][y_new].delete("all")
	
	board[x_new][y_new].create_image(42, 40, image=img,\
		tag="get_image")

	board[x_old][y_old].delete("all")

	if checkmate(self_obj, board) != None:

		if piece_color[0][0] != checkmate(self_obj, board)[0] \
				and piece_color[0][1] != "K" and mode == 1:
			board[x_old][y_old].create_image(42, 40, image=img,\
			tag="get_image")

			board[x_new][y_new].delete("all")

			if condition == 1:
				board[x_new][y_new].create_image(42, 40, image=img_piece_eaten,\
					tag="get_image")

			return True

		
		if piece_color[0][0] == checkmate(self_obj, board)[0] \
				and piece_color[0][1] == "K" and mode == 1:
			changeColor = 1
			args = [0, checkmate(self_obj, board)[2]]
			
		board[x_old][y_old].create_image(42, 40, image=img,\
		tag="get_image")

		board[x_new][y_new].delete("all")

		if condition == 1:
			board[x_new][y_new].create_image(42, 40, image=img_piece_eaten,\
				tag="get_image")

		if changeColor == 1:
			self_obj.change_Color(args)

		return False

	else:
		board[x_old][y_old].create_image(42, 40, image=img,\
		tag="get_image")

		board[x_new][y_new].delete("all")

		if condition == 1:
			board[x_new][y_new].create_image(42, 40, image=img_piece_eaten,\
				tag="get_image")

		return True


def help(self_obj, board, color, pos):
	# Permet de savoir comment éviter un échec
	returnValue = False
	for x in range(0,8):
		for y in range(0,8):
			if check_is_empty(self_obj, [x,y]) == False:
				if self_obj.get_image(board[x][y])[1][0][0] == color:
					img_name = self_obj.get_image(board[x][y])[1][0]
					img = self_obj.get_image(board[x][y])[0]

					for i in range(0,8):
						for j in range(0,8):
							# On regarde si il y a echec quand <img_name> se déplace
							# à la case [i,j]
							if which_piece([img_name], self_obj, [i,j], [x,y], checkmate=1) == True:
								if testBoard(self_obj, board, img,[x,y],[i,j]):
									helpMove = img_name+" : "+str(chr(65+y))+str(x+1)+" -> "+str(chr(65+j))+str(i+1)
									self_obj.set_help(helpMove)
									returnValue = True
							
	if returnValue == False:
		print("ECHEC et MAT")
	return returnValue
	