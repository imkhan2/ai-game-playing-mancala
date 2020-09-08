from random import randint
import argparse
import sys

N_PITS = 6
N_STONES = 4
PLAYER = 0
WINNER = -1
STATES = 0         # For maintaining the count of number of expanded states
MINIMAX_DEPTH = 10
ALPHABETA_DEPTH = 10

def toggle_player():
	global PLAYER
	PLAYER = (PLAYER+1)%2

def utility(player, store):
	return store[player] - store[(player+1)%2]

def heuristic(player, board, store):
	return (store[player] + sum(board[player])) - (store[(player+1)%2] + sum(board[(player+1)%2]))

def move(pit, board, store):
	global PLAYER                # players here are 0 and 1 and pit is oriented from 0 to 5 for 1 and 5 to 0 for 0
	pit -= 1
	player = PLAYER
	last_index = [player, pit]
	stones = board[player][pit]
	board[player][pit] = 0
	y = min(N_PITS-pit-1, stones)
	for i in range(1, y+1):
		board[player][pit+i] += 1
	last_index = [player, pit+y]
	stones = stones - y
	if stones>0:
		store[player] += 1
		stones -= 1
		last_index = [-1,-1]
	while stones:
		player = (player + 1)%2
		y = min(N_PITS, stones)
		for i in range(y):
			board[player][i] += 1
		last_index = [player, y-1]
		stones = stones - y
		if stones>0 and player == PLAYER:
			store[player] += 1
			stones -= 1
			last_index = [-1,-1]
	if last_index[0] == PLAYER and board[last_index[0]][last_index[1]] == 1 and board[(last_index[0]+1)%2][N_PITS-1-last_index[1]]>0:
		store[PLAYER] += board[last_index[0]][last_index[1]]
		store[PLAYER] += board[(last_index[0]+1)%2][N_PITS-1-last_index[1]]
		board[last_index[0]][last_index[1]] = 0
		board[(last_index[0]+1)%2][N_PITS-1-last_index[1]] = 0
	if last_index[0] >= 0:
		toggle_player()
	return board, store

def minimax(player, maxPlayer, board, store, depth):
	global PLAYER, STATES
	temp_board = [board[i][:] for i in range(2)]
	temp_store = [store[0], store[1]]
	if game_end(temp_board, temp_store):
		return utility(maxPlayer, temp_store)
	if depth == 0:
		return heuristic(maxPlayer, board, store)
	if player == maxPlayer:
		value = -1000
		for i in range(1, 7):
			if board[player][i-1] > 0:
				temp_player = PLAYER
				STATES += 1
				move(i, temp_board, temp_store)
				value = max(value, minimax(PLAYER, maxPlayer, temp_board, temp_store, depth-1))
				PLAYER = temp_player
				temp_board = [board[i][:] for i in range(2)]
				temp_store = [store[0], store[1]]
		return value
	else:
		value = 1000
		for i in range(1, 7):
			if board[player][i-1] > 0:
				temp_player = PLAYER
				STATES += 1
				move(i, temp_board, temp_store)
				value = min(value, minimax(PLAYER, maxPlayer, temp_board, temp_store, depth-1))
				PLAYER = temp_player
				temp_board = [board[i][:] for i in range(2)]
				temp_store = [store[0], store[1]]
		return value

def alphabeta(player, maxPlayer, alpha, beta, board, store, depth):
	global PLAYER, STATES
	temp_board = [board[i][:] for i in range(2)]
	temp_store = [store[0], store[1]]
	if game_end(temp_board, temp_store):
		return utility(maxPlayer, temp_store)
	if depth == 0:
		return heuristic(maxPlayer, board, store)
	if player == maxPlayer:
		value = -1000
		for i in range(1, 7):
			if board[player][i-1] > 0:
				temp_player = PLAYER
				STATES += 1
				board_new, store_new = move(i, temp_board, temp_store)
				value = max(value, alphabeta(PLAYER, maxPlayer, alpha, beta, temp_board, temp_store, depth-1))
				PLAYER = temp_player
				temp_board = [board[i][:] for i in range(2)]
				temp_store = [store[0], store[1]]
				alpha = max(alpha, value)
				if alpha >= beta:
					break
		return value
	else:
		value = 1000
		for i in range(1, 7):
			if board[player][i-1] > 0:
				temp_player = PLAYER
				STATES += 1
				board_new, store_new = move(i, temp_board, temp_store)
				value = min(value, alphabeta(PLAYER, maxPlayer, alpha, beta, temp_board, temp_store, depth-1))
				PLAYER = temp_player
				temp_board = [board[i][:] for i in range(2)]
				temp_store = [store[0], store[1]]
				beta = min(beta, value)
				if alpha >= beta:
					break
		return value

def game_end(board, store):          # check for terminal condition
	global WINNER, PLAYER
	if sum(board[PLAYER]) == 0 or sum(board[(PLAYER+1)%2]) == 0:
		o_player = (PLAYER+1)%2
		for i in range(N_PITS):
			store[PLAYER] += board[PLAYER][i]
		for i in range(N_PITS):
			store[o_player] += board[o_player][i]
		if store[PLAYER]>store[o_player]:
			WINNER = PLAYER
		elif store[PLAYER]<store[o_player]:
			WINNER = o_player
		else:
			WINNER = -1
		return True
	else:
		return False

def select_move(player_type, board, store):        # select move for every turn
	global PLAYER, STATES
	temp_player = PLAYER
	temp_board = [board[i][:] for i in range(2)]
	temp_store = [store[0], store[1]]
	if player_type == 'minimax':
		max_pit = -1
		max_value = -1000
		for i in range(1, 7):
			if board[PLAYER][i-1] > 0:
				move(i, temp_board, temp_store)
				STATES+=1
				value = minimax(PLAYER, temp_player, temp_board, temp_store, MINIMAX_DEPTH)
				if max_value < value:
					max_value = value
					max_pit = i
				PLAYER = temp_player
				temp_board = [board[i][:] for i in range(2)]
				temp_store = [store[0], store[1]]
		print('Player '+str(PLAYER+1)+' move: '+str(max_pit))
		return max_pit
	elif player_type == 'alphabeta':
		max_pit = -1
		max_value = -1000
		for i in range(1, 7):
			if board[PLAYER][i-1] > 0:
				move(i, temp_board, temp_store)
				value = alphabeta(PLAYER, temp_player, -10000, 10000, temp_board, temp_store, ALPHABETA_DEPTH)
				if max_value < value:
					max_value = value
					max_pit = i
				PLAYER = temp_player
				temp_board = [board[i][:] for i in range(2)]
				temp_store = [store[0], store[1]]
		print('Player '+str(PLAYER+1)+' move: '+str(max_pit))
		return max_pit
	elif player_type == 'human':
		pit = int(input('Enter player '+str(PLAYER + 1)+' move: '))
		while pit < 0 or board[PLAYER][pit-1] == 0:
			print('Illegal move! Re-enter:')
			pit = int(input())
		return pit
	elif player_type == 'random':
		pit = randint(1, 6)
		while board[PLAYER][pit-1] == 0:
			pit = randint(1, 6)
		print('Player '+str(PLAYER+1)+' move: '+str(pit))
		return pit

def print_board(board, store):
	print('      6    5    4    3    2    1')
	print('    -----------------------------')
	print('{:02d}'.format(store[0]), end=' | ')
	print('{:02d}'.format(board[0][5]), '{:02d}'.format(board[0][4]), '{:02d}'.format(board[0][3]), '{:02d}'.format(board[0][2]), '{:02d}'.format(board[0][1]), '{:02d}'.format(board[0][0]), sep=' | ', end=' ')
	print('| P1')
	print("-------------------------------------")
	print('P2 |', end=' ')
	print('{:02d}'.format(board[1][0]), '{:02d}'.format(board[1][1]), '{:02d}'.format(board[1][2]), '{:02d}'.format(board[1][3]), '{:02d}'.format(board[1][4]), '{:02d}'.format(board[1][5]), sep=' | ', end=' | ')
	print('{:02d}'.format(store[1]))
	print('    -----------------------------')
	print('      1    2    3    4    5    6\n')

def gameplay(player1, player2, board, store):
	global WINNER
	print_board(board, store)
	while not game_end(board, store):
		if PLAYER == 0:
			pit = select_move(player1, board, store)
		else:
			pit = select_move(player2, board, store)
		move(pit, board, store)
		print_board(board, store)
	if WINNER == -1:
		print("Draw!")
	else:
		print("Player "+str(WINNER+1)+ " wins!\n")

if __name__ == "__main__":
	sys.setrecursionlimit(10000)
	board = [[N_STONES]*N_PITS for _ in range(2)]
	store = [0, 0]
	parser = argparse.ArgumentParser()
	parser.add_argument('player1', type=str)
	parser.add_argument('player2', type=str)
	args = parser.parse_args()
	gameplay(str(args.player1), str(args.player2), board, store)
	#select_move('minimax', board, store)
	#print(STATES)