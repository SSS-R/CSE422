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