import csv

import random as rand
import cricket as cric

class bidder:
    
    def __init__(self,name,battgt=700,bowltgt=500,fieldtgt=900):
         self.budget=1540
         self.boughtplayers=[]
         self.batval=self.battgt=battgt
         self.bowlval=self.bowltgt=bowltgt
         self.fieldval=self.fieldtgt=fieldtgt
         self.name=name
         self.nplayers=0
         self.maxbid=0
    def set_targets(self,player):
        if ((self.batval-player.bat)>0):
            self.batval-=player.bat
        else:
            self.batval=0
        if ((self.bowlval-player.bowl)>0):
            self.bowlval-=player.bowl
        else:
            self.bowlval=0
        if ((self.fieldval-player.field)>0):
            self.fieldval-=player.field
        else:
            self.fieldval=0
    def usermaxbid(self,player):
        self.maxbid=int(input('{} :'.format(player.name)))
        if(self.nplayers==11):
            self.maxbid=0
        else:
            pass
    def bid(self,curbid):
        if curbid<self.maxbid and curbid<self.budget:
            return 1
        else:
            return 0
    def calmaxbid(self,player):
        if(self.nplayers==11):
            self.maxbid=0
        else:
            if(player.bowl>=50):
                self.maxbid=((player.bat*self.batval/self.battgt)+(player.bowl*self.bowlval/self.bowltgt)+(player.field*self.fieldval/self.fieldtgt))
            else:
                self.maxbid=((player.bat*self.batval/self.battgt)+(player.field*self.fieldval/self.fieldtgt))
    def addplayer(self,player,bidamt):
        self.boughtplayers.append(player)
        self.nplayers+=1
        self.budget-=bidamt
        self.set_targets(player)
    def showplayers(self):
        print("bidder:",self.name,"\trem budget:",self.budget,"players:",self.nplayers,"\n")
        teamovr=teambat=teambowl=teamfield=0
        for j in range(self.nplayers):
            x=self.boughtplayers[j]
            print(x.name)
            teambat+=x.bat
            teambowl+=x.bowl
            teamfield+=x.field
        teamovr=(teamfield+teambowl+teambat)/3
        print("teambat:",teambat,"\tteambowl",teambowl,"/tteamfieald:",teamfield,"/tteamovr:",teamovr)

    def resettgt(self):
        self.fieldtgt=self.fieldval
        self.battgt=self.batval
        self.bowltgt=self.bowlval




def createpl():
    i=0
    players={'stars':[],'tier1':[],'tier2':[]}
    with open('players.csv','r') as pfile:
        readfile=csv.reader(pfile)
        
        for line in readfile:
            t=cric.player(line[0],line[1],int(line[2]),int(line[3]),int(line[4]))
            players[str(line[5])].append(t)
            i+=1
    rand.shuffle(players['stars'])
    rand.shuffle(players['tier1'])
    rand.shuffle(players['tier2'])
    return players
        
def biddinground(player,bidders,user):
    baseprice=1
    # if (player.ty>90):
    #     baseprice=80
    # elif (player.bat>80):
    #     baseprice=60
    # else:
    #     baseprice=30
    for bidder in bidders:
        if bidder is user:
            bidder.usermaxbid(player)
        else:
            bidder.calmaxbid(player)
    bidwinner=-1
    curbid=(baseprice-1)
    bidno=0
    passes=0
    while ((passes<7 and curbid>=baseprice) or (passes<8 and curbid<baseprice)):      
        n=(bidno%8)
        if (bidders[n].bid(curbid)==1):
            curbid+=bidders[n].bid(curbid)
            bidwinner=n
            passes=0
        else:
            passes+=1
        bidno+=1
    if(curbid>=baseprice):
        print(player.name,"was sold at",curbid,"to bidder",bidwinner,"after",bidno,"bids")
        x = bidders[bidwinner]
        x.addplayer(player,curbid)
    else:
        print(player.name,"was unsold")

def createbidders():
    bidders=[]
    with open('biddername.csv','r') as bfile:
        i=0
        rfile=csv.reader(bfile)
        for line in rfile:
            bidders.append(bidder(line[0],int(line[1]),int(line[2]),int(line[3])))
        return bidders

def choosebid(username,bidders):
    for b in bidders:
        if b.name==username:
            # b=bidder(username,int(input('bat')),int(input('bowl')),int(input('field')))
            return b

def playauction(players,bidders,user):
    for l in range(len(players['stars'])):
        biddinground(players['stars'][l],bidders,user)
        if l%8==0:
            ch=input('disp?')
            if ch=='y':
                user.showplayers()

    for bidder in bidders:
        bidder.resettgt()
    for l in range(len(players['tier1'])):
        biddinground(players['tier1'][l],bidders,user)
        if l%8==0:
            ch=input('disp?')
            if ch=='y':
                user.showplayers()
    for bidder in bidders:
        bidder.resettgt()

    for l in range(len(players['tier2'])):
        biddinground(players['tier2'][l],bidders,user)

def finishauction(bidders):
    with open('teams.csv','w',newline='') as teamfile:
        for i in range(8):
            bidders[i].showplayers()
            teamfile.writelines(bidders[i].name+'\n')
            teamwriter=csv.DictWriter(teamfile,bidders[i].boughtplayers[0].__dict__.keys())
            for o in range(11):
                teamwriter.writerow(bidders[i].boughtplayers[o].__dict__)         

def auction(username):
    bidders=createbidders()
    
    user=choosebid(username,bidders)
    players=createpl()
    playauction(players,bidders,user)
    finishauction(bidders)

def retainauction(teams,username):
    bidders=createbidders()
    
    user=choosebid(username,bidders)
    rejects=[]
    for team in teams:
        if team.name==user.name:
            rejects=team.userrejects(rejects)
        else:
            rejects=team.rejects(rejects)
    rand.shuffle(rejects)
    print(len(rejects))
    for bidder in bidders:
        for team in teams:
            if team.name==bidder.name:
                bidder.boughtplayers=team.players
                bidder.nplayers=len(bidder.boughtplayers)
                bidder.budget=140*(11-bidder.nplayers)
    for l in range(len(rejects)):
        biddinground(rejects[l],bidders,user)
        if l%8==0:
            ch=input('disp?')
            if ch=='y':
                user.showplayers()
    finishauction(bidders)
auction('csk')