from random import uniform, randint
import matplotlib.pyplot as plt
import random
import numpy as np

random.seed(2)

class Toplogic():
    def __init__(self, Age, Industry):
        self.Age = Age
        self.Industry = Industry

class Agent():
    def __init__(self, S, C, R, Neighbors):
        self.Score = S
        self.Competitiveness = C
        self.Resistance = R
        self.Neighbors = Neighbors

def Find_Neighbors(NumAgent):
    Network = []
    # Initialize the population according to NumAgent
    for i in range(0, NumAgent):

        #  Suppose we want to study workers aged 20-70 and divide them into age groups
        Age = randint(20, 70)
        Age_Group = int((Age - 20) / 10)

        # Suppose there are five occupations
        # (representing computer, doctor, lawyer, teacher and farmer respectively)
        Industry = randint(0, 4)

        Network.append(Toplogic(Age_Group, Industry))
    return Network

def Generate_agent(Network):
    Agents = []
    Neighbors = []
    # Each Agent has a random value of Competitiveness and Resistance
    for i in range(len(Network)):
        Competitive = randint( 0, 7 )
        Prob_Competitive = Competitive / 7

        Resistance = randint( 0, 7 )
        Prob_Resistance = Resistance / 7

        for j in range(len(Network)):
            if Network[j].Age == Network[i].Age or Network[j].Industry == Network[i].Industry:
                Neighbors.append( Network[j] )
        Agents.append(Agent(0, Prob_Competitive, Prob_Resistance, Neighbors))
        Neighbors = [] # Here can not use list.clear()
    return Agents

# print agents' feature
def Agent_print(j, Agents):
    print("Score: " + str(Agents[j].Score))
    print("Competitiveness: " + str( Agents[j].Competitiveness ) )
    print("Resistance: " + str( Agents[j].Resistance ) )
    print("Neighbors: " + str(Agents[j].Neighbors))

# Norm Game
def Norm_Game(Agents):
    # Traverse the entire list of Agents
    N = NumAgent
    deserter = []
    for u in range(len(Agents)):
        # randomly initialise probability
        prob = random.uniform(0, 1)
        compete = Agents[u].Competitiveness
        if prob < compete:
            Agents[u].Score += -2
            for y in range(len(Agents)):
                # Search the same value in neighbors
                for i in range( len( Agents[y].Neighbors ) ):
                    for j in range( len( Agents[u].Neighbors ) ):
                        # only can be seen by their neighbors
                        if y != u:
                            Agents[y].Score += -2
                            if Agents[y].Neighbors[i].Age == Agents[u].Neighbors[j].Age or \
                                Agents[y].Neighbors[i].Industry == Agents[u].Neighbors[j].Industry:
                                if prob < Agents[y].Resistance:
                                    Agents[u].Score += -11
                                    Agents[y].Score += -1.5
                                else:
                                    deserter.append(y)
    return Agents, deserter

def Iteration(Agents, epoch):
    # Initiate the parameter
    Scores = []
    Competitiveness = []
    Resistance = []
    Neighbors = []
    # 1000 times loop
    print("Running iteration...")
    for y in range(0, epoch):

        Agents, deserter = Norm_Game(Agents)
        # next_Agents = Metanorm(Agents, deserter)
        next_Agents = Agents
        Scores.append([u.Score for u in next_Agents])
        # print "i: " + str(y) + " Scores: ", Scores
        Competitiveness.append([u.Competitiveness for u in next_Agents] )
        Resistance.append( [u.Resistance for u in next_Agents] )
        Neighbors.append([u.Neighbors for u in next_Agents])
        # Find the mean of the scores and their standard deviation
        M = np.mean(Scores[0])
        std_deviation = np.std(Scores[0])

        # Norm happens here!
        new_agents = []  # create new agents list
        abondoned_agent = []
        for i in range(len(Agents)):
            # StandardScaler: All data are clustered around 0, and the variance is 1
            scaler = (next_Agents[i].Score - M) / std_deviation
            if scaler >= 1:
                for n in range(int(1/(len(next_Agents[i].Neighbors)/NumAgent))):
                # for n in range(5):
                    new_agents.append( Agent( next_Agents[i].Score, next_Agents[i].Competitiveness, next_Agents[i].Resistance, next_Agents[i].Neighbors ) )
            elif scaler > 0 and scaler < 1:
                new_agents.append( Agent( next_Agents[i].Score, next_Agents[i].Competitiveness, next_Agents[i].Resistance, next_Agents[i].Neighbors ) )
            else:
                abondoned_agent.append( Agent( next_Agents[i].Score, next_Agents[i].Competitiveness, next_Agents[i].Resistance, next_Agents[i].Neighbors ) )
        # refresh the Agents list
        if len(new_agents) <= NumAgent:
            Agents = new_agents
            Num_rest_Agents = NumAgent - len(Agents)
            # randomly create the rest of the Agents
            for i in range( Num_rest_Agents ):
                nn = Find_Neighbors( 1 )
                Agents.extend( Generate_agent( nn ) )
        else:
            # if the Agents' size is out of the len(Agents), cut off the last the Agents' list
            Agents = new_agents[:NumAgent]

        Mutation(Agents)

    return Scores, Competitiveness, Resistance, Neighbors, Agents
    # return Scores[-1], Competitiveness[-1], Resistance[-1], Neighbors[-1], Agents

def Mutation(Agents):
    # mutation is according to a very small probability
    for i in range(len(Agents)):
        mutation = uniform(0, 1)
        if mutation < 0.01:
            Competitiveness = randint( 0, 7 )
            Prob_Competitiveness = Competitiveness / 7

            Resistance = randint( 0, 7 )
            Prob_Resistance = Resistance / 7

            Agents[i].Competitiveness = Prob_Competitiveness
            Agents[i].Resistance = Prob_Resistance

#################
# Hyperparamter
# NumExp = 200
NumExp = 10
epoch = 1000
NumAgent = 25

X = []
Y = []
Z = []
Competitiveness_end = []
Resistance_end = []
# # 1. Find Neighbors
# Network = Find_Neighbors(NumAgent)
# # 1+. Generate agent
# Agents = Generate_agent(Network)
# external loops
for i in range(NumExp):
    print("This is the " + str(i+1) + " round...")
    # 1. Find Neighbors
    Network = Find_Neighbors( NumAgent )
    # 1+. Generate agent
    Agents = Generate_agent( Network )
    # # 2. Print Agents
    # for j in range(len(Agents)):
    #     Agent_print(j, Agents)
    # 3. Norm Game
    # Agents, deserter = Norm_Game(Agents)
    # 3+. Metanorm
    # Agents = Metanorm(Agents, deserter)
    # 4. Iteration
    Scores, Competitiveness_iter, Resistance_iter, Neighbors, Agents = Iteration( Agents, epoch )
    # Read the Competitiveness and Resistance of the agent after the last iteration
    Competitiveness_end.append( Competitiveness_iter[-1] )
    Resistance_end.append( Resistance_iter[-1] )
    x = [np.mean(u) for u in Scores]
    X.append(x)
    y = [np.mean(u) for u in Competitiveness_iter]
    Y.append(y)
    z = [np.mean(u) for u in Resistance_iter]
    Z.append(z)

# Print Figure
# Norm Game Dynamics
fig, ax = plt.subplots()
plt.xlabel("Competitiveness")
plt.ylabel("Resistance")
plt.title('Norm Game Dynamics')
plt.ylim([0.0, 1.0])
plt.xlim([0.0, 1.0])
plt.plot( [np.mean(u) for u in Competitiveness_end], [np.mean( u ) for u in Resistance_end], 'D', c='blue' )
plt.savefig("Norm_Game_Dynamics.png")
plt.show()

# Find mean
S = []
C = []
R = []
for i in range(0, epoch):
    s = [e[i] for e in X]
    c = [e[i] for e in Y]
    r = [e[i] for e in Z]
    S.append( np.mean( s ) )
    C.append( np.mean( c ) )
    R.append(np.mean(r))

# Average Score
fig, ax = plt.subplots()
ax.plot( S, color='red', label='Score' )
plt.xlabel( "Time" )
plt.ylabel( "Value" )
plt.legend()
plt.xlim( [0.0, epoch] )
plt.title( "Average Score in each epoch" )
plt.savefig( "Average Score" )
plt.show()

# Average Competitiveness and Resistance in each epoch
fig, ax = plt.subplots()
ax.plot(C, color='green', label='Competitiveness')
ax.plot(R, color='purple', label='Resistance')
plt.title('Average C and R in each epoch')
plt.xlabel("Epoch")
plt.ylabel("Value")
plt.legend()
plt.ylim([0.0, 1.0])
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
plt.xlim([0.0, epoch])
plt.savefig("Norm Game")
plt.show()

# # --------only used in (ExpNum,epoch,numAgents=3,1000,25)------
# # Average Competitiveness and Resistance in each epoch
# fig, ax = plt.subplots()
# ax.plot([np.mean(u) for u in Competitiveness_end], color='green', label='Competitiveness')
# ax.plot([np.mean(u) for u in Resistance_end], color='purple', label='Resistance')
# plt.title('Average C and R in last loop')
# plt.xlabel("Epoch")
# plt.ylabel("Value")
# plt.legend()
# plt.ylim([0.0, 1.0])
# plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
# plt.xlim([0.0, 20])
# plt.savefig("Norm Game-for top left")
# plt.show()


print("Figure Generated Successfully!")