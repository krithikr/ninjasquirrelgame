from sys import maxsize
from copy import deepcopy
import sys, getopt

class Node():
    def __init__(self,cutoff,depth,player,playerchar,oppplayer,board,scoreboard,score1,score2,move,minmax=0):
        self.cutoff=cutoff #cutoff depth value
        self.depth=depth #what is the depth of the tree
        self.board=board #the position of all the pieces on the board
        self.scoreboard=scoreboard #the scores at every square on the board
        self.player=player #whose turn it is
        self.playerchar=playerchar
        self.oppplayer=oppplayer
        self.score1=score1 #what is the score of player 1
        self.score2=score2 #what is the score of player 2
        self.move=move
        if(self.player==1):
            self.minmax=maxsize*-1
        elif(self.player==2):
            self.minmax=maxsize
        self.children=[] #the list of children at that stage
        if(self.depth!=self.cutoff):
            self.GenerateChildren()
    
    def IsValid(self,i,j):
        if(i>=0 and i<=4 and j>=0 and j<=4):
            return True
        else:
            return False
    
    def OppositePlayer(self,c):
        if(c=="X"):
            return "O"
        else:
            return "X"
            
        
    def MoveChecker(self,board,x,y,player):
        if(player==1):
            c=self.playerchar
        else:
            c=self.OppositePlayer(self.playerchar)
        if((self.IsValid(x+1,y) and board[x+1][y]==c) or (self.IsValid(x-1,y) and board[x-1][y]==c) or (self.IsValid(x,y+1) and board[x][y+1]==c) or (self.IsValid(x,y-1) and board[x][y-1]==c)):
            if(self.IsValid(x-1,y)):
                if(board[x-1][y]==self.OppositePlayer(c)):
                    board[x-1][y]=c
            if(self.IsValid(x+1,y)):
                if(board[x+1][y]==self.OppositePlayer(c)):
                    board[x+1][y]=c
            if(self.IsValid(x,y+1)):
                if(board[x][y+1]==self.OppositePlayer(c)):
                    board[x][y+1]=c
            if(self.IsValid(x,y-1)):
                if(board[x][y-1]==self.OppositePlayer(c)):
                    board[x][y-1]=c
        
                                
        
    def GenerateChildren(self):
        dict1 = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'};
        dict2 = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5'};
        if(self.player==2):
            #decide the move
            #pass the move to the evaluation function
            #once the e
            for i in range(5):
                for j in range(5):
                    if(self.board[i][j]=="*"):
                        extra=deepcopy(self.board)
                        extra[i][j]=self.oppplayer
                        self.MoveChecker(extra,i,j,2)
                        score1=0
                        for a in range(5):
                            for b in range(5):
                                if(extra[a][b]==self.playerchar):
                                    score1+=self.scoreboard[a][b]
                        newscore1=deepcopy(score1)
                        score1=0
                        score2=0
                        for a in range(5):
                            for b in range(5):
                                if(extra[a][b]==self.oppplayer):
                                    score2+=self.scoreboard[a][b]
                        newscore2=deepcopy(score2)
                        score2=0
                        move=dict1[j]+dict2[i]
                        self.children.append(Node(self.cutoff,self.depth+1,1,self.playerchar,self.oppplayer,extra,self.scoreboard,newscore1,newscore2,move,0))
        elif(self.player==1):
            #decide the move
            #pass the move to the evaluation function
            for i in range(5):
                for j in range(5):
                    if(self.board[i][j]=="*"):
                        extra=deepcopy(self.board)
                        extra[i][j]=self.playerchar
                        self.MoveChecker(extra,i,j,1)
                        score1=0
                        for a in range(5):
                            for b in range(5):
                                if(extra[a][b]==self.playerchar):
                                    score1+=self.scoreboard[a][b]
                        newscore1=deepcopy(score1)
                        score1=0
                        score2=0
                        for a in range(5):
                            for b in range(5):
                                if(extra[a][b]==self.oppplayer):
                                    score2+=self.scoreboard[a][b]
                        newscore2=deepcopy(score2)
                        score2=0
                        move=dict1[j]+dict2[i]
                        self.children.append(Node(self.cutoff,self.depth+1,2,self.playerchar,self.oppplayer,extra,self.scoreboard,newscore1,newscore2,move,0))

def Evaluation(a,b,player):
        if(player==1):
            return a-b
        else:
            return b-a
def SubValue(a):
    if(a==maxsize):
        return "Infinity"
    elif(a==maxsize*-1):
        return "-Infinity"
    else:
        return str(a)

def AlphaBeta(node,depth,alpha,beta,player,check,traverse_log):
    if(check==0):
        traverse_log = open("traverse_log.txt", "w")
        traverse_log.write("Node,Depth,Value,Alpha,Beta\n")
    if(node.depth==node.cutoff):
        if((node.cutoff%2)!=0):
            if(player==1):
                node.minmax=Evaluation(node.score1, node.score2, 2)
            else:
                node.minmax=Evaluation(node.score1, node.score2, 1)
        else:
            node.minmax=Evaluation(node.score1, node.score2, player) 
        return node.minmax, alpha, beta
    else:
        if(node.player==1):
            bestvalue=maxsize*-1
            traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+","+SubValue(alpha)+","+SubValue(beta)+"\n")
            num=0
            for child in node.children:
                if(num>0):
                    traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+","+SubValue(alpha)+","+SubValue(beta)+"\n")
                temp,x,y=deepcopy(AlphaBeta(child,depth+1,alpha,beta,2,1,traverse_log))
                child.minmax=temp
                traverse_log.write(str(child.move)+","+str(child.depth)+","+SubValue(child.minmax)+","+SubValue(x)+","+SubValue(y)+"\n")
                if(temp>bestvalue):
                    bestvalue=temp
                if(bestvalue>x):
                    alpha=deepcopy(bestvalue)
                if(beta<=alpha):
                    break
                num+=1
            if(node.move=="root"):
                traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+","+SubValue(alpha)+","+SubValue(beta))
            return bestvalue,x,beta  
        elif(node.player==2):
            bestvalue=maxsize
            traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+","+SubValue(alpha)+","+SubValue(beta)+"\n")
            num=0
            for child in node.children:
                if(num>0):
                    traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+","+SubValue(alpha)+","+SubValue(beta)+"\n")
                temp,x,y=deepcopy(AlphaBeta(child,depth+1,alpha,beta,1,1,traverse_log))
                child.minmax=temp
                traverse_log.write(str(child.move)+","+str(child.depth)+","+SubValue(child.minmax)+","+SubValue(x)+","+SubValue(y)+"\n")
                if(temp<bestvalue):
                    bestvalue=temp
                if(bestvalue<y):
                    beta=deepcopy(bestvalue)
                if(beta<=alpha):
                    break
                num+=1
            if(node.move=="root"):
                traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+","+SubValue(alpha)+","+SubValue(beta))
            return bestvalue,alpha,y  
                
def MinMax(node,depth,player,check,traverse_log):
    if(check==0):
        traverse_log = open("traverse_log.txt", "w")
        traverse_log.write("Node,Depth,Value\n")
    if(node.depth==node.cutoff):
        if((node.cutoff%2)!=0):
            if(player==1):
                node.minmax=Evaluation(node.score1, node.score2, 2)
            else:
                node.minmax=Evaluation(node.score1, node.score2, 1)
        else:
            node.minmax=Evaluation(node.score1, node.score2, player)   
        return node.minmax
    else:
        if(node.player==1):
            traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(node.minmax)+"\n")                 
            bestvalue=maxsize*-1
            num=0
            for child in node.children:
                if(num>0):
                    traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+"\n")
                temp=MinMax(child,depth+1,2,1,traverse_log)
                child.minmax=temp
                traverse_log.write(str(child.move)+","+str(child.depth)+","+SubValue(child.minmax)+"\n")
                if(temp>bestvalue):
                    bestvalue=temp
                num+=1
        elif(node.player==2):
            traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(node.minmax)+"\n") 
            bestvalue=maxsize
            num=0
            for child in node.children:
                if(num>0):
                    traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue)+"\n")
                temp=MinMax(child,depth+1,1,1,traverse_log)
                child.minmax=temp
                traverse_log.write(str(child.move)+","+str(child.depth)+","+SubValue(child.minmax)+"\n")
                if(temp<bestvalue):
                    bestvalue=temp
                num+=1 
        if(node.move=="root"):
            traverse_log.write(str(node.move)+","+str(node.depth)+","+SubValue(bestvalue))
        return bestvalue
    
def AlphaBeta4(node,depth,alpha,beta,player):
    if(node.depth==node.cutoff):
        if((node.cutoff%2)!=0):
            if(player==1):
                node.minmax=Evaluation(node.score1, node.score2, 2)
            else:
                node.minmax=Evaluation(node.score1, node.score2, 1)
        else:
            node.minmax=Evaluation(node.score1, node.score2, player) 
        return node.minmax, alpha, beta
    else:
        if(node.player==1):
            bestvalue=maxsize*-1
            for child in node.children:
                temp,x,y=deepcopy(AlphaBeta4(child,depth+1,alpha,beta,2))
                child.minmax=temp
                if(temp>bestvalue):
                    bestvalue=temp
                if(bestvalue>x):
                    alpha=deepcopy(bestvalue)
                if(beta<=alpha):
                    break
            return bestvalue,x,beta  
        elif(node.player==2):
            bestvalue=maxsize
            for child in node.children:
                temp,x,y=deepcopy(AlphaBeta4(child,depth+1,alpha,beta,1))
                child.minmax=temp
                if(temp<bestvalue):
                    bestvalue=temp
                if(bestvalue<y):
                    beta=deepcopy(bestvalue)
                if(beta<=alpha):
                    break
            return bestvalue,alpha,y
    
def MinMax4(node,depth,player):
    if(node.depth==node.cutoff):
        if((node.cutoff%2)!=0):
            if(player==1):
                node.minmax=Evaluation(node.score1, node.score2, 2)
            else:
                node.minmax=Evaluation(node.score1, node.score2, 1)
        else:
            node.minmax=Evaluation(node.score1, node.score2, player)   
        return node.minmax
    else:
        if(node.player==1):                
            bestvalue=maxsize*-1
            for child in node.children:
                temp=MinMax4(child,depth+1,2)
                child.minmax=temp
                if(temp>bestvalue):
                    bestvalue=temp
        elif(node.player==2):
            bestvalue=maxsize
            for child in node.children:
                temp=MinMax4(child,depth+1,1)
                child.minmax=temp
                if(temp<bestvalue):
                    bestvalue=temp
        return bestvalue
        
def GreedyBFS(node):
    maxvalue=maxsize*-1
    for child in node.children:
        value=Evaluation(child.score1, child.score2, node.player)
        if(value>maxvalue):
            maxvalue=value
            temp=child
    return temp


def main(argv):
    depth=0
    inp=''
    try:
        options, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
        print 'hw1cs561s16old.py -i <inputfile>'
        sys.exit(2)
    for option, arg in options:
        if option in ("-i", "--ifile"):
            inp=arg
    inputfile=open(inp)
    x=int(inputfile.readline())
    if(x==4):
        player1=inputfile.readline()
        player1=player1.replace('\n', '')
        if(player1=="X"):
            oppplayer1="O"
        else:
            oppplayer1="X"
        y1=int(inputfile.readline())
        cutoff1=int(inputfile.readline())
        
        player2=inputfile.readline()
        player2=player2.replace('\n', '')
        if(player2=="X"):
            oppplayer2="O"
        else:
            oppplayer2="X"
        y2=int(inputfile.readline())
        cutoff2=int(inputfile.readline())
        scoreboard=[]
        board=list()
        for i in range(5):
            scorerow=inputfile.readline()
            scoreboard.append([int(a) for a in scorerow.split()] )   
        for j in range(5):
            positionrow=inputfile.readline()
            board.append(list(positionrow.strip('\n')))
        trace_state = open("trace_state.txt", "w")
        player=1
        temp=[]
        temp=deepcopy(board)
        while(1):
            if(player==1):
                depth=0
                root1=Node(cutoff1,depth,1,player1,oppplayer1,temp,scoreboard,0,0,"root",maxsize*-1)
                if(y1==1):
                    temp1=deepcopy(GreedyBFS(root1))
                    for row in range(5):
                        for column in range(5):
                            trace_state.write(temp1.board[row][column])
                        trace_state.write('\r\n')
                        temp=deepcopy(temp1.board)
                elif(y1==2):
                    bestvalue=MinMax4(root1, depth, 1)
                    for child in root1.children:
                        if(child.minmax==bestvalue):
                            temp1=child
                            break
                    temp=deepcopy(temp1.board)
                    for row in range(5):
                        for column in range(5):
                            trace_state.write(temp1.board[row][column])
                        trace_state.write('\r\n')
                elif(y1==3):
                    bestvalue,x,y=AlphaBeta4(root1,depth,maxsize*-1,maxsize,1)
                    for child in root1.children:
                        if(child.minmax==bestvalue):
                            temp1=child
                            break
                    temp=deepcopy(temp1.board)
                    for row in range(5):
                        for column in range(5):
                            trace_state.write(temp1.board[row][column])
                        trace_state.write('\r\n')
                chuck=0
                for i in range(5):
                    for j in range(5):
                        if(temp[i][j]=="*"):
                            chuck=1
                if(chuck==0):
                    break
                player=2
            if(player==2):
                depth=0
                root2=Node(cutoff2,depth,1,player2,oppplayer2,temp,scoreboard,0,0,"root",maxsize*-1)
                if(y2==1):
                    temp2=deepcopy(GreedyBFS(root1))
                    for row in range(5):
                        for column in range(5):
                            trace_state.write(temp2.board[row][column])
                        trace_state.write('\r\n')
                        temp=deepcopy(temp2.board)
                elif(y2==2):
                    bestvalue=MinMax4(root2, depth, 1)
                    for child in root2.children:
                        if(child.minmax==bestvalue):
                            temp2=child
                            break
                    temp=deepcopy(temp2.board)
                    for row in range(5):
                        for column in range(5):
                            trace_state.write(temp2.board[row][column])
                        trace_state.write('\r\n')
                elif(y1==3):
                    bestvalue,x,y=AlphaBeta4(root2,depth,maxsize*-1,maxsize,1)
                    for child in root2.children:
                        if(child.minmax==bestvalue):
                            temp2=child
                            break
                    temp=deepcopy(temp2.board)
                    for row in range(5):
                        for column in range(5):
                            trace_state.write(temp2.board[row][column])
                        trace_state.write('\r\n')
                chuck=0
                for i in range(5):
                    for j in range(5):
                        if(temp[i][j]=="*"):
                            chuck=1
                if(chuck==0):
                    break
                player=1
        trace_state.truncate(trace_state.tell()-2)
        trace_state.close()
    #------------------------------------------------------------------------------------------------------------------
    else:
        playerchar=inputfile.readline()
        playerchar=playerchar.replace('\n', '')
        if(playerchar=="X"):
            oppplayer="O"
        else:
            oppplayer="X"
        cutoff=int(inputfile.readline())
        scoreboard=[]
        board=list()
        for i in range(5):
            scorerow=inputfile.readline()
            scoreboard.append([int(a) for a in scorerow.split()] )   
        for j in range(5):
            positionrow=inputfile.readline()
            board.append(list(positionrow.strip('\n')))
        root=Node(cutoff,depth,1,playerchar,oppplayer,board,scoreboard,0,0,"root",maxsize*-1)
        if(x==1):
            temp=GreedyBFS(root)
            next_state = open("next_state.txt", "w")
            for row in range(5):
                for column in range(5):
                    next_state.write(temp.board[row][column])
                if(row!=4):
                    next_state.write('\r\n')
            next_state.close()
        elif(x==2):        
            bestvalue=MinMax(root, depth, 1, 0, None)
            for child in root.children:
                if(child.minmax==bestvalue):
                    temp=child
                    break
            next_state = open("next_state.txt", "w")
            for row in range(5):
                for column in range(5):
                    next_state.write(temp.board[row][column])
                if(row!=4):
                    next_state.write('\r\n')
            next_state.close()
        elif(x==3):
            bestvalue,x,y=AlphaBeta(root,depth,maxsize*-1,maxsize,1,0,None)
            for child in root.children:
                if(child.minmax==bestvalue):
                    temp=child
                    break
            next_state = open("next_state.txt", "w")
            for row in range(5):
                for column in range(5):
                    next_state.write(temp.board[row][column])
                if(row!=4):
                    next_state.write('\r\n')
            next_state.close()


if __name__=="__main__" :
    main(sys.argv[1:])