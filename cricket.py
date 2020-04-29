import random as rand
import csv
import copy
class player:
    def __init__(self,name,coun,bat,bowl,field):
        self.name=name
        self.coun=coun
        self.bat=bat
        self.bowl=bowl
        self.field=field
        self.totalruns=self.batscore=self.bowlruns=0
        self.totalwkts=self.bowlwkts=0
        self.pts=self.outs=self.totalbowlruns=self.totalballs=self.bowlballs=self.ballsfaced=self.totalballsfaced=0
        self.avg=0.00
    def batstat(self,runs,wkts,balls):
        self.batscore+=runs
        self.totalruns+=runs
        self.ballsfaced+=balls
        self.totalballsfaced+=balls
        self.outs+=wkts
    def bowlstat(self,runs,wkts,balls):
        self.bowlruns+=runs
        self.totalbowlruns+=runs
        self.bowlwkts+=wkts
        self.totalwkts+=wkts
        self.bowlballs+=balls
        self.totalballs+=balls
    def reset(self):
        
        self.batscore=0
        self.bowlballs=0
        self.bowlwkts=0
        self.bowlruns=0
        self.ballsfaced=0
        
    def calcpts(self):
        if self.outs>0:
            self.avg=round((self.totalruns/self.outs),2)
        else:
            self.avg=self.totalruns
        self.pts=int((2*self.totalruns)-(self.totalballsfaced)-(10*self.outs)+(30*self.totalwkts)+((self.totalballs*1.67)-self.totalbowlruns))
        k=0  


class team:
    def __init__(self,name,players):
        self.name=name
        self.players=copy.deepcopy(players)
        self.batorder=copy.deepcopy(players)
        self.bowlorder=copy.deepcopy(players)
        self.played=self.won=self.lost=0
        self.runscored=0
        self.runsconceded=0  
        self.nrr=0.00  
        self.pts=0
        self.nbowl=6
    def autoorder(self):    
        for l in range(11):
            for j in range(10-l):
                if(self.batorder[j].bat<self.batorder[j+1].bat):
                    self.batorder[j],self.batorder[j+1]=Switch(self.batorder[j],self.batorder[j+1])
                if(self.bowlorder[j].bowl<self.bowlorder[j+1].bowl):
                    self.bowlorder[j],self.bowlorder[j+1]=Switch(self.bowlorder[j],self.bowlorder[j+1])
        if self.bowlorder[5].bowl<50:
            self.nbowl=5
    def manualorder(self):
        
        t=self.bowlorder
        
        ch='y'
        while ch=='y':
            i=0
            for p in self.batorder:
                print(str(i+1).ljust(4),p.name.ljust(20),str(i+1).ljust(4),t[i].name.ljust(20))
                i+=1
            cho=input('order to change\n')           
            if cho=='bat':
                swap1=int(input("enter positions to swap"))-1
                swap2=int(input())-1
                self.batorder[swap1],self.batorder[swap2]=Switch(self.batorder[swap1],self.batorder[swap2])
            elif cho=='bowl':
                swap1=int(input("enter positions to swap"))-1
                swap2=int(input())-1
                t[swap1],t[swap2]=Switch(t[swap1],t[swap2])
                self.nbowl=int(input('no of bowlers?'))
            else:
                print('dumbfuck')
            ch=input('more?')
    def updateteamstats(self,teamscore,oppscore):
        self.runsconceded+=oppscore['runs']
        self.runscored+=teamscore['runs']
        self.played+=1
        if teamscore['runs']>oppscore['runs']:
            self.won+=1
            self.pts+=2
        elif teamscore['runs']<oppscore['runs']:
            self.lost+=1
        else:
            self.pts+=1
        self.nrr=float((self.runscored/self.runsconceded))
        for j in range(11):
            for i in range(11):
                if(self.batorder[j].name==self.players[i].name):
                    self.players[i].totalruns=self.batorder[j].totalruns
                    self.players[i].totalballsfaced=self.batorder[j].totalballsfaced
                    self.players[i].outs=self.batorder[j].outs
                else:
                    pass
                if(self.bowlorder[j].name==self.players[i].name):
                    self.players[i].totalwkts=self.bowlorder[j].totalwkts
                    self.players[i].totalballs=self.bowlorder[j].totalballs
                    self.players[i].totalbowlruns=self.bowlorder[j].totalbowlruns

                else:
                    pass

    def userrejects(self,rejects):
        
        for player in self.players:
            print(player.name+':'+str(player.pts))
            
        for player in self.players:
            ch=input('reject'+player.name+'?')
            if ch=='y':
                rejects.append(player)
        for p in rejects:
            self.players.remove(p)

        return rejects
    def rejects(self,rejects):
        for player in self.players:
            if player.pts<300:
                rejects.append(player)
                self.players.remove(player)
        
        return rejects


    def seasonreset(self):
        self.played=self.won=self.lost=self.pts=self.runscored=self.runsconceded=self.nrr=0
        for i in range(11):
            self.players[i].totalruns=self.batorder[i].totalruns=0
            self.players[i].totalballsfaced=self.batorder[i].totalballsfaced=0
            self.players[i].outs=self.batorder[i].outs=0
            self.players[1].avg=0.0  
            self.players[i].pts=0
            self.players[i].totalwkts=self.bowlorder[i].totalwkts=0
            self.players[i].totalballs=self.bowlorder[i].totalballs=0
            self.players[i].totalbowlruns=self.bowlorder[i].totalbowlruns=0
        self.batorder=copy.deepcopy(self.players)
        self.bowlorder=copy.deepcopy(self.players)


def Switch(st,nst):
    t=st
    st=nst
    nst=t
    return st,nst
def scoreupdate(teamscore,batsman,bowler,runs,wkts=0,balls=1):
    batsman.batstat(runs,wkts,balls)
    bowler.bowlstat(runs,wkts,balls)
    teamscore['runs']+=runs
    teamscore['wkts']+=wkts
    return teamscore
    
def scorecard(batsmen,bowlers,teamscore):
    print("BATTING TEAM")
    for i in range(11):
        print(batsmen[i].name.ljust(15),": ",str(batsmen[i].batscore)+'('+str(batsmen[i].ballsfaced)+')')
    print("bowling TEAM\n","name".ljust(20),"overs".ljust(6),"wkts".ljust(6),"runs")
    for i in range(11):
        if bowlers[i].bowlballs>0:
            print(bowlers[i].name.ljust(20),str(int((bowlers[i].bowlballs)/6))+'.'+str((bowlers[i].bowlballs)%6)," ".ljust(5),str(bowlers[i].bowlwkts).ljust(6),str(bowlers[i].bowlruns).ljust(6))  
        else:
            pass
    print("the final score is:",teamscore['runs']," for ",teamscore['wkts'])
def summary(inn1,inn2,team1,team2):
   
    p1=copy.deepcopy(team1.batorder)
    p2=copy.deepcopy(team2.batorder)
    b1=copy.deepcopy(team1.bowlorder)
    b2=copy.deepcopy(team2.bowlorder)
    for i in range(2):
        for j in range(1+i,11):
            if p1[11-j].batscore>p1[10-j].batscore:
                p1[11-j],p1[10-j]=Switch(p1[11-j],p1[10-j])
            else:
                pass
        
            if p2[11-j].batscore>p2[10-j].batscore:
                p2[11-j],p2[10-j]=Switch(p2[11-j],p2[10-j])
            else:
                pass
        
            if b1[11-j].bowlwkts>b1[10-j].bowlwkts or (b1[11-j].bowlwkts==b1[10-j].bowlwkts and b1[11-j].bowlruns<b1[10-j].bowlruns):
                b1[11-j],b1[10-j]=Switch(b1[11-j],b1[10-j])
            else:
                pass
        
            if (b2[11-j].bowlwkts>b2[10-j].bowlwkts) or (b2[11-j].bowlwkts==b2[10-j].bowlwkts and b2[11-j].bowlruns<b2[10-j].bowlruns):
                b2[11-j],b2[10-j]=Switch(b2[11-j],b2[10-j])
            else:
                pass
        
    print("\t", team1.name ,"innings:",inn1,'\n',p1[0].name.ljust(20),":",str(p1[0].batscore)+'('+str(p1[0].ballsfaced)+')',"\t",b2[0].name.ljust(20),":",b2[0].bowlwkts,"for",b2[0].bowlruns,"\n",p1[1].name.ljust(20),":",str(p1[1].batscore)+'('+str(p1[1].ballsfaced)+')',"\t",b2[1].name.ljust(20),":",b2[1].bowlwkts,"for",b2[1].bowlruns,"\n")
    print("\t", team2.name ,"innings:",inn2,'\n',p2[0].name.ljust(20),":",str(p2[0].batscore)+'('+str(p2[0].ballsfaced)+')',"\t",b1[0].name.ljust(20),":",b1[0].bowlwkts,"for",b1[0].bowlruns,"\n",p2[1].name.ljust(20),":",str(p2[1].batscore)+'('+str(p2[1].ballsfaced)+')',"\t",b1[1].name.ljust(20),":",b1[1].bowlwkts,"for",b1[1].bowlruns,"\n")
    
def showlineups(team1,team2):
    for i in range(11):
        print(team1.batorder[i].name.ljust(15),team2.batorder[i].name)
def play(batsman,bowler,fielders):
    stroke=rand.randint(1,batsman.bat+1)
    ball=rand.randint(1,bowler.bowl+1)
    fielding=rand.randint(1,fielders[rand.randint(0,10)].field+1)
    if stroke<int((ball+fielding)/2-50):
        return -1
    elif stroke<int((ball+fielding)/2-10):
        return 0
    elif stroke<int((ball+fielding)/2+11):
        return(rand.choice([0,1]))
    elif stroke<int((ball+fielding)/2+51):
        return(rand.choice([2,3]))
    elif stroke>int((ball+fielding)/2+50):
        return rand.choice([4,6])

def playinnings(batsmen,fielders,nbowl):
    striker=0
    nonstriker=1
    curbowl=0
    teamscore={'runs':0,'wkts':0}
    nextbat=2
    for o in range(1,21):
        
        
        for j in range(6):
            if(teamscore['wkts']==10):
                break
            x=play(batsmen[striker],fielders[curbowl],fielders)
            
            if(x!=-1):
                teamscore=scoreupdate(teamscore,batsmen[striker],fielders[curbowl],x,0,1)
                if(x%2!=0):
                    striker,nonstriker=Switch(striker,nonstriker)
                

            else:
                teamscore=scoreupdate(teamscore,batsmen[striker],fielders[curbowl],0,1,1)
                striker=nextbat
                nextbat+=1
        striker,nonstriker=Switch(striker,nonstriker)
        curbowl=(o%(nbowl))
          
        if teamscore['wkts']==10:
            break    
    scorecard(batsmen,fielders,teamscore)
    print("after",o,"overs")
    return teamscore  
def siminnings(batsmen,fielders,nbowl):
    striker=0
    nonstriker=1
    curbowl=0
    teamscore={'runs':0,'wkts':0}

    for o in range(1,21):
        if(striker>nonstriker):
            lastbat=striker
        else:
            lastbat=nonstriker
        
        for j in range(6):
            if(teamscore['wkts']==10):
                break
            x=play(batsmen[striker],fielders[curbowl],fielders)
            
            if(x!=-1):
                teamscore=scoreupdate(teamscore,batsmen[striker],fielders[curbowl],x)
                if(x%2!=0):
                    striker,nonstriker=Switch(striker,nonstriker)
                

            else:
                teamscore=scoreupdate(teamscore,batsmen[striker],fielders[curbowl],0,1)
                striker=lastbat+1
        
        striker,nonstriker=Switch(striker,nonstriker)
        curbowl=(o%nbowl)
          
        if teamscore['wkts']==10:
            break    
    print(teamscore,"after",o,"overs")
    return teamscore  
def cricketmatch(team1,team2):
    print("1.play\n2.sim")
    ch=int(input())
    if(ch==1):
        showlineups(team1,team2)
        innings1score=playinnings(team1.batorder,team2.bowlorder,team2.nbowl)
        innings2score=playinnings(team2.batorder,team1.bowlorder,team1.nbowl)
    
    
        team1.updateteamstats(innings1score,innings2score)

        
        team2.updateteamstats(innings2score,innings1score)
        print(team1.name,"score:",innings1score,"\t",team2.name,"score:",innings2score)
        for i in range(11):  
            team1.batorder[i].reset()
            team2.batorder[i].reset()
            team2.bowlorder[i].reset()
            team1.bowlorder[i].reset()
        
        if (innings1score['runs']>innings2score['runs']):
            print('\t\t------------\n\t',team1.name,"WON")
            return team1,team2
        elif (innings1score['runs']<innings2score['runs']):
            print('\t\t------------\n\t',team2.name,"WON")
            return team2,team1
        else:
            return team1,team2
    else:
        showlineups(team1,team2)
        innings1score=siminnings(team1.batorder,team2.bowlorder,team2.nbowl)
        innings2score=siminnings(team2.batorder,team1.bowlorder,team1.nbowl)
    

        team1.updateteamstats(innings1score,innings2score)

        
        team2.updateteamstats(innings2score,innings1score)
        summary(innings1score,innings2score,team1,team2)
        print(team1.name,"score:",innings1score,"\t",team2.name,"score:",innings2score)
        for i in range(11):  
            team1.batorder[i].reset()
            team2.batorder[i].reset()
            team2.bowlorder[i].reset()
            team1.bowlorder[i].reset()
        
        if (innings1score['runs']>innings2score['runs']):
            print('\t\t------------\n\t',team1.name,"WON")
            return team1,team2
        elif (innings1score['runs']<innings2score['runs']):
            print('\t\t------------\n\t',team2.name,"WON")
            return team2,team1
        else:
            return team1,team2

    
# teams=[]
# createteams()
# cricketmatch(teams[5],teams[7])


