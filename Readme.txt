norm_emergence+topology+metanorm & norm_emergence+topology-metanorm:
The model uses Python language as the medium, combined with multi-agent system, norm game, metanorm,
evolutionary method and topological logic model to simulate the emergence of involution social norms.
These two files are the core codes of this experiment, which are roughly divided into the following five steps:
1) First, using find_ Neighbors() to randomly generate an agent's age and industry.
2) Then, set the agent of the same age group (10 years) and the same industry as neighbors,
 and then using generate_ Agent() generates agents
3) Norm_ Game (the specific process is similar to the process described in Axelrod's paper)
# 3+) Metanorm part will be include in "...+metanorm.py", and "...-metanorm.py" means metanorm part has been removed
4) Iterate to show how norm is generated (select the agent with high score to propagate. The specific process is
similar to BGA: binary genetic algorithm)
5) Visual display of experimental results

There are also several codes for comparing experimental results:
a)"... [+/-] metanorm.py": It is used to compare the analysis of experimental results and experimental
running time by adding metanorm punishment mechanism.
b) "norm_emergence+ [fully_linked/topology] ....py": The experimental results used to compare the difference of
experimental results between fully connected and involuted topology.
c) Figure Directory: contains the experimental results of full connection
Some Abbreviation introduction: (Both u and V are used twice)
                                (Exp == NumExp(number of external loops));
                                (epoch == epoch(number of internal loops));
                                (numA == NumAgent)
                                (u == Score of the agent as supervisees)
                                (v == Score of the agent as supervisors)