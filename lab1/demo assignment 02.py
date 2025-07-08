import heapq,math
from collections import deque
file= open('input3b.txt')

N, M = map(int, file.readline().split())
x=file.readline()
iv, lv = map(int, file.readline().split())
x=file.readline()

nodes=[0]*(N+1)
hue=[0]*(N+1)
graph={}
for i in range(1,N+1):
    graph[i]=[]

for _ in range(N):
    x,y=map(int,file.readline().split())
    node=(x,y)
    nodes[x]=node
    hue[x]=y
x=file.readline()

for _ in range(M):
    u,v = map(int,file.readline().split())
    graph[u].append(v)
    graph[v].append(u)

def admissibilityCheck(graph, end, hue):
    def UCS(graph,end):
        dis=[math.inf]*(N+1)
        dis[end]=0
        que=deque([end])
        
        while que:
            node= que.popleft()
            for child in graph[node]:
                if dis[child]==math.inf:
                    dis[child]=dis[node]+1
                    que.append(child)
        return dis
    uno_cost=UCS(graph,end)
    
    inadmissible = []
    for node in range(1, N+1):
        cost=hue[node]
        real_cost = uno_cost[node]
        if cost>real_cost:
            return 0
    if len(inadmissible) == 0:
        print(1)
    else:
        print("Here nodes", end = " ")
        print(",".join(map(str, inadmissible)) , end = " ")
        print("are inadmissible.")

admissibilityCheck(graph, lv, hue)