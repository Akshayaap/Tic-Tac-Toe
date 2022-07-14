
import json


state_cross=json.load(open("states-cross.json",'r'))
state_naught=json.load(open("states-naught.json",'r'))

for key in state_cross.keys():
    state=state_cross[key]
    sum=0
    for i in state['next'].keys():
        sum+=state['next'][i]
    for i in state['next'].keys():
        state['next'][i]/=sum


for key in state_naught.keys():
    state=state_naught[key]
    sum=0
    for i in state['next'].keys():
        sum+=state['next'][i]
    for i in state['next'].keys():
        state['next'][i]/=sum

json.dump(state_cross,open("states-cross_n.json",'w'))
json.dump(state_naught,open("states-naught_n.json",'w'))