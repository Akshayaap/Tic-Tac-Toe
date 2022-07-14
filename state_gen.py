
import numpy as np
import random
import time
import json


def GenKey(state):
    s=0
    p=0
    for i in range(3):
        for j in range(3):
            s+=(state[i][j]+1)*3**p
            p+=1
    return s



class State():
    def __init__(self,key,arr,player):
        self.player=player
        self.key=key
        self.state=arr
        unique,counts =np.unique(self.state,return_counts=True)
        self.d=dict(zip(unique, counts))
        self.next={}

        try: 
            self.d[0]=self.d[0]
        except KeyError:
            self.d[0]=0
        
        try:
            self.d[1]=self.d[1]
        except KeyError:
            self.d[1]=0

        try:
            self.d[-1]=self.d[-1]
        except KeyError:
            self.d[-1]=0
        
        try:
            if self.d[-1]==self.d[1]:
                for i in range(3):
                    for j in range(3):
                        temp=np.array(self.state)
                        if self.state[i][j] == 0:
                            temp[i][j]=self.player
                            self.next[int(GenKey(temp))]=1

        except KeyError:
            pass

        try:
            if self.d[-1]==self.d[1]+1:
                for i in range(3):
                    for j in range(3):
                        temp=np.array(self.state)
                        if self.state[i][j] == 0:
                            temp[i][j]=self.player
                            self.next[int(GenKey(temp))]=1

        except KeyError:
            pass

        try:
            if self.d[0]==9:
                    for i in range(3):
                        for j in range(3):
                            temp=np.array(self.state)
                            if self.state[i][j] == 0:
                                temp[i][j]=self.player
                                self.next[int(GenKey(temp))]=1
        except KeyError:
            pass

        try:
            if self.d[1]==self.d[-1]+1:
                for i in range(3):
                    for j in range(3):
                        temp=np.array(self.state)
                        if self.state[i][j] == 0:
                            temp[i][j]=self.player
                            self.next[int(GenKey(temp))]=1

        except KeyError:
            pass

        try:
            if self.d[1]==1 and self.d[0]==8:
                for i in range(3):
                    for j in range(3):
                        
                        temp=np.array(self.state)
                        if self.state[i][j] == 0:
                            temp[i][j]=self.player
                            self.next[int(GenKey(temp))]=1

        except KeyError:
            pass

        try:
            if self.d[-1]==1 and self.d[0]==8:
                for i in range(3):
                    for j in range(3):
                        
                        temp=np.array(self.state)
                        if self.state[i][j] == 0:
                            temp[i][j]=self.player
                            self.next[int(GenKey(temp))]=1

        except KeyError:
            pass

        self.nextKeys=list(self.next.keys())
        self.totalNext=len(self.nextKeys)
    def getNext(self):
        return random.choice(self.nextKeys)





class StateSpaceGen():

    def __init__(self,player):
        self.player=player
        self.states={}
        for i in range(-1,2):
            for j in range(-1,2):
                for k in range(-1,2):

                    for l in range(-1,2):   
                        for m in range(-1,2):
                            for n in range(-1,2):

                                for o in range(-1,2):
                                    for p in range(-1,2):
                                        for q in range(-1,2):
    
                                            arr=np.array([
                                                [i, j, k],
                                                [l, m, n],
                                                [o, p, q]
                                            ])
                                            key=GenKey(arr)
                                            unique, counts = np.unique(arr, return_counts=True)
                                            d=dict(zip(unique, counts))

                                            try:
                                                d[0]=d[0]
                                            except KeyError:
                                                d[0]=0
                                            
                                            try:
                                                d[1]=d[1]
                                            except KeyError:
                                                d[1]=0

                                            try:
                                                d[-1]=d[-1]
                                            except KeyError:
                                                d[-1]=0
                                                

                                            try:
                                                if d[1]==(d[-1]+1):
                                                    self.states[key]=State(key,arr,player)
                                            except KeyError:
                                                    pass


                                            try:
                                                if d[1]==d[-1]:
                                                    self.states[key]=State(key,arr,player)
                                            except KeyError:
                                                    pass

                                            try:
                                                if d[-1]==(d[1]+1):
                                                    self.states[key]=State(key,arr,player)
                                            except KeyError:
                                                    pass

                                            try:
                                                if d[0] == 9:
                                                    self.states[key]=State(key,arr,player)
                                            except KeyError as err:
                                                pass

                                            try:
                                                if key==9841:
                                                    self.states[key]=State(key,arr,player)
                                            except KeyError:
                                                pass

                                            try:
                                                if d[1]==1 and d[0]==8:
                                                    self.states[key]=State(key,arr,player)
                                            except KeyError:
                                                pass

                                            try:
                                                if d[-1]==1 and d[0]==8:
                                                    self.states[key]=State(key,arr,player)
                                            except KeyError:
                                                pass
        
        all_state={}
        for i in self.states.keys():
            all_state[int(i)]={"state":[[int(k) for k in j] for j in self.states[i].state],"next":self.states[i].next}
        f=open('states-{}.json'.format('cross' if self.player==-1 else 'naught'),'w')
        json.dump(all_state,f)
        f.close()

    def getState(self,key):
        return self.states[key]
        

def GenStates():
    StateSpaceGen(1)
    StateSpaceGen(-1)

GenStates()