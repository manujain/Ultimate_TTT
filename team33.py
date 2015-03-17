class Player33:
	maxcount = 0
	count = 0
	BIGINT = 9999999999999

	def __init__(self):
		pass

	def getStats(self, tempBlock, tempBoard):
		filledInTempBlock = 0
		movedChances = 0

		for i in tempBlock:
			if i is not '-':
				filledInTempBlock = filledInTempBlock + 1

		for i in tempBoard:
			for j in i:
				if j is not '-':
					movedChances = movedChances + 1
		return filledInTempBlock, movedChances

	def copyBlock1D(self, Block1D):
		toReturn = []
		for eachItem in Block1D:
			toReturn.append(eachItem)
		return toReturn

	def copyBlock2D(self, Block2D):
		toReturn = []
		for each1D in Block2D:
			inside1D = []
			for eachCell in each1D:
				inside1D.append(eachCell)
			toReturn.append(inside1D)
		return toReturn

	def getBoardmax(self, listBoardofBoardtupleBoardandBoardheuristic):
		valueToReturn = -self.BIGINT
		maBoard = (0, 0)
		index = 0
		for i in listBoardofBoardtupleBoardandBoardheuristic:
			if i[1][2]>valueToReturn:
				valueToReturn = i[1][2]
				maBoard = i[1][1]
				index = i[0]
		return index, maBoard, valueToReturn


	def getBoardmin(self, listBoardofBoardtupleBoardandBoardheuristic): 
		valueToReturn = self.BIGINT
		miBoard = (0, 0)
		index = 0
		for i in listBoardofBoardtupleBoardandBoardheuristic:
			if i[1][2]<valueToReturn:
				valueToReturn = i[1][2]
				miBoard = i[1][1]
				index = i[0]
		return index, miBoard, valueToReturn

	def isCorner(self, x, y):
		forCorner = [0, 2, 3, 5, 6, 8]
		if x in forCorner and y in forCorner:
			return 1
		return 0

	def removeWaste(self, gameb, useful, blockBoardstat):
		outputCells = []
		for idOfBlock in useful:
			part1 = idOfBlock / 3
			part2 = idOfBlock % 3
			for i in range(part1 * 3, part1 * 3 + 3):
				for j in range(part2 * 3, part2 * 3 + 3):
					if gameb[i][j]  == '-':
						outputCells.append((i, j))
		if outputCells  == []:
			for i in range(9):
				for j in range(9):
                        	        no = (i/3)*3
                                	no  +=  (j/3)
					if gameb[i][j]  == '-' and blockBoardstat[no]  == '-':
						outputCells.append((i, j))	
		return outputCells


	def getNewMoves(self, oldMove, tempBoard, tempBlock):
		forCorner = [0, 2, 3, 5, 6, 8]
		blocksAllowed  = []

		if oldMove[0] in forCorner and oldMove[1] in forCorner:
			if oldMove[0] % 3  == 0 and oldMove[1] % 3  == 0:
				blocksAllowed = [0, 1, 3]
			elif oldMove[0] % 3  == 0 and oldMove[1] in [2, 5, 8]:
				blocksAllowed = [1, 2, 5]
			elif oldMove[0] in [2, 5, 8] and oldMove[1] % 3  == 0:
				blocksAllowed  = [3, 6, 7]
			elif oldMove[0] in [2, 5, 8] and oldMove[1] in [2, 5, 8]:
				blocksAllowed = [5, 7, 8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
			if oldMove[0] % 3  == 0 and oldMove[1] in [1, 4, 7]:
				blocksAllowed = [1]
	
			elif oldMove[0] in [1, 4, 7] and oldMove[1] % 3  == 0:
				blocksAllowed = [3]
		
			elif oldMove[0] in [2, 5, 8] and oldMove[1] in [1, 4, 7]:
				blocksAllowed = [7]

			elif oldMove[0] in [1, 4, 7] and oldMove[1] in [2, 5, 8]:
				blocksAllowed = [5]
			elif oldMove[0] in [1, 4, 7] and oldMove[1] in [1, 4, 7]:
				blocksAllowed = [4]
                
		for i in reversed(blocksAllowed):
			if tempBlock[i] != '-':
				blocksAllowed.remove(i)
		outputCells = self.removeWaste(tempBoard, blocksAllowed, tempBlock)
		return outputCells

	def bestPossibleMoves(self, prevBoardmove, board, block, listOfMoves, specialFlag, depth, myplayerBoard, maxDepth):
		self.count = self.count + 1
		prevBoardmoveBoard = prevBoardmove
		if depth > maxDepth:
			return 0, prevBoardmove, self.Heuristic(board, block, prevBoardmoveBoard, myplayerBoard)
		elif len(listOfMoves) is 0:
			return 0, prevBoardmove, self.Heuristic(board, block, prevBoardmoveBoard, myplayerBoard)
		elif self.count >= 100000 and maxDepth is 3:
			return 0, prevBoardmove, self.Heuristic(board, block, prevBoardmoveBoard, myplayerBoard)
		else:
			scoreBoardoutputCells = []
			count = 0
			for movesToMove in listOfMoves:	
				givenBoard = self.copyBlock2D(board)
				givenBlock = self.copyBlock1D(block)
				row = movesToMove[0]
				col = movesToMove[1]
				if specialFlag  == 0:
					givenBoard[row][col] = 'x'
				else:
					givenBoard[row][col] = 'o'
				newBlocksT = self.blockUpdate(givenBoard, givenBlock, movesToMove, specialFlag)
				placesToMoveNow = self.getNewMoves(movesToMove, givenBoard, newBlocksT)			
				p = (count, self.bestPossibleMoves(movesToMove, givenBoard, newBlocksT, placesToMoveNow, specialFlag^1, depth + 1, myplayerBoard, maxDepth))
				scoreBoardoutputCells.append(p);
#				print scoreBoardoutputCells	
				count = count + 1

			if depth % 2 == 0:
				txx = self.getBoardmax(scoreBoardoutputCells)
				return txx
			else:
				BlockYy = self.getBoardmin(scoreBoardoutputCells)
				return BlockYy
			
	def blockUpdate(self, tBoardbrd, tBoardblck, vBoardm, XorO):
		rc = vBoardm[0] / 3 #row change
		col = vBoardm[1] / 3 #coloumn change
		idx = rc*3 + col
		xBoards = rc*3
		yBoards = col*3
		if XorO  == 0:
			zz = 'x' ##
		else:
			zz = 'o'
		if(tBoardbrd[xBoards + 0][yBoards + 0] == zz and tBoardbrd[xBoards + 0][yBoards + 1] == zz and tBoardbrd[xBoards + 0][yBoards + 2] == zz):
			tBoardblck[idx]=zz
		if(tBoardbrd[xBoards + 1][yBoards + 0] == zz and tBoardbrd[xBoards + 1][yBoards + 1] == zz and tBoardbrd[xBoards + 1][yBoards + 2] == zz):
			tBoardblck[idx]=zz
		if(tBoardbrd[xBoards + 2][yBoards + 0] == zz and tBoardbrd[xBoards + 2][yBoards + 1] == zz and tBoardbrd[xBoards + 2][yBoards + 2] == zz):
			tBoardblck[idx]=zz
		if(tBoardbrd[xBoards + 0][yBoards + 0] == zz and tBoardbrd[xBoards + 1][yBoards + 0] == zz and tBoardbrd[xBoards + 2][yBoards + 0] == zz):
			tBoardblck[idx]=zz
		if(tBoardbrd[xBoards + 0][yBoards + 1] == zz and tBoardbrd[xBoards + 1][yBoards + 1] == zz and tBoardbrd[xBoards + 2][yBoards + 1] == zz):
			tBoardblck[idx]=zz
		if(tBoardbrd[xBoards + 0][yBoards + 2] == zz and tBoardbrd[xBoards + 1][yBoards + 2] == zz and tBoardbrd[xBoards + 2][yBoards + 2] == zz):
			tBoardblck[idx]=zz
		if(tBoardbrd[xBoards + 0][yBoards + 0] == zz and tBoardbrd[xBoards + 1][yBoards + 1] == zz and tBoardbrd[xBoards + 2][yBoards + 2] == zz):
			tBoardblck[idx]=zz
		if(tBoardbrd[xBoards + 0][yBoards + 2] == zz and tBoardbrd[xBoards + 1][yBoards + 1] == zz and tBoardbrd[xBoards + 2][yBoards + 0] == zz):
			tBoardblck[idx]=zz
		return tBoardblck

	def Heuristic(self, tempBoardBoard, tempBlockBoard, tupleofcell, meOrOpponent):

		factor = [10, 9, 10, 9, 12, 9, 10, 9, 10];
		
		if meOrOpponent  == 0:
			player = 'x'
			opponent = 'o'
		else:
			player ='o'
			opponent = 'x'

		WinningBoardtriads = [
			( 0, 1, 2 ), 
			( 3, 4, 5 ), 
			( 6, 7, 8 ), 
			( 0, 3, 6 ), 
			( 1, 4, 7 ), 
			( 2, 5, 8 ), 
			( 0, 4, 8 ), 
			( 2, 4, 6 )
		];

		HeuristicBoardAroway = [
			( 0, -10, -100, -1000 ), 
			( 10, 0, 0, 0 ), 
			( 100, 0, 0, 0 ), 
			( 1000, 0, 0, 0 )
		];

		toReturn = 0

		for i in range(9):
			blockX = i/3
			BlockY = i%3
			offsetX = blockX*3
			offsetY = BlockY*3

			for j in range(8):
			#Looping on winning triads!
				countOfOpponent = 0
				countOfPlayer = 0
				for k in range(3):					
					x = WinningBoardtriads[j][k]
					rowAdd = x/3
					colAdd = x%3
					if(tempBoardBoard[offsetX + rowAdd][offsetY + colAdd]  == player):
						countOfPlayer  += 1
					elif(tempBoardBoard[offsetX + rowAdd][offsetY + colAdd]  == opponent):
						countOfOpponent  += 1
				toReturn = toReturn + factor[i] * HeuristicBoardAroway[countOfPlayer][countOfOpponent]

		for i in range(8):
			countOfOpponent = 0
			countOfPlayer = 0
			for j in range(3):
				if tempBlockBoard[WinningBoardtriads[i][j]]  == player:
					countOfPlayer  += 1
				elif tempBlockBoard[WinningBoardtriads[i][j]]  == opponent:
					countOfOpponent  += 1
			toReturn = toReturn + 70 * HeuristicBoardAroway[countOfPlayer][countOfOpponent]
		return toReturn


	def move(self, tempBoard, tempBlock, oldMove, flag):
		#print self.count
		self.maxcount = max(self.count, self.maxcount)
		#print self.maxcount
		self.count = 0
		if oldMove  == (-1, -1):
			return (0, 0)
		oldMoveBoard = oldMove
		tempBoardBoard = self.copyBlock2D(tempBoard)
		tempBlockBoard = self.copyBlock1D(tempBlock)
		if flag == 'x':
			meOrOpponent = 0
		else:
			meOrOpponent = 1
		myplayer = meOrOpponent
		outputCells = self.getNewMoves(oldMoveBoard, tempBoardBoard, tempBlockBoard)
		filledInTempBlock = 0
		movedChances = 0

		for i in tempBlock:
			if i is not '-':
				filledInTempBlock = filledInTempBlock + 1

		for i in tempBoard:
			for j in i:
				if j is not '-':
					movedChances = movedChances + 1

		filledInTempBlock, movedChances = self.getStats(tempBlock, tempBoard);
		
		add = 0
		#After 50 chances start going to more depth.
		if movedChances > 50:
			add = add + 1

		bestSetOfMoves = self.bestPossibleMoves(oldMoveBoard, tempBoardBoard, tempBlockBoard, outputCells, meOrOpponent, 0, myplayer, 2 + add)
		return outputCells[bestSetOfMoves[0]]
