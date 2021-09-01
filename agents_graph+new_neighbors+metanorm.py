from random import uniform, randint
import matplotlib.pyplot as plt
import random
import datetime
import numpy as np

random.seed(2)
# random.seed(1031)

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
    # 初始NumAgent人口
    for i in range(0, NumAgent):

        # 假设研究20-70岁的工作者
        Age = randint(20, 70)
        Age_Group = int((Age - 20) / 10)

        # 假设有5个职业(计算机，医生，律师，教师，农民)
        Industry = randint(0, 4)

        Network.append(Toplogic(Age_Group, Industry))
    return Network

def Generate_agent(Network):
    Agents = []
    Neighbors = []
    # 每个agent有一个随机的boldness和vengefulness
    for i in range(len(Network)):
        Competitive = randint( 0, 7 )
        Prob_Competitive = Competitive / 7

        Resistence = randint( 0, 7 )
        Prob_Resistence = Resistence / 7

        for j in range(len(Network)):
            if Network[j].Age == Network[i].Age or Network[j].Industry == Network[i].Industry:
                Neighbors.append( Network[j] )
        Agents.append(Agent(0, Prob_Competitive, Prob_Resistence, Neighbors))
        Neighbors = [] # 这里不能用list.clear()
    return Agents

# print agents' feature
def Agent_print(j, Agents):
    print("Score: " + str(Agents[j].Score))
    print("Boldness: " + str( Agents[j].Competitiveness ) )
    print("Vengefulness: " + str( Agents[j].Resistance ) )
    print("Neighbors: " + str(Agents[j].Neighbors))

# Norm Game
def Norm_Game(Agents):
    # 遍历整个Agent的list
    N = NumAgent
    deserter = []
    for u in range(len(Agents)):
        # 随机为score赋值
        prob = random.uniform(0, 1)
        # Boldness是天生的
        compete = Agents[u].Competitiveness
        if prob < compete:
            Agents[u].Score += 5 / N
            for y in range(len(Agents)):
                # 寻找neighbors中的相同值
                for i in range( len( Agents[y].Neighbors ) ):
                    for j in range( len( Agents[u].Neighbors ) ):
                        # only can be seen by their neighbors
                        if y != u:
                            if Agents[y].Neighbors[i].Age == Agents[u].Neighbors[j].Age or \
                                Agents[y].Neighbors[i].Industry == Agents[u].Neighbors[j].Industry:
                                Agents[y].Score += -1 / N
                                if prob < Agents[y].Resistance:
                                    Agents[u].Score += -4.8 / N
                                    # Agents[u].Score += -0.05 / N
                                    # Agents[u].Score += -0.45 / N
                                    Agents[y].Score += -1 / N
                                else:
                                    deserter.append(y)
    return Agents, deserter

def Metanorm(Agents, deserter):
    N = NumAgent
    for u in deserter:
        # 随机为score赋值
        prob = random.uniform(0, 1)
        # Boldness是天生的
        compete = Agents[u].Competitiveness
        if prob < 0.5:
            for y in range(len(Agents)):
                # only can be seen by their neighbors
                c = tuple(set( Agents[y].Neighbors ) & set( Agents[u].Neighbors ))
                if y != u and prob < Agents[y].Resistance:
                    if [c[i].Age for i in range( len( c ) )] == [Agents[y].Neighbors[j].Age for j in range( len( Agents[y].Neighbors ) )] \
                        or [c[i].Industry for i in range( len( c ) )] == [Agents[y].Neighbors[j].Industry for j in range( len( Agents[y].Neighbors ) )]:
                        # Agents[u].Score += -4.8 / N
                        Agents[u].Score += -5 / N
                        # [c[i].Score for i in range(len(c))] += -5 / N
                        Agents[y].Score += -1 / N
    return Agents

def Iteration(Agents, epoch):
    # Initiate the parameter
    next_Agents = []

    Scores = []
    Boldness = []
    Vengefulness = []
    Neighbors = []
    # 迭代100次
    print("运行迭代中...")
    for y in range(0, epoch):

        Agents, deserter = Norm_Game(Agents)
        next_Agents = Metanorm(Agents, deserter)

        Scores.append([u.Score for u in next_Agents])
        # print "i: " + str(y) + " Scores: ", Scores
        Boldness.append( [u.Competitiveness for u in next_Agents] )
        Vengefulness.append( [u.Resistance for u in next_Agents] )
        Neighbors.append([u.Neighbors for u in next_Agents])
        # 找到分数的平均值及其标准偏差
        M = np.mean(Scores[0])
        # print("mean:", str(M))
        std_deviation = np.std(Scores[0])
        # print("std_deviation:", str(std_deviation))

        # Norm happens here!
        new_agents = []  # create new agents list
        abondoned_agent = []
        for i in range(len(Agents)):
            # StandardScaler: 所有数据都聚集在0附近，方差为1
            scaler = (next_Agents[i].Score - M) / std_deviation
            if scaler >= 1:
                new_agents.append( Agent( 0, next_Agents[i].Competitiveness, next_Agents[i].Resistance, next_Agents[i].Neighbors ) )
                new_agents.append( Agent( 0, next_Agents[i].Competitiveness, next_Agents[i].Resistance, next_Agents[i].Neighbors ) )
            elif scaler > 0 and scaler < 1:
                new_agents.append( Agent( 0, next_Agents[i].Competitiveness, next_Agents[i].Resistance, next_Agents[i].Neighbors ) )
            else:
                abondoned_agent.append( Agent( 0, next_Agents[i].Competitiveness, next_Agents[i].Resistance, next_Agents[i].Neighbors ) )
        # refresh the Agents list
        if len(new_agents) <= NumAgent:
            Agents = new_agents
            Num_rest_Agents = NumAgent - len(Agents)
            # randomly create the rest of the Agents
            nn = Find_Neighbors(Num_rest_Agents)
            Generate_agent(nn)
        else:
            # if the Agents' size is out of the len(Agents), cut off the last the Agents' list
            next_Agents = new_agents[:NumAgent]

        Mutation(Agents)
    return Scores, Boldness, Vengefulness, Neighbors, next_Agents

def Mutation(Agents):
    # 突变
    for i in range(len(Agents)):
        mutation = uniform(0, 1)
        if mutation < 0.01:
            Competitiveness = randint( 0, 7 )
            Prob_Competitiveness = Competitiveness / 7

            Resistance = randint( 0, 7 )
            Prob_Resistance = Resistance / 7

            Agents[i].Competitiveness = Prob_Competitiveness
            Agents[i].Resistance = Prob_Resistance

# 模型参数
# NumExp = 200
NumExp = 10
epoch = 1000
NumAgent = 25

#################
X = []
Y = []
Z = []
U = []
Boldness_end = []
Vengefulness_end = []

# 这是一个循环
for i in range(NumExp):
    print("This is the " + str(i) + "round...")
    # 1. Find Neighbors
    Network = Find_Neighbors(NumAgent)
    # 1+. Generate agent
    Agents = Generate_agent(Network)
    # # 2. Print Agents
    # for j in range(len(Agents)):
    #     Agent_print(j, Agents)
    # 3. Norm Game
    Agents, deserter = Norm_Game(Agents)
    # 3+. Metanorm
    Agents = Metanorm(Agents, deserter)
    # 4. Iteration
    Scores, Competitiveness_iter, Resistance_iter, Neighbors, Agents = Iteration( Agents, epoch )
    # 读取最后一次迭代后的Agent的Boldness和Vengefulness
    Boldness_end.append( Competitiveness_iter[len( Competitiveness_iter ) - 1] )
    Vengefulness_end.append( Resistance_iter[len( Resistance_iter ) - 1] )
    x = [np.mean(u) for u in Scores]
    y = [np.mean(u) for u in Competitiveness_iter]
    z = [np.mean(u) for u in Resistance_iter]
    # u = [np.mean(u) for u in Agents]
    X.append(x)
    Y.append(y)
    Z.append(z)
    # U.append(u)


# Norm Game Dynamics
fig, ax = plt.subplots()
plt.xlabel("Competitiveness")
plt.ylabel("Resistance")
plt.title('Norm Game Dynamics')
plt.ylim([0.0, 1.0])
plt.xlim([0.0, 1.0])
plt.plot([np.mean(u) for u in Vengefulness_end], [np.mean(u) for u in Boldness_end], 'D', c='blue')
plt.savefig("Norm_Game_Dynamics.png")
plt.show()

# Find mean
x = []
for i in range(epoch):
    gen = [e[i] for e in X]
    x.append(np.mean(gen))

y = []
for i in range(epoch):
    gen = [e[i] for e in Y]
    y.append( np.mean( gen ) )

z = []
for i in range(epoch):
    gen = [e[i] for e in Z]
    z.append(np.mean(gen))

u = []
for i in range(epoch):
    gen = [e[i] for e in U]
    u.append(np.mean(gen))

##
# Average Score
fig, ax = plt.subplots()
ax.plot( x, color='red', label='mean' )
plt.title( "Average Score in each epoch" )
plt.xlabel( "Time" )
plt.ylabel( "Value" )
plt.legend()
# plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
# plt.xlim( [0.0, epoch] )
plt.savefig( "Average Score" )
plt.show()

# Average Competitiveness and Resistance in each epoch
fig, ax = plt.subplots()
ax.plot(z, color='green', label='Competitiveness')
ax.plot(y, color='purple', label='Resistance')
plt.title('Average C and R in each epoch')
plt.xlabel("Epoch")
plt.ylabel("Value")
plt.legend()
plt.ylim([0.0, 1.0])
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
# plt.xlim([0.0, NumExp])
plt.savefig("Norm Game")
plt.show()

print("Figure Generating...")
