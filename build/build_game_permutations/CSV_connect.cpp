#include<iostream>
#include<fstream>
#include<iomanip>

using namespace std;

ofstream csvfile("tictactoe.csv", ios::app);

int csv_write(int gameno, int count, int player_no, int line, char player, int outcome){
	csvfile<<gameno<<","<<count<<","<<player_no<<","<<line<<","<<outcome<<endl;
	return 0;
}

int close_csv_file() {
	csvfile.close();
	return 0;
}