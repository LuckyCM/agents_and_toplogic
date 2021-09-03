norm+topologic+no_metanor.pyIt is the core code in this experiment, which is roughly divided into the following five steps:
1) First, using find_ Neighbors() to randomly generate an agent's age and industry.
2) Then, set the agent of the same age group (10 years) and the same industry as neighbors,
 and then using generate_ Agent() generates agents
3) Norm_ Game (the specific process is similar to the process described in Axelrod's paper)
4) Iterate to show how norm is generated (select the agent with high score to propagate.
 The specific process is similar to BGA: binary genetic algorithm)
5) Visual display of experimental results

There are also several codes for comparing experimental results:
a) norm_emergence+topologic+metanorm.py:It is used to compare the analysis of experimental results and experimental running time by adding metanorm punishment mechanism.
(due to the limitation of computer performance and time, the effect of adding metanorm is not good, so we decided to remove metanorm after weighing)
b) norm_emergence+fully-linked_topologic.py:The experimental results used to compare the fully connected topology with the involuted topology are different.
c) Figure Directory: contains the experimental results of full connection
Some Abbreviation introduction:(c == Score of the agent as supervisees)
                               (r == Score of the agent as supervisors)
                               (no involution == involution do not happened)
d) Figure+Topologic-metanorm:
Some Abbreviation introduction:(Exp == NumExp(number of external loops));
                               (epoch == epoch(number of internal loops));
                               (numA == NumAgent)
                               (u == Score of the agent as supervisees)
                               (v == Score of the agent as supervisors)