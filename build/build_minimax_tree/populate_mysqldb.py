__author__ = 'ankush'


import MySQLdb
import csv
import json

mysql_credentials = json.load(open('../../mysql_credentials.json'))
conn = MySQLdb.connect(**mysql_credentials)
cursor = conn.cursor()

fo = open('tictactoe.csv')
reader = csv.reader(fo)

root_node_query = "insert into tictactoe values('0', 0, 0, 0, -1, '', NULL)"
cursor.execute(root_node_query)


move_id = '0'
game_no = 1
count = 0
for row in reader:
    if 'game' in row[0].lower():  #Ignoring header line
        continue

    count += 1

    if count%50000==0:
        print count
        conn.commit()

    move_no = int(row[1])
    move = int(row[3])
    player = int(row[2])
    result = int(row[4])

    if game_no==int(row[0]):
        move_id += str(move)
    else:
        game_no = int(row[0])
        move_id = '0' + str(move)

    parent_move_id = move_id[:-1]

    query = "insert into tictactoe values('%s', %d, %d, %d, %d, '%s', NULL)" %(move_id, player, move, move_no, result, parent_move_id)

    try:
        cursor.execute(query)
    except MySQLdb.IntegrityError:
        pass
    

conn.commit()



###################################################################################################

#CODE FOR INSERTING MINIMAX SCORES
#
#
#
#

print "Setting decision node scores..."
# Setting score for all decision nodes
start = 0
limit = 10000
while True:
    query = "select move_id, result, move_no from tictactoe where result!=-1 limit %d,%d" %(start, limit)
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        break
    for row in rows:
        move_id = str(row[0])
        result = int(row[1])
        move_no = int(row[2])
        score = 0
        if result==1:
            score = 1
        if result==2:
            score = -1
        query = "update tictactoe set score=%d where move_id='%s'" %(score,move_id)
        cursor.execute(query)

    start += limit
    print start
    conn.commit()

print "Decision node scores set.."


for level in range(9,0,-1):
    print "level: %d" %(level)
    print
    start = 0
    limit = 10000
    while True:
        if level%2==0:
            query = "select parent_move_id, min(score) from tictactoe where move_no=%d group by parent_move_id limit %d,%d" %(level,start,limit)
        else:
            query = "select parent_move_id, max(score) from tictactoe where move_no=%d group by parent_move_id limit %d,%d" %(level,start,limit)

        print query
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            break

        for row in rows:
            move_id = str(row[0])
            score = int(row[1])
            query = "update tictactoe set score=%d where move_id='%s'" %(score,move_id)
            cursor.execute(query)

        start += limit
        print start
        conn.commit()


conn.commit()
