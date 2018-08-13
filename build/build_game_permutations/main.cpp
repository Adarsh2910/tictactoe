#include<iostream>
#include<fstream>
#include<string>
#include<limits>
#include"boardlogic.cpp"
#include"CSV_connect.cpp"

using namespace std;

void game_run(int* arr,int gameno) {
	board_reset(); 
	show_board();
	int count=0;
	int line;
	int player_no;
	player = 'X';
	
	for(int i=0;i<9;i++){
		
		line = arr[i];
		
		if(line == 1){
			board[0][0] = player;
			count++;
		}
		else if(line == 2){
			board[0][1] = player;
			count++;
		}
		else if(line == 3){
			board[0][2] = player;
			count++;
		}
		else if(line== 4){
			board[1][0] = player;
			count++;
		}
		else if(line== 5){
			board[1][1] = player;
			count++;
		}
		else if(line== 6){
			board[1][2] = player;
			count++;
		}
		else if(line == 7){
			board[2][0] = player;
			count++;
		}
		else if(line == 8){
			board[2][1] = player;
			count++;
		}
		else if(line == 9){
			board[2][2] = player;
			count++;
		}
		
		if(player=='X')
			player_no=1;
		else
			player_no=2;
	
		toggle_player();

		if(count==9 && winning_check()==false){
			cout<<"Draw\n";
			cout<<count<<"\n";
			csv_write(gameno,count,player_no,line,player,0);
			return;
		}	
		if(winning_check()==true) {
			show_board();
			cout<<player<<" Wins\n";
			cout<<count<<"\n";
			csv_write(gameno,count,player_no,line,player,player_no);
			return;
		}
		csv_write(gameno,count,player_no,line,player,-1);		
	}
}

fstream& Go_to_line(fstream& file, int num){
    file.seekg(ios::beg);
    for(int i=0; i < num - 1; ++i){
        file.ignore(numeric_limits<streamsize>::max(),'\n');
    }
    return file;
}

void array_input(){
	int gameno=0;
	string line;
	int in_value[9];
	fstream myfile("permutations");
	for(int j=1;j<=362880;j++){
		Go_to_line(myfile,j);
		myfile >> line;
		int i = 0;
		for ( std::string::iterator it=line.begin(); it!=line.end(); ++it) {
			in_value[i] = int(*it - '0');
			i += 1;
		}
		gameno++;
		game_run(in_value,gameno);
	}
}
int main() {
	array_input();
	close_csv_file();
	return 0;
}

/**Game no	Move no	Player no	Cell no	Outcome
	1		1		1			2		-1
	1		2		2			3		-1
	1		3		1			5		-1
	1		4		2			8		-1
	1		5		1			1		-1
	1		6		2			9		-1
	1		7		1			7		-1
	1		8		2			6		2
**/
