import json,os,sys,urllib.error as u,urllib.request as r
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit()
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
Q={"p":[0,0,0,0,50,50,50,50,10,20,30,30,5,10,25,25],"n":[-50,-30,-30,-30,-40,0,0,0,-30,10,15,15,-30,5,20,20],"b":[-20,-10,-10,-10,-10,0,0,0,-10,5,10,10,-10,5,10,10],"r":[0,0,0,0,5,10,10,10,-5,0,0,0,-5,0,0,0],"q":[-20,-10,-5,-5,-10,0,0,0,-10,5,5,5,-5,5,5,5],"k":[-30,-40,-50,-50,-30,-40,-50,-50,-30,-40,-50,-50,-20,-30,-40,-40]}
def P(p,s):r,f=divmod(s,8);return Q[p][(7-r if r>3 else r)*4+(7-f if f>3 else f)]
def post(p,b):
 q=r.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with r.urlopen(q) as x:return json.load(x)
 except u.HTTPError:sys.exit()
def board(f):
 b={};k=7
 for x in f.split()[0].split("/"):
  j=0
  for c in x:
   if c.isdigit():j+=int(c)
   else:b[j+k*8]=c;j+=1
  k-=1
 return b
def ev(b,s):
 t=0
 for q,c in b.items():
  v=c.lower();t+=V[v]+P(v,q) if c.isupper() else -(V[v]+P(v,q))
 return t if s==1 else -t
def mg(b,s):
 M=[]
 for q,c in b.items():
  if (c.isupper() and s==1)or(c.islower() and s==-1):
   p=c.lower();r,f=divmod(q,8)
   if p=='p':
    d=-1 if s==1 else 1;t=q+d*8
    if 0<=t<64 and t not in b:
     M.append((q,t,'q') if r+d in(0,7) else (q,t,None))
     if(r==1 and s==1)or(r==6 and s==-1):
      t2=q+2*d*8
      if t2 not in b:M.append((q,t2,None))
    for df in(-1,1):
     f2=f+df
     if 0<=f2<8:
      t=q+d*8+df
      if 0<=t<64 and t in b:
       cap=b[t]
       if(s==1 and cap.islower())or(s==-1 and cap.isupper()):M.append((q,t,'q') if r+d in(0,7) else (q,t,None))
   elif p=='n':
    for dr,df in((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)):
     r2,f2=r+dr,f+df
     if 0<=r2<8 and 0<=f2<8:
      t=r2*8+f2
      if t not in b or(s==1 and b[t].islower())or(s==-1 and b[t].isupper()):M.append((q,t,None))
   elif p in'brq':
    D=((1,0),(-1,0),(0,1),(0,-1)) if p=='r' else ((1,1),(1,-1),(-1,1),(-1,-1)) if p=='b' else((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
    for dr,df in D:
     r2,f2=r+dr,f+df
     while 0<=r2<8 and 0<=f2<8:
      t=r2*8+f2
      if t in b:
       if(s==1 and b[t].islower())or(s==-1 and b[t].isupper()):M.append((q,t,None))
       break
      M.append((q,t,None));r2+=dr;f2+=df
   else:
    for dr,df in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
     r2,f2=r+dr,f+df
     if 0<=r2<8 and 0<=f2<8:
      t=r2*8+f2
      if t not in b or(s==1 and b[t].islower())or(s==-1 and b[t].isupper()):M.append((q,t,None))
 return M
def mk(b,m,s):
 nb=dict(b);frm,to,pr=m;pc=nb.pop(frm)
 nb[to]='Q' if pr and s==1 else 'q' if pr else pc;return nb
N=[0]
def sr(b,s,d,a,be,bd):
 N[0]+=1
 if N[0]>bd or d==0:return ev(b,s)
 M=mg(b,s)
 if not M:return -20000+(50-d)
 best=-999999
 for m in M:
  sc=-sr(mk(b,m,s),-s,d-1,-be,-a,bd)
  if sc>best:best=sc
  if sc>a:a=sc
  if a>=be:break
 return best
def bm(fen,leg,bd):
 b=board(fen);s=1 if fen.split()[1]=='w' else -1
 N[0]=0;best=None;bs=-999999;d=3
 for m0 in leg:
  frm=(int(m0[1])-1)*8+ord(m0[0])-97;to=(int(m0[3])-1)*8+ord(m0[2])-97
  pr=m0[4] if len(m0)==5 else None
  sc=-sr(mk(b,(frm,to,pr),s),-s,d-1,-999999,999999,bd)
  if sc>bs:bs=sc;best=m0
 return best
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":bm(g["fen"],g["legal_moves"],4000)})
 if g.get("outcome") is not None:print(f"g {g['game']}: {g['outcome']}",file=sys.stderr)
print("done",file=sys.stderr)
