import math
class Agent:
    def __init__(self,turn):
        if turn=="First":
            self.fplayer=True
        else: self.fplayer=False
def minimax (position, depth, alpha, beta, maxiplayer,id,pool,target):
    if depth == 0:
        return utility(position, target, id), position
    if maxiplayer:
        best_pos = position
        maxvalue=-math.inf
        for child in range(len(pool)):
            pool2 = pool.copy()
            nucleotide = pool2.pop(child)
            new_position = position + nucleotide
            value, pos = minimax(new_position, depth-1, alpha, beta, not maxiplayer, id, pool2, target)
            if value > maxvalue:
                maxvalue = value
                best_pos = pos
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return maxvalue, best_pos
    
    else:
        minvalue=math.inf
        best_pos=position
        for child in range(len(pool)):
            pool2 = pool.copy()
            nucleotide = pool2.pop(child)
            new_position = position + nucleotide
            value, pos= minimax(new_position, depth-1, alpha, beta, not maxiplayer, id, pool2, target)
            if value < minvalue:
                minvalue = value
                best_pos = pos
            beta = min(beta, value)
            if beta <= alpha:
                break
        return minvalue, best_pos

def utility(pos,target,id):
    sum=0
    for i in range(len(target)):
        x=id[i]*abs(ord(pos[i])-ord(target[i]))
        sum+=x
    return -sum

def utility2(pos,target,id):
    sum=0
    if "S" in pos:
        num=''
        ind=pos.index('S')
        for i in ID_Constant[:2]:
            num+=str(i)
        num=int(num)
        for _ in range(ind,len(id)):
            id[_]=id[_]*num/100
        for i in range(len(target)):
            x=id[i]*abs(ord(pos[i])-ord(target[i]))
            sum+=x
    return -sum

nucleotides_pool= list(map(str, input().split(",")))
target=input()
ID_Constant= list(map(int, input().split()))

agent1=Agent("First")
agent2=Agent("Second")

def solve(pool, target, Id):
    Id=Id[len(target):]
    path=""
    sudo_pool=pool.copy()
    best_val,pos=minimax(path, len(pool), -math.inf, math.inf,agent1.fplayer,Id,sudo_pool,target)
    return best_val, pos

r1,p1=solve(nucleotides_pool, target, ID_Constant)

print (f"Best gene sequence generated: {p1}")
print(f"Utility score: {r1}")