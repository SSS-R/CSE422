#task 1

import heapq,math

file= open('input3.txt')

N, M = map(int, file.readline().split())
xi, yi = map(int, file.readline().split())
xl, yl = map(int, file.readline().split())

board=[]

for _ in range(N):
    x=file.readline().replace("\n","").replace(" ","")
    x= [i for i in x]
    board.append(x)

directions=[(0,-1), (0,1), (-1,0), (1,0)]
directionsNames=["L", "R", "U", "D"]

def heuristic(preset,end):
    px, py = preset
    ex, ey = end
    heu= abs(px-ex)+ abs(py-ey)
    return heu

def maze(board, start, end, directions, directionsNames):
    d_cost={start: 0}
    visited=[]
    parents={}
    que=[]
    heapq.heappush(que,(heuristic(start,end),0,start))
    
    while que:
        f_cost, g_cost, node = heapq.heappop(que)
        if node==end:
            path=[]
            while node in parents:
                prev, move= parents[node]
                path.append(move)
                node =prev
            path.reverse()
            return len(path), "".join(path)
        
        if node in visited:
            continue
        visited.append(node)
        px,py=node
        for i, (dx, dy) in enumerate(directions):
            nx , ny = px+dx , py+dy
            newNode=(nx,ny)
            
            if 0<=nx<N and 0<=ny<M and board[nx][ny]!="#":
                present_cost=g_cost+1
                if newNode not in d_cost or present_cost<d_cost[newNode]:
                    parents[newNode]=(node, directionsNames[i])
                    d_cost[newNode]=present_cost
                    f_cost=present_cost+heuristic(newNode,end)
                    heapq.heappush(que,(f_cost,present_cost,newNode))
    return -1, "-1"

start =(xi, yi)
end = (xl,yl)
cost, path= maze(board, start, end, directions, directionsNames)

print(cost)
if path!="-1":
    print(path)

#task 2

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