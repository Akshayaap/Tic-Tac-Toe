
import numpy as np
import random
import json


stats={"cross":0,"naught":0,"tie":0}
def ResetStats():
    global stats
    stats={"cross":0,"naught":0,"tie":0}

def GenKey(state):
    s=0
    p=0
    for i in range(3):
        for j in range(3):
            s+=(state[i][j]+1)*3**p
            p+=1
    return s


class StateSpace():

    def __init__(self,player):
        self.player=player
        f=open("states-{}.json".format('naught' if self.player == 1 else 'cross'),'r')
        self.states=json.load(f)
        #print(list(self.states.keys()))
        f.close()



class Game():

    def __init__(self):
        self.naught=StateSpace(1)
        self.cross=StateSpace(-1)
        self.reset()

    def step(self):

        if self.isWinner(1):
            return 1
        elif self.isWinner(-1):
            return -1
        if self.isOver():
            return 0
        key=GenKey(self.state)

        if self.turn == 1:
            #print(np.array(self.state))
            nextKey=random.choices(list(self.naught.states[str(key)]['next'].keys()),weights=list(self.naught.states[str(key)]['next'].values()))[0]
            self.state=self.naught.states[str(nextKey)]['state']
            self.trace.append(str(nextKey))
            self.turn = -1

        else:
            nextKey=random.choices(list(self.cross.states[str(key)]['next'].keys()),weights=list(self.cross.states[str(key)]['next'].values()))[0]
            self.state=self.cross.states[str(nextKey)]['state']
            self.trace.append(str(nextKey))
            self.turn=1
            
        #print(np.array(self.state))

        
        return 2

    def isWinner(self,player):
        for i in range(3):
            if self.state[i][0] == self.state[i][1] == self.state[i][2] == player:
                #print(r'*************{} Won**************'.format('Cross' if player is -1 else 'Naught'))
                return True
            if self.state[0][i] == self.state[1][i] == self.state[2][i] == player:
                #print(r'*************{} Won**************'.format('Cross' if player is -1 else 'Naught'))
                return True

        # Diagonals
        if self.state[0][0] == self.state[1][1] == self.state[2][2] == player:
            #print(r'*************{} Won**************'.format('Cross' if player is -1 else 'Naught'))
            return True

        if self.state[0][2] == self.state[1][1] == self.state[2][0] == player:
            #print(r'*************{} Won**************'.format('Cross' if player is -1 else 'Naught'))
            return True

        return False

    def isOver(self):
        unique, counts = np.unique(self.state, return_counts=True)
        d=dict(zip(unique, counts))
        try:
            if d[0]==0:
                #print('*************Game Over**************')
                return True
            else:
                return False
        except KeyError:
            #print('*************Game Over**************')
            return True

    def reset(self):

        #print('*************Game Reset**************')
        self.state=[
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
        self.turn=random.choice([-1,1])
        self.trace=[str(GenKey(self.state))]
        self.first=self.turn
        self.noerr=0
    def go(self):
        pass

    def train(self,iter):
        s=100

        for i in range(iter):
            if i % 2000==0:
                print(f"iterations: {i}", end='\r')
                if i % 100000==0:
                    fN=open('states-{}.json'.format('naught'),'w')
                    fC=open('states-{}.json'.format('cross'),'w')
                    json.dump(self.naught.states,fN)
                    json.dump(self.cross.states,fC)
                    fN.close()
                    fC.close()


            while True:
                s=self.step()
                if s== 0:
                    #print('*************Tie************')
                    self.reset()
                    break
                elif s==1:
                    self.updateN()
                    self.reset()
                    break
                elif s==-1:
                    self.updateC()
                    self.reset()
                    break
            
        fN=open('states-{}.json'.format('naught'),'w')
        fC=open('states-{}.json'.format('cross'),'w')
        json.dump(self.naught.states,fN)
        json.dump(self.cross.states,fC)
        fN.close()
        fC.close()

    def updateN(self):
        #print(self.trace)
        i=0
        n=len(self.trace)
        t=self.first
        while i <n-1:
            #print(self.cross.states[self.trace[i]]['next'])
            if t == -1:
                tmp=self.cross.states[self.trace[i]]['next']
                tmp[self.trace[i+1]]-=100
                i+=1
                t=1
            else:
                tmp=self.naught.states[self.trace[i]]['next']
                try:
                    tmp[self.trace[i+1]]+=100
                except KeyError:
                    self.noerr+=1
                    print('*************Errors Occured in Naught:{}************'.format(self.noerr))
                i+=1
                t=-1       

        

    def updateC(self):
        i=0
        n=len(self.trace)
        t=self.first
        while i <n-1:
            #print(self.cross.states[self.trace[i]]['next'])
            if t == 1:
                tmp=self.naught.states[self.trace[i]]['next']
                tmp[self.trace[i+1]]-=100
                i+=1
                t=-1
            else:
                tmp=self.cross.states[self.trace[i]]['next']
                try:
                    tmp[self.trace[i+1]]+=100
                except KeyError:
                    self.noerr+=1
                    print('*************Errors Occured in Cross:{}************'.format(self.noerr))
                i+=1
                t=1

    def playCross(self,i,j):
        if self.state[i][j]==0:
            self.state[i][j]=-1
            if self.isWinner(1):
                return 1
            elif self.isWinner(-1):
                return -1
            if self.isOver():
                return 0
            return 2
        else:
            return 3

    def playNaught(self,i,j):
        if self.state[i][j]==0:
            self.state[i][j]=1
            if self.isWinner(1):
                return 1
            elif self.isWinner(-1):
                return -1
            if self.isOver():
                return 0
            return 2
        else:
            return 3

    def playCrossAI(self):
        key=GenKey(self.state)
        nextKey=random.choices(list(self.cross.states[str(key)]['next'].keys()),weights=list(self.cross.states[str(key)]['next'].values()),k=1)[0]
        self.state=self.cross.states[str(nextKey)]['state']
        if self.isWinner(1):
            return 1
        elif self.isWinner(-1):
            return -1
        if self.isOver():
            return 0
        return 2

    def playNaughtAI(self):
        key=GenKey(self.state)
        nextKey=random.choices(list(self.naught.states[str(key)]['next'].keys()),weights=list(self.naught.states[str(key)]['next'].values()),k=1)[0]
        self.state=self.naught.states[str(nextKey)]['state']
        if self.isWinner(1):
            return 1
        elif self.isWinner(-1):
            return -1
        if self.isOver():
            return 0
        return 2

if __name__ == '__main__':
    game=Game()
    game.train(1000000000000)
        
