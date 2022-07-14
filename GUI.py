
import re
from tkinter import *
from tkinter import messagebox
from Game import *

root=Tk()
root.title('Tic Tac Toe')
game=Game()
def click(i,j):
    global turn
    global game
    if turn==-1:
        r=game.playCross(i,j)
        render()
        if r==1 :
            messagebox.showinfo('Tic Tac Toe','I Won!')
            reset()
            return
        elif r==-1:
            messagebox.showinfo('Tic Tac Toe','You Won!')
            reset()
            return
        elif r==0:
            messagebox.showinfo('Tic Tac Toe','Draw!')
            reset()
            return
        elif r==3:
            messagebox.showinfo('Tic Tac Toe','Invalid Move!')
            return
        turn=1

    if turn==1:
        r=game.playNaughtAI()
        render()
        if r==1 :
            messagebox.showinfo('Tic Tac Toe','I Won!')
            reset()
            return
        elif r==-1:
            messagebox.showinfo('Tic Tac Toe','You Won !')
            reset()
            return
        elif r==0:
            messagebox.showinfo('Tic Tac Toe','Draw!')
            reset()
            return
        elif r==3:
            messagebox.showinfo('Tic Tac Toe','Invalid Move!')
            return
        turn=-1


def reset():
    global turn
    global game
    game.reset()
    turn=game.first
    render()
    if(turn==1):
        messagebox.showinfo('Tic Tac Toe','I will play first')
        r=game.playNaughtAI()
        render()
        turn=-1
    else:
        messagebox.showinfo('Tic Tac Toe','You will play first')
    render()

def render():
    global turn
    global game
    for i in range(3):
        for j in range(3):
            if(game.state[i][j]==-1):
                bs[i][j].config(text='X')
            elif game.state[i][j]==1:
                bs[i][j].config(text='O')
            else:
                bs[i][j].config(text=' ')

bs=[]
for i in range(3):
    bs.append([])
    for j in range(3):
        bs[i].append(Button(root,text='X',command=lambda i=i,j=j:click(i,j)))
        bs[i][j].config(font=('Helvetica', 20))
        bs[i][j].grid(row=i,column=j)
        bs[i][j].config(height=3,width=10)
        bs[i][j].config(bg='white')


turn=game.first
reset()

root.mainloop()

