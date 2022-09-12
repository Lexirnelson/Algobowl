# Algobowl
This my group's coding solution to a class-wide coding competition "Algobowl". 

The problem was as follows:

You are given
1. a set of n tasks along with their integer runtimes t1, t2, . . . , tn, and
2. a set of m machines along with their integer speeds s1, s2, . . . , sn.

Your task is to assign each of the n tasks to one of the m machines so that the overall completion time (the
time at which all of the tasks are completed) is minimized. The completion time of a machine is the sum of
the runtimes of the tasks assigned to it divided by its speed. The overall completion time is the maximum of
the completion times of all of the machines.

Our strategy to solve this was to take the total task time. We would then assign “space” to the machines based 
on the proportion of total run time that each machine had. Once we found the proportions of the tasks and 
machines, we sorted the tasks from largest to smallest proportion and randomly assigned them to machines based 
on the amount of “space” we calculated from the machine’s proportional speed. If a task made a machine overflow, 
we simply assigned it to the machine that overflowed the least. The idea behind this was to assign the largest 
tasks first randomly and see if we could get good run times greedily. We would run this 1000 times to see what 
the best randomly assigned times were.
