#include<iostream>
using namespace std;

char board[3][3]={'1','2','3','4','5','6','7','8','9'};
char player= 'X';

void show_board() {
	for(int i=0;i<=2;i++) {
		for(int j=0;j<=2;j++) {
			cout<<board[i][j]<<" ";
		}
		cout<<endl;
	}
}

void board_reset(){
	board[0][0]='1';
	board[0][1]='2';
	board[0][2]='3';
	board[1][0]='4';
	board[1][1]='5';
	board[1][2]='6';
	board[2][0]='7';
	board[2][1]='8';
	board[2][2]='9';
}

void toggle_player() {
	if(player=='X'){
		player='O';
	}
	else {
		player = 'X';
	}
}

bool winning_check() {
	for(int i=0;i<=2;i++){
		if ((board[i][0]==board[i][1])&&(board[i][0]==board[i][2]))
			return true;
		else if ((board[0][i]==board[1][i])&&(board[0][i]==board[2][i]))
			return true;
	}
	if ((board[0][0]==board[1][1])&&(board[0][0]==board[2][2]))
		return true;
	if ((board[0][2]==board[1][1])&&(board[0][2]==board[2][0]))
		return true;
	
	return false;
}
