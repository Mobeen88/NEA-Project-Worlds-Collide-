import random

'''
class basket_Players:
    def __init__(self,name):
        self.name = name

    def GetName(self):
        return self.name

    def __str__(self):
        return self.name


class team:
    def __init__(self,name):
        self.name = name
        self.score = 0
        self.players = []

    def addPlayer(self,newPlayer):
        self.newPlayer = newPlayer
        self.players.append(self.newPlayer)

    def setScore(self):
        self.score += 1

    def showPlayers(self):
        for row in self.players:
            print(row)


Lakers = team("Lakers")

players1 = basket_Players("Bob")
Lakers.addPlayer(players1)

players2 = basket_Players("Jack")
Lakers.addPlayer(players2)

players3 = basket_Players("Mo")
Lakers.addPlayer(players3)

print(Lakers.showPlayers())

def complete(Lakers,Bull):
    score = 0
    r = [Lakers, Bull]
    
    random1 = random.choice(r)
    print(random1)
    if random1 == "Lakers":
        print("winner")
        score += 1
        print(score)

#Main program
Laker = "Lakers"
Bulls = "Bull"
complete(Laker, Bulls)


name = input("Enter name: ")
num = int(input("Enter num: "))
print(name + str(num))
'''