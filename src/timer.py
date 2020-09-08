from random import randint
import argparse
import sys
import time
from mancala import *

if __name__ == "__main__":
	sys.setrecursionlimit(10000)
	board = [[N_STONES]*N_PITS for _ in range(2)]
	store = [0, 0]
	parser = argparse.ArgumentParser()
	parser.add_argument('player1', type=str)
	parser.add_argument('player2', type=str)
	args = parser.parse_args()
	start = time.time()
	gameplay(str(args.player1), str(args.player2), board, store)
	print("Time taken: "+str(time.time() - start)+" seconds!")