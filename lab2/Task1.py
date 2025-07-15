import math, random

gridsize=25

components={'ALU':(5,7),
            'Cache':(7,4),
            'Control Unit':(4,4),
            'Register File':(6,6),
            'Decoder':(5,3),
            'Floating Unit':(5,5)
            }

order=['ALU','Cache','Control Unit','Register File','Decoder','Floating Unit']

interconnections=[(3,0),(2,0),(0,1),(3,5),(1,4),(4,5)]

populationMax=100
generationTime=50
mutationRate=0.10
elitismCount=2

overlapCost=100
wireCost=2
boundingCost=1

class Chromosome:
    
    def __init__(self, cordinates=None):
        if cordinates:
            self.cordinates=cordinates
        else:
            self.cordinates=[]
            for x in range(len(order)):
                x= random.randint(0,gridsize-1)
                y= random.randint(0,gridsize-1)
                self.cordinates.extend([x,y])
        self.fitness= 0.0
    
    def __str__(self):
        output="cords: "
        for i in range(len(order)):
            name=order[i]
            x= self.cordinates[i*2]
            y= self.cordinates[i*2 +1]
            output+=f"{name}:({x},{y})"
        return output

def fitness(Chromosome):
    overlaps=0
    wire=0
    bounding=0
    
    for i in range(len(order)):
        for j in range(i+1, len(order)):
            name_a=order[i]
            ax=Chromosome.cordinates[i*2]
            ay=Chromosome.cordinates[i*2 +1]
            a_width=components[name_a][0]
            a_height=components[name_a][1]
            a_left, a_right= ax, ax+a_width
            a_bottom, a_top = ay, ay+a_height
            
            name_b=order[j]
            bx=Chromosome.cordinates[j*2]
            by=Chromosome.cordinates[j*2 +1]
            b_width=components[name_b][0]
            b_height=components[name_b][1]
            b_left, b_right= bx, bx+b_width
            b_bottom, b_top = by, by+b_height
            
            overlap = not (a_right<=b_left or a_left>=b_right or a_bottom>=b_top or a_top<=b_bottom)
            
            if overlap:
                overlaps+=1
    overlapPenalty= overlapCost * overlaps
    
    for start,end in interconnections:
        start_name=order[start]
        start_x=Chromosome.cordinates[start*2]
        start_y=Chromosome.cordinates[start*2 +1]
        start_cx=start_x+components[start_name][0]/2
        start_cy=start_y+components[start_name][1]/2
        
        end_name=order[end]
        end_x=Chromosome.cordinates[end*2]
        end_y=Chromosome.cordinates[end*2 +1]
        end_cx=end_x + components[end_name][0]/2
        end_cy=end_y + components[end_name][1]/2
        
        distance= math.sqrt((start_cx-end_cx)**2 +(start_cy-end_cy)**2)
        wire+=distance
    wirePenalty=wireCost*wire
    
    min_x,min_y=math.inf, math.inf
    max_x,max_y=-math.inf, -math.inf
    for i in range(len(order)):
        name=order[i]
        x=Chromosome.cordinates[i*2]
        y=Chromosome.cordinates[i*2 +1]
        width=components[name][0]
        height=components[name][1]
        min_x=min(min_x,x)
        min_y=min(min_y,y)
        max_x=max(max_x,x+width)
        max_y=max(max_y, y+height)
        
    bound_area= (max_x-min_x) *(max_y-min_y)
    areaPenalty= boundingCost*bound_area
    
    MaxPenalty= overlapPenalty+wirePenalty+areaPenalty
    Chromosome.fitness= -MaxPenalty
    
    return overlapPenalty, wirePenalty, areaPenalty

def parents(populationMax):
    parentA_tourny=random.sample(populationMax,2)
    parentA = max(parentA_tourny, key=lambda ind: ind.fitness)
    
    parentB_tourny=random.sample(populationMax,2)
    parentB = max(parentB_tourny,key=lambda ind:ind.fitness)
    
    return parentA, parentB

def crossover(parentA,parentB):
    #single-point-crossover
    cords1=parentA.cordinates
    cords2=parentB.cordinates
    
    split=random.randrange(2, len(cords1)-1, 2)
    
    child1_cords=cords1[:split]+cords2[split:]
    child2_cords=cords2[:split]+cords1[split:]
    
    return Chromosome(child1_cords), Chromosome(child2_cords)

def crossover2(parentA,parentB):
    #double-point-crossover
    cords1=parentA.cordinates
    cords2=parentB.cordinates
    
    split1=random.randrange(2, len(cords1)-2, 2)
    split2=random.randrange(split1+2, len(cords1), 2)
    
    child1_cords=cords1[:split1]+cords2[split1:split2]+cords1[split1:]
    child2_cords=cords2[:split1]+cords1[split1:split2]+cords2[split2:]
    
    return Chromosome(child1_cords), Chromosome(child2_cords)

def mutation(Chromosome):
    if random.random()<mutationRate:
        ind= random.randint(0, len(order)-1)
        
        nx=random.randint(0,gridsize-1)
        ny=random.randint(0,gridsize-1)
        
        Chromosome.cordinates[ind*2]=nx
        Chromosome.cordinates[ind*2 +1]= ny
    return Chromosome

def geneticAlgorithm():
    population=[Chromosome() for _ in range(populationMax)]
    result= None
    print("----Started----")
    
    for gen in range(generationTime):
        for ind in population:
            fitness(ind)
        best_fit=max(population,key=lambda ind:ind.fitness)
        if result is None or best_fit.fitness>result.fitness:
            result=Chromosome(best_fit.cordinates[:])
            fitness(result)
            
        new_population=[]
        population.sort(key=lambda ind: ind.fitness, reverse=True)
        new_population.extend(population[:elitismCount])
    
        while len(new_population)<populationMax:
            parentA, parentB = parents(population)
            childA,childB= crossover(parentA,parentB)
        
            mutatedA=mutation(childA)
            mutatedB=mutation(childB)
        
            new_population.extend([mutatedA,mutatedB])
        population=new_population
        print(f"generation: {gen+1}/{generationTime}, Best fitness: {result.fitness:.2f}")
    
    overlap,wire,area= fitness(result)
    print("Finished")
    print("found - ")
    print(f" -- Total Fitness: {result.fitness:.2f}")
    print(f" -- Overlap count: {overlap}, penalty: {overlap*overlapCost}")
    print(f" -- Wire length: {wire}, penalty: {wire*wireCost}")
    print(f" -- Bounding Box Area: {area}, penalty: {area*boundingCost}")
    print()
    print("Optional bottom-left coordinates:")
    for i in range(len(order)):
        name=order[i]
        x= result.cordinates[i*2]
        y=result.cordinates[i*2 +1]
        print(f"   ==  {name}: ({x}, {y})")

if __name__=="__main__":
    geneticAlgorithm()