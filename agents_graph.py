from random import uniform, randint
import matplotlib.pyplot as plt
import random
import datetime
import numpy as np

random.seed(2)
class Agent():
    def __init__(self, S, B, V):
        self.Score = S
        self.Boldness = B
        self.Vengefulness = V
    # def __init__(self, S, B, V, Age, Industry):
    #     self.Score = S
    #     self.Boldness = B
    #     self.Vengefulness = V
    #     self.Neighbors = Age + Industry

def Generate_agent(NumAgent):
    Agents = []
    # 初始NumAgent人口，每个agent有一个随机的boldness和vengefulness
    for i in range( 0, NumAgent):
        Bold = randint( 0, 7 )
        Prob_Bold = Bold / 7

        Veng = randint( 0, 7 )
        Prob_Veng = Veng / 7

        Agents.append(Agent(0, Prob_Bold, Prob_Veng))
    return Agents

# print agents' feature
def Agent_print(j, Agents):
    print("Score: " + str(Agents[j].Score))
    print("Boldness: " + str(Agents[j].Boldness))
    print("Vengefulness: " + str(Agents[j].Vengefulness))
    # print("Neigbhors: " + str(Agents[j].Neighbors))

# Norm Game
def Norm_Game(Agents):
    # 遍历整个Agent的list
    for u in range(len(Agents)):
        # 随机为score赋值
        s = random.uniform(0, 1)
        # Boldness是天生的
        b = Agents[u].Boldness
        if s < b:
            Agents[u].Score += 3
            for y in range(len(Agents)):
                if y != u:
                    Agents[y].Score += -1
                    if s < Agents[y].Vengefulness:
                        Agents[u].Score += -9
                        Agents[y].Score += -2
    return Agents

def Iteration(Agents, epoch):
    # Initiate the parameter
    next_Agents = []

    Scores = []
    Boldness = []
    Vengefulness = []

    # 迭代100次
    print("运行迭代中...")
    for y in range(0, epoch):

        next_Agents = Norm_Game(Agents)

        Scores.append([u.Score for u in next_Agents])
        # print "i: " + str(y) + " Scores: ", Scores
        Boldness.append([u.Boldness for u in next_Agents])
        Vengefulness.append([u.Vengefulness for u in next_Agents])

        # 找到分数的平均值及其标准偏差
        M = np.mean(Scores[0])
        print("mean:", str(M))
        std_deviation = np.std(Scores[0])
        print("std_deviation:", str(std_deviation))

        # 确定好人和普通人
        new_agents = []  # 新的agent
        abondoned_agent = []
        for i in range(len(Agents)):
            # StandardScaler: 所有数据都聚集在0附近，方差为1
            scaler = (next_Agents[i].Score - M) / std_deviation
            if scaler >= 1:
                # new_agents.append(Agent(0, next_Agents[i].Boldness, next_Agents[i].Vengefulness, next_Agents[i].Neighbors))
                # new_agents.append(Agent(0, next_Agents[i].Boldness, next_Agents[i].Vengefulness, next_Agents[i].Neighbors))
                new_agents.append(
                    Agent( 0, next_Agents[i].Boldness, next_Agents[i].Vengefulness) )
                new_agents.append(
                    Agent( 0, next_Agents[i].Boldness, next_Agents[i].Vengefulness) )
            elif scaler * std_deviation > 0 and scaler < 1:
                new_agents.append(Agent(0, next_Agents[i].Boldness, next_Agents[i].Vengefulness))
            else:
                abondoned_agent.append(Agent(0, next_Agents[i].Boldness, next_Agents[i].Vengefulness))
        # 根据好人和普通人的后代创建一个新的列表
        # 打印“新员工人数：”+str（len（新员工））
        if len(new_agents) <= NumAgent:
            Agents = new_agents
            Num_rest_Agents = NumAgent - len(Agents)
            # 随机生成剩下的Agent
            Generate_agent( Num_rest_Agents )
            # for i in range(Num_rest_Agents):
            #     Bold = randint(0, 7)
            #     Prob_Bold = Bold / 7
            #     Veng = randint(0, 7)
            #     Prob_Veng = Veng / 7
            #     Agents.append(Agent(0, Prob_Bold, Prob_Veng))
        else:
            # 超出NumAgent的部分被截取
            next_Agents = new_agents[:NumAgent]

        Mutation(Agents)
    return Scores, Boldness, Vengefulness, next_Agents

def Mutation(Agents):
    # 突变
    for i in range(len(Agents)):
        mutation = uniform(0, 1)
        if mutation < 0.01:
            Bold = randint( 0, 7 )
            Prob_Bold = Bold / 7

            Veng = randint( 0, 7 )
            Prob_Veng = Veng / 7

            Agents[i].Boldness = Prob_Bold
            Agents[i].Vengefulness = Prob_Veng

# 模型参数
NumExp = 10
epoch = 100
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
    print("这是第" + str(i) + "轮")
    # 1. Generate agent
    Agents = Generate_agent(NumAgent)
    # 2. Print Agents
    for j in range(len(Agents)):
        Agent_print(j, Agents)
    # 3. Norm Game
    Agents = Norm_Game(Agents)
    # 4. Iteration
    Scores, Boldness_1, Vengefulness_1, Agents = Iteration(Agents, epoch)
    # 读取最后一次迭代后的Agent的Boldness和Vengefulness
    Boldness_end.append(Boldness_1[len(Boldness_1)-1])
    Vengefulness_end.append(Vengefulness_1[len(Vengefulness_1)-1])
    # for i in range(len(x)):
    #     print "i: " + str(i) + " x: " + str(x[i])
    x = [np.mean(u) for u in Scores]
    y = [np.mean(u) for u in Boldness_1]
    z = [np.mean(u) for u in Vengefulness_1]
    # u = [np.mean(u) for u in Agents]
    X.append(x)
    Y.append(y)
    Z.append(z)
    # U.append(u)

    x = []
    for i in range( epoch ):
        gen = [e[i] for e in X]
        x.append( np.mean( gen ) )
    fig, ax = plt.subplots()
    ax.plot( x, color='red', label='mean' )
    plt.title("Average Score in each epoch")
    plt.xlabel( "Time" )
    plt.ylabel( "Value" )
    plt.legend()
    plt.yticks( [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] )
    plt.xlim( [0.0, epoch] )
    plt.savefig( "Norm Game" )
    plt.show()

# Axelrod 基本图
plt.xlabel("Boldness")
plt.ylabel("Vengefulness")
plt.title('Norm Game Dynamics')
plt.ylim([0.0, 1.0])
plt.xlim([0.0, 1.0])
plt.plot([np.mean(u) for u in Vengefulness_end], [np.mean(u) for u in Boldness_end], 'D', color='red')
plt.savefig("Norm_Game_Dynamics.png")
plt.show()

# 找到平均值
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

# 画图
fig, ax = plt.subplots()

ax.plot(z, color='grey', label='Boldness')
ax.plot(y, color='black', label='Vengefulness')

plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.ylim([0.0, 1.0])
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
plt.xlim([0.0, epoch])
plt.savefig("Norm Game")
plt.show()

fig, ax = plt.subplots()
ax.plot(x, color='red', label='mean')

plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
plt.xlim([0.0, epoch])
plt.savefig("Norm Game")
plt.show()

print("画图中。。。")
