import auction
import cricket as cric
import copy
import csv
# added to github
def instruction():
    print("\t\t T20 Cricket league simulator\n ".capitalize())
    print("\n\ninstructions".capitalize())
    print("1.the game has 2 stages\n\ti.the auction\n\tii.the league\nsimilair to the structure of the ipl\n2.first pick your team by typing the abbreviation of ipl teams\n3.the auction:the auction begins by displaying the number of players and then proceed to display the players.After the current player to be bid on is displayed you can type in the maximum bid for that player.Your starting budget 1540 coins.Each auction round consists of 8 players being bid on and after each round you can choose to view yor existing team and budget when prompted.\n4.the league:before every match you have the option of rearranging your team's batting and bowling order.You can also view the points table and the players' stats table or your team's detailed stats.When you decide to play a match you have 2 options\n\t1.detailed scorecard\n\t2.summary ")
def createteams():
    teams=[]
    with open('teams.csv','r') as teamfile:
        play=cric.player('i','j',1,1,1)
        teamread=csv.DictReader(teamfile,play.__dict__.keys())
        for i in range(8):
            n=teamfile.readline()
            players=[]
            for l in range(11):
                play.__dict__=teamread.__next__()
                # line=teamfile.readline().split(',')
                # p=cric.player(line[0],line[1],int(line[2]),int(line[3]),int(line[4]))
                # players.append(p)
                # play.calcpts()
                play.batscore=int(play.batscore)
                play.bat=int(play.bat)
                play.bowl=int(play.bowl)
                play.field=int(play.field)
                play.bowlruns=int(play.bowlruns)
                play.outs=int(play.outs)
                play.bowlwkts=int(play.bowlwkts)
                play.avg=float(play.avg)
                play.pts=int(play.pts)
                play.bowlballs=int(play.bowlballs)

                play.ballsfaced=int(play.ballsfaced)
                players.append(copy.deepcopy(play))
            teams.append(cric.team(n[:-1],players))
    for t in teams:
        t.autoorder()
    return teams

def showtable(tableteams):
    print("pos".ljust(7),"team".ljust(7),"played".ljust(7),"won".ljust(7),"lost".ljust(7),"pts".ljust(7),"nrr".ljust(7))
    for i in range(8):
        print(str(i+1).ljust(7),tableteams[i].name.ljust(7),str(tableteams[i].played).ljust(7),str(tableteams[i].won).ljust(7),str(tableteams[i].lost).ljust(7),str(tableteams[i].pts).ljust(7),str(tableteams[i].nrr).ljust(7))
def updatetable(tableteams):
    for i in range(8):
        for j in range(7-i):
            if ((tableteams[j].pts<tableteams[j+1].pts) or (tableteams[j].pts==tableteams[j+1].pts and tableteams[j].nrr<tableteams[j+1].nrr)):
                tableteams[j],tableteams[j+1]=cric.Switch(tableteams[j],tableteams[j+1])
def chooseteam(teams,username):

    for t in teams:
        if (t.name==username):
            return t
def userorder(team):
    team.manualorder()
def playerstats(teams,mvp,batstats,bowlstats):
    
    for p in mvp:
        p.calcpts()
    for i in range(len(batstats)):
        for j in range(len(batstats)-1-i):
            if batstats[j].totalruns<batstats[j+1].totalruns:
                batstats[j],batstats[j+1]=cric.Switch(batstats[j],batstats[j+1])
            if bowlstats[j].totalwkts<bowlstats[j+1].totalwkts or (bowlstats[j].totalwkts==bowlstats[j+1].totalwkts and bowlstats[j].totalbowlruns>bowlstats[j+1].totalbowlruns):
                bowlstats[j],bowlstats[j+1]=cric.Switch(bowlstats[j],bowlstats[j+1])
            if mvp[j].pts<mvp[j+1].pts:
                mvp[j],mvp[j+1]=cric.Switch(mvp[j],mvp[j+1])
    print("pos","mvp".ljust(20),"pts".ljust(5),"pos","batsman".ljust(20),"runs".ljust(5),"pos","bowler".ljust(20),"wkts")
    for l in range(10):
        print(str(l+1).ljust(3),mvp[l].name.ljust(20),str(mvp[l].pts).ljust(5),str(l+1).ljust(3),batstats[l].name.ljust(20),str(batstats[l].totalruns).ljust(5),str(l+1).ljust(3),bowlstats[l].name.ljust(20),str(bowlstats[l].totalwkts).ljust(5))   
def teamstats(team):
    for p in team.players:
        p.calcpts()
        print(p.name.ljust(20),":",str(p.pts).ljust(5),(str(p.totalruns)+'('+str(p.totalballsfaced)+')').ljust(9),str(p.avg).ljust(8),(str(p.totalwkts)+'-'+str(p.totalbowlruns)).ljust(8),int(p.totalballs/6),'.',p.totalballs%6)
def playleague(teams,tableteams,userteam,mvp,batstats,bowlstats):
    for t in teams:
        t.autoorder()
    
    # userteam.manualorder()
    ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
    while ch!=1:
        if ch==1:
            break
        elif ch==2:
            showtable(tableteams)
        elif ch==4:
            teamstats(userteam)
        elif ch==5:
            userorder(userteam)                        
        else:
            playerstats(teams,mvp,batstats,bowlstats)
        ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
    for i in range(8):
        for j in range(8):
            if(i!=j):
                if(ch==1):        
                    cric.cricketmatch(teams[i],teams[j])
                    tableteams=copy.deepcopy(teams)
                    updatetable(tableteams)
                    ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
                    while ch!=1:
                        if ch==1:
                            break
                        elif ch==2:
                            showtable(tableteams)
                        elif ch==4:
                            teamstats(userteam)
                        elif ch==5:
                            userorder(userteam)                        
                        else:
                            playerstats(teams,mvp,batstats,bowlstats)
                        ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
def playknockouts(teams,tableteams,userteam,mvp,batstats,bowlstats):
    tableteams=copy.deepcopy(teams)
    updatetable(tableteams)
    t1=tableteams[0].name
    t2=tableteams[1].name
    t3=tableteams[2].name
    t4=tableteams[3].name
    qual1=qual2=lqual1=elim=final=pos1=pos2=pos3=pos4=None    
    for i in range(8):
        if(teams[i].name==t1):
            pos1=teams[i]
        if(teams[i].name==t2):
            pos2=teams[i]
        if(teams[i].name==t3):
            pos3=teams[i]
        if(teams[i].name==t4):
            pos4=teams[i]
    
    winner=third=fourth=runner=None
    ch=1
    if(ch==1):        
        qual1,lqual1=cric.cricketmatch(pos1,pos2)
        tableteams=copy.deepcopy(teams)
        updatetable(tableteams)
        ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
        while ch!=1:
            if ch==1:
                break
            elif ch==2:
                showtable(tableteams)
            elif ch==4:
                teamstats(userteam)
            elif ch==5:
                userorder(userteam)
            else:
                playerstats(teams,mvp,batstats,bowlstats)
            ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
    # if pos1==qual1:
    #     lqual1=pos2
    # else:
    #     lqual1=pos1
    if(ch==1):        
        elim,fourth=cric.cricketmatch(pos3,pos4)
        tableteams=copy.deepcopy(teams)
        updatetable(tableteams)
        ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
        while ch!=1:
            if ch==1:
                break
            elif ch==2:
                showtable(tableteams)
            elif ch==4:
                teamstats(userteam)
            elif ch==5:
                userorder(userteam)
            else:
                playerstats(teams,mvp,batstats,bowlstats)
            ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
    if(ch==1):        
        qual2,third=cric.cricketmatch(lqual1,elim)
        tableteams=copy.deepcopy(teams)
        updatetable(tableteams)
        ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
        while ch!=1:
            if ch==1:
                break
            elif ch==2:
                showtable(tableteams)
            elif ch==4:
                teamstats(userteam)
            elif ch==5:
                userorder(userteam)
            else:
                playerstats(teams,mvp,batstats,bowlstats)
            ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
    if(ch==1):        
        winner,runner=cric.cricketmatch(qual1,qual2)
        tableteams=copy.deepcopy(teams)
        updatetable(tableteams)
        ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
        while ch!=1:
            if ch==1:
                break
            elif ch==2:
                showtable(tableteams)
            elif ch==4:
                teamstats(userteam)
            elif ch==5:
                userorder(userteam)
            else:
                playerstats(teams,mvp,batstats,bowlstats)
            ch=int(input("1.next match\n2.showtable\n3.showplayerstats\n4.teamstats\n5.reorder team"))
    # tableteams=copy.deepcopy(teams)
    tableteams[0]=copy.deepcopy(winner)
    tableteams[1]=copy.deepcopy(runner)
    tableteams[2]=copy.deepcopy(third)
    tableteams[3]=copy.deepcopy(fourth)
    showtable(tableteams)
    print(winner.name,"is the winner")
    return tableteams
def finish(teams):
    with open('teams.csv','w',newline='') as teamfile:
        for i in range(8):
            teamfile.writelines(teams[i].name+'\n')
            teamwriter=csv.DictWriter(teamfile,teams[i].players[0].__dict__.keys())
            for o in range(11):
                teamwriter.writerow(teams[i].players[o].__dict__)         

def season():
    instruction()
    username=input('choose team')
    for i in range(9999):
        if i%3==0 :
            auction.auction(username)
        elif i%3!=0 :
            teams=createteams()
            auction.retainauction(teams,username)
        else:
            pass
        teams=createteams()
        for team in teams:
            team.seasonreset()
        mvp=[]
        batstats=[]
        bowlstats=[]
        for t in teams:
            for p in t.players:
                p.calcpts()
                mvp.append(p)
                batstats.append(p)
                bowlstats.append(p)
        
        tableteams=copy.deepcopy(teams)
        user=chooseteam(teams,username)
        showtable(tableteams)
        playleague(teams,tableteams,user,mvp,batstats,bowlstats)
        tableteams=playknockouts(teams,tableteams,user,mvp,batstats,bowlstats)
        
        with open('seasons.csv','a') as seasonfile:
            line='\n{0[0].name},{0[1].name},{0[2].name},{0[3].name},{0[4].name},{0[5].name},{0[6].name},{0[7].name},{1[0].name},{2[0].name},{3[0].name}'.format(tableteams,mvp,batstats,bowlstats)
            seasonfile.write(line)
        
        finish(teams)
        
season()

