__author__ = 'ankush'


import MySQLdb
from random import randint
import json


def display_board(board):
	for i in range(0,3):
		print board[i] + ' ',
	print
	for i in range(3,6):
		print board[i] + ' ',
	print
	for i in range(6,9):
		print board[i] + ' ',
	print


def check_draw():
	count = 0
	for i in range(0,9):
		if board[i]!='_':
			count += 1
	if count==9:
		return True
	else:
		return False


def check_winner():
	if board[0]==board[3]==board[6]:
		if board[0]!='_':
			return board[0]
	if board[1]==board[4]==board[7]:
		if board[1]!='_':
			return board[0]
	if board[2]==board[5]==board[8]:
		if board[2]!='_':
			return board[2]
	if board[0]==board[1]==board[2]:
		if board[0]!='_':
			return board[0]
	if board[3]==board[4]==board[5]:
		if board[3]!='_':
			return board[3]
	if board[6]==board[7]==board[8]:
		if board[6]!='_':
			return board[6]
	if board[0]==board[4]==board[8]:
		if board[0]!='_':
			return board[0]
	if board[2]==board[4]==board[6]:
		if board[2]!='_':
			return board[2]
	return None



def get_move_id_from_board(board):
	X_positions = [str(ind+1) for ind,value in enumerate(board) if value=='X']
	O_positions = [str(ind+1) for ind,value in enumerate(board) if value=='O']
	move_id = '0'
	for ind in range(len(X_positions)):
		if ind>(len(O_positions)-1):
			move_id += X_positions[ind]
		else:
			move_id += (X_positions[ind] + O_positions[ind])
	return move_id



def get_optimal_move(cursor, board=None, move_id=None):
	if not move_id:
		move_id = get_move_id_from_board(board)
	if len(move_id)%2==0:
		comp_symbol = 'O'
	else:
		comp_symbol = 'X'
	if comp_symbol=='O':
		query = "select move, score, result from tictactoe where parent_move_id='%s' order by score asc" %(move_id)
	else:
		query = "select move, score, result from tictactoe where parent_move_id='%s' order by score desc" %(move_id)
	cursor.execute(query)

	top_row = cursor.fetchone()
	if not top_row:
		return None

	#If top row satisfies the winning condition
	top_result = int(top_row[2])
	if comp_symbol=='X' and top_result==1:
		return top_row[0]
	elif comp_symbol=='O' and top_result==2:
		return top_row[0]


	top_score = int(top_row[1])
	moves = [top_row[0]]


	rows = cursor.fetchall()
	for row in rows:
		print row
		score = int(row[1])
		result = int(row[2])
		if comp_symbol=='X' and result==1:
			return row[0]
		elif comp_symbol=='O' and result==2:
			return row[0]
		if top_score!=score:
			break
		moves.append(row[0])
	return moves[randint(0,len(moves)-1)]



if __name__ == '__main__':

	mysql_credentials = json.load(open('mysql_credentials.json'))
	conn = MySQLdb.connect(**mysql_credentials)
	cursor = conn.cursor()

	board = ['_']*9

	print "Choose X or O (X goes first)"
	user_symbol = raw_input()

	move_no = 0
	user_symbol = user_symbol.upper()
	if user_symbol=='X':
		move_no += 1
		user_move = int(raw_input())
		board[user_move-1] = user_symbol
		comp_symbol = 'O'
	else:
		comp_symbol = 'X'

	while True:
		display_board(board)
		move_no += 1
		comp_move = get_optimal_move(cursor, board=board)
		print comp_move
		if comp_move:
			board[comp_move-1] = comp_symbol
			display_board(board)

		result = check_winner()
		if result:
			display_board(board)
			print result + ' Wins!'
			break
		if check_draw():
			display_board(board)
			print 'Draw'
			break

		move_no += 1
		user_move = int(raw_input())
		board[user_move-1] = user_symbol

		result = check_winner()
		if result:
			display_board(board)
			print result + ' Wins!'
			break
		if check_draw():
			display_board(board)
			print 'Draw'
			break

