import sys
import random

#machine class
class Machine:
    def __init__(self, speed, power, ID):
        self.speed = speed
        self.power = power
        self.tasksAssigned = []
        self.completionTime = 0.0
        self.taskSum = 0
        self.machID = ID
    def __repr__(self):
        return self.__str__()
    def __lt__(self, other):
        return self.completionTime < other.completionTime


#task class
class Task:
    def __init__(self, runtime, workload, ID):
        self.isAssigned = False
        self.runtime = runtime
        self.workload = workload
        self.taskID = ID
    def __lt__(self, other):
        return self.runtime < other.runtime
    def __str__(self):
        return str(self.taskID)+str(": ")+str(self.runtime)
    def __repr__(self):
        return self.__str__()


#removes task from one machine and adds it to the machine with speed
def maxGive(machineList, cIndex, maxIndex, space, doInsert):
    counter = 0
    addIndex = 0
    newMaxT = 0
    newCT = 0
    limit = machineList[maxIndex].completionTime
    for task in machineList[maxIndex].tasksAssigned:
        
        if (task.runtime <= space):
            newMaxT = (machineList[maxIndex].taskSum - task.runtime) / machineList[maxIndex].speed
            newCT = (machineList[cIndex].taskSum + task.runtime) / machineList[cIndex].speed
            if (max(newMaxT, newCT) < limit and min(newMaxT, newCT)):
                limit = max(newCT, newMaxT)
                addIndex = counter

                # removing task
                if doInsert == True:
                    addTask = machineList[maxIndex].tasksAssigned.pop(addIndex)
                    machineList[cIndex].tasksAssigned.append(addTask)

                    machineList[maxIndex].taskSum = newMaxT * machineList[maxIndex].speed                    
                    machineList[maxIndex].completionTime = newMaxT
                    machineList[cIndex].taskSum = newCT * machineList[cIndex].speed
                    machineList[cIndex].completionTime = newCT
                    return
        counter += 1
    return limit
        

#adjusts final lists based on comparison to maxMachine
def adjustLists(machineList, numMachines):
    maxIndex = machineList.index(max(machineList))

    timeList = []
    for i in range(int(numMachines)):
        if (i == maxIndex):
            timeList.append(machineList[maxIndex].completionTime)
        else:
            space = machineList[maxIndex].completionTime * machineList[i].speed - machineList[i].taskSum
            timeList.append(maxGive(machineList, i, maxIndex, space, False))

    i = timeList.index(min(timeList))
    maxGive(machineList, i, maxIndex, space, True)
        

#function to assign tasks if they overflow the computing power
#assigns task to machine that would overflow the least
def assignByOverflow(task, machineList, isGreedy, bestLimit):
    minOverflow = sys.maxsize
    machineIndex = 0
    bestMachineIndex = 0
    for machine in machineList:
        #calculate overflow
        overflow = abs(machine.power - task.workload)
        #if new min overflow found, update min and machine index
        if (overflow < minOverflow):
            minOverflow = overflow
            bestMachineIndex = machineIndex
        machineIndex += 1
    #assign task to machine with smallest overflow
    task.isAssigned = True
    machineList[bestMachineIndex].tasksAssigned.append(task)
    machineList[bestMachineIndex].power -= task.workload


#Algorithm
def fillMachines(numTasks, numMachines, taskTimes, machineSpds, isGreedy, bestLimit):    
    
    #find total runtimes and speeds
    totalTime = sum(taskTimes)
    totalSpd = sum(machineSpds)

    idealTime = totalTime/totalSpd

    counter = 0
    machineList = []
    #create machine objects
    for machineSpd in machineSpds:
        computingPower = machineSpd/totalSpd  #represents how fast the machine is proportionally
        counter += 1
        newMachine = Machine(machineSpd, computingPower, counter)
        machineList.append(newMachine)

    counter = 0
    taskList = []
    #create task objects
    for taskTime in taskTimes:
        taskLoad = taskTime/totalTime  #represents how long the task is proportionally
        counter += 1
        newTask = Task(taskTime, taskLoad, counter)
        taskList.append(newTask)
        
    #sorting tasks from highest to lowest for Greedy
    #if isGreedy == True:
    taskList.sort(reverse=True)
    #sorting tasks randomly for Stochastic
    #else: random.shuffle(taskList)
        
    #"fill" computing power of each machine with task loads until proportions are roughly equal
    #(assumes task proportions will be smaller than machine proportions)
    for task in taskList:

        #sort machine by speed for Greedy
        if isGreedy == True:
            machineList = sorted(machineList, key = lambda x: x.speed)
        #sorting machines randomly for Stochastic
        else: random.shuffle(machineList)

        #for each task loop through all machines
        for machine in machineList:
            #assigns task to machine if enough space
            if (task.workload <= machine.power and task.isAssigned == False):
                task.isAssigned = True
                machine.tasksAssigned.append(task)
                machine.power -= task.workload
        
        #if task can't fit on any machines, assign by overflow
        if (task.isAssigned == False):
            assignByOverflow(task, machineList, isGreedy, bestLimit)

    #calculate completion times of all machines    
    for machine in machineList:
        machine.tasksAssigned.sort()
        for task in machine.tasksAssigned:
            machine.taskSum += task.runtime
        machine.completionTime = machine.taskSum / machine.speed


    adjustLists(machineList, numMachines)
    if (isGreedy == False and bestLimit<=max(machineList).completionTime and bestLimit > 0):
            
            return []

    """   
    #print data analysis
    for machine in machineList:
        print ('\nMachine speed:', machine.speed, ', completion time:', machine.completionTime, ', sum of tasks:', machine.taskSum)
        print('Tasks assigned:', machine.tasksAssigned)
    print('Ideal Completion Time:', idealTime)
    """
    print('Max Completion Time:', max(machineList).completionTime)
    print('====================')

    return machineList


#writing output file
def writeFile(machineList):
    f = open("OUTPUT.txt", "w")

    numPrint = round(max(machineList).completionTime,2)
    f.write("{0:.2f}".format(numPrint))

    #sort machines by ID / order they were read from file
    machineList = sorted(machineList, key = lambda x: x.machID)
    
    for machine in machineList:
        first = True
        f.write("\n")
        for task in machine.tasksAssigned:
            num = str(task.taskID)
            if first == True:
                f.write(num)
                first = False
            else:
                f.write(" ")
                f.write(num)
    f.close()


#main---------------------------------------------------------

#read file and make arrays
f = open(r'C:\Users\lexir\Documents\Algorithms\inputs\input_group.txt')

numTasks = f.readline()       #number of tasks
numMachines = f.readline()     #number of machines
taskStr = f.readline()
taskStr = taskStr.split()
temp = map(int, taskStr)

taskTimes = list(temp)  #array of task times

machineStr = f.readline()
machineStr = machineStr.split()
temp2 = map(int, machineStr)

machineSpeeds = list(temp2)  #array of machine speeds
f.close()

#calling greedy algorithm
machList = fillMachines(numTasks, numMachines, taskTimes, machineSpeeds, True, -1.0)


epicArray = []
epicArray.append(machList)
bestTime = max(machList).completionTime
bestIndex = 0

#write file
writeFile(epicArray[bestIndex])

for i in range(1,4000):
    ex = fillMachines(numTasks, numMachines, taskTimes, machineSpeeds, False, bestTime)
    if bool(ex) == True:
        epicArray.append(ex)
        if max(epicArray[-1]).completionTime < bestTime:
            bestTime = max(epicArray[-1]).completionTime
            bestIndex += 1

            #write file
            writeFile(epicArray[bestIndex])

        
print('\n========== DONE ==========')

#write file
writeFile(epicArray[bestIndex])


