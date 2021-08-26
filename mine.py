#coding=utf-8
from random import uniform, randint
import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
import scipy as sp

# 用当前时间作为种子
random.seed(datetime.datetime.now())

# Agents
class Jugadores():
    def __init__(self, S, B, V):
        self.Score = S
        self.Boldness = B
        self.Vengefulness = V

# print agents
def Imprimir_Jugador(j, Personas):
    print("Score: " + str( Personas[j].Score ))
    print("Boldness: " + str( Personas[j].Competitiveness ) )
    print("Vengefulness: " + str( Personas[j].Resistance ) )

def Iteraction(Poblacion):
    Corrompe_norma = []
    for u in range(len(Poblacion)):
        # 我们给每个居民4次不符合标准的机会
        for k in range(0, 4):
            s = random.uniform(0, 1)
            b = Poblacion[u].Competitiveness
            if s < b:
                Poblacion[u].Score += 3
                Corrompe_norma.append(0)
                for y in range(len(Poblacion)):
                    if y != u:
                        Poblacion[y].Score += -1
                        if s < Poblacion[y].Resistance:
                            Poblacion[u].Score += -9
                            Poblacion[y].Score += -2
            else:
                Corrompe_norma.append(1)
    return Poblacion, Corrompe_norma

def Experimento():
    # Initiate the parameter
    Personas = []
    Scores = []
    Boldness_1 = []
    Vengefulness_1 = []
    Corrompe_norma_1 = []

    # 初始20人口，每个agent有一个随机的boldness和vengefulness
    for i in range(0, 20):
        Bold = randint(0, 7)
        Prob_Bold = Bold / 7

        Veng = randint(0, 7)
        Prob_Veng = Veng / 7

        Personas.append(Jugadores(0, Prob_Bold, Prob_Veng))

    # 迭代100次
    print("运行迭代中...")
    for y in range(0, NumGeneraciones):

        Personas, aux = Iteraction(Personas)

        Scores.append([u.Score for u in Personas])
        # print "i: " + str(y) + " Scores: ", Scores
        Boldness_1.append( [u.Competitiveness for u in Personas] )
        Vengefulness_1.append( [u.Resistance for u in Personas] )
        Corrompe_norma_1.append( aux ) # Norm

        # 找到分数的平均值及其标准偏差
        M = np.mean(Scores)
        print("mean:", str(M))
        std_deviation = np.std(Scores)
        print("std_deviation:", str(std_deviation))
        # M = np.mean(Boldness_1)
        # print "El promedio de boldness es: " + str(M)
        #
        # M = np.mean(Vengefulness_1)
        # print "El promedio de vengefulness es: " + str(M)

        # 确定好人和普通人
        Personas_nuevas = [] # 新的agent

        for i in range(len(Personas)):
            x = (Personas[i].Score - M) / std_deviation
            if Personas[i].Score >= M + 1 * std_deviation:
                Personas_nuevas.append( Jugadores( 0, Personas[i].Competitiveness, Personas[i].Resistance ) )
                Personas_nuevas.append( Jugadores( 0, Personas[i].Competitiveness, Personas[i].Resistance ) )
            elif Personas[i].Score >= M and Personas[i].Score < M + 1 * std_deviation:
                Personas_nuevas.append( Jugadores( 0, Personas[i].Competitiveness, Personas[i].Resistance ) )

        # print "Lista de buenos (tamano " + str(len(indices_buenos)) + ")"
        # print indices_buenos
        # print "Lista de regulares (tamano " + str(len(indices_regulares)) + ")"
        # print indices_regulares

        # 根据好人和普通人的后代创建一个新的列表
        # 打印“新员工人数：”+str（len（新员工））
        if len(Personas_nuevas) <= 20:
            Personas = Personas_nuevas
            x = 20 - len(Personas)
            for i in range(x):
                Bold = randint(0, 7)
                Prob_Bold = Bold / 7

                Veng = randint(0, 7)
                Prob_Veng = Veng / 7

                Personas.append(Jugadores(0, Prob_Bold, Prob_Veng))
        else:
            Personas = Personas_nuevas[:20]

        # 突变
        for i in range(len(Personas)):
            mutation = uniform(0, 101)
            if mutation < 1:
                Bold = randint( 0, 7 )
                Prob_Bold = Bold / 7

                Veng = randint( 0, 7 )
                Prob_Veng = Veng / 7

                Personas[i].Boldness = Prob_Bold
                Personas[i].Vengefulness = Prob_Veng

    return Scores, Boldness_1, Vengefulness_1, Corrompe_norma_1


# 模型参数
NumExp = 10
NumGeneraciones = 100

#################
X = []
Y = []
Z = []
U = []
Boldness_Av = []
Vengefulness_Av = []

# 这是一个循环
for i in range(NumExp):
    print("这是第" + str(i) + "轮")
    Scores, Boldness_1, Vengefulness_1, Corrompe_norma_1 = Experimento()
    Boldness_Av.append(Boldness_1[len(Boldness_1)-1])
    Vengefulness_Av.append(Vengefulness_1[len(Vengefulness_1)-1])
    # for i in range(len(x)):
    #     print "i: " + str(i) + " x: " + str(x[i])
    x = [np.mean(u) for u in Scores]
    y = [np.mean(u) for u in Boldness_1]
    z = [np.mean(u) for u in Vengefulness_1]
    u = [np.mean(u) for u in Corrompe_norma_1]
    X.append(x)
    Y.append(y)
    Z.append(z)
    U.append(u)

# Axelrod 基本图
plt.xlabel("Boldness")
plt.ylabel("Vengefulness")
plt.title('Norm Game Dynamics')
plt.ylim([0.0, 1.0])
plt.xlim([0.0, 1.0])
plt.plot([np.mean(u) for u in Vengefulness_Av], [np.mean(u) for u in Boldness_Av], 'D', color='red')
plt.savefig("Norm_Game_Dynamics.png")
plt.show()

# 找到平均值
x = []
for i in range(NumGeneraciones):
    gen = [e[i] for e in X]
    x.append(np.mean(gen))

y = []
for i in range(NumGeneraciones):
    gen = [e[i] for e in Y]
    y.append( np.mean( gen ) )

z = []
for i in range(NumGeneraciones):
    gen = [e[i] for e in Z]
    z.append(np.mean(gen))

u = []
for i in range(NumGeneraciones):
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
plt.xlim([0.0, NumGeneraciones])
plt.savefig("Norm Game")
plt.show()

# print Corrompe_norma_1
# print "Listo!"

print("画图中。。。")
f, axarr = plt.subplots(4)

axarr[0].set_ylabel('Score')
axarr[1].set_ylabel('Boldness')
axarr[1].set_ylim(-0.1, 1.1)
axarr[2].set_ylabel('Vengefulness')
axarr[2].set_ylim(-0.1, 1.1)
axarr[3].set_ylabel('Norma')
axarr[3].set_ylim(-0.1, 1.1)
axarr[3].set_xlabel('Generation')

axarr[0].plot(x)
axarr[1].plot(y)
axarr[2].plot(z)
axarr[3].plot(u)
# axarr[1].plot( y, 'y--', linewidth = 1)
# axarr[2].plot( z, 'r-.', linewidth = 1)
# axarr[0].set_title('Boldness =' + str(Boldness_inicial) + ' Vengefulness =' + str(Vengefulness_inicial))

plt.savefig("Multiple.png")
plt.show()

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# #ax1.set_title("Temperatura del panal vs. tiempo")
# # ax1.set_xlabel('t (time)')
# # ax1.set_ylabel('T (temperature)')
# # ax1.set_ylim([29, 33])
# ax1.plot([np.mean(u) for u in Scores], marker="v", ls='-') # , 'x', c = 'black', linewidth=4)
# ax1.plot([np.mean(u) for u in Boldness_1], marker="o",ls='-') # , 'x', c = 'black', linewidth=4)
# plt.show()
# #ax1.plot(Tp, c='black')