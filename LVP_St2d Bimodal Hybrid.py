
tsize=2048;
countermax=3;
counterthres=1;

f=open('swaptions.txt', 'r')
table=[]
for line in f:
  
    table.append(line);
  

ip=[];
loadval=[];
for i in range(3,len(table)-1):
  stringvalue=table[i];
  b=stringvalue[0:13];
  b=int(b,16);
  ip.append(b);

  c=stringvalue[-22:];
  c=int(c);
  loadval.append(c);

LVPT={};

for i in range(0,len(ip)-1):
	key=(ip[i])%tsize;
	count=0;
	LVPT[key]=[0,0];

Stride={}
for i in range(0,len(ip)-1):
  key=(ip[i])%tsize;
  count=0;
  Stride[key]=[0,0,0,0];

stride1=0;
stride2=0;

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;


for i in range(0,len(ip)):
  key=(ip[i])%tsize
  answer=loadval[i]

  value=LVPT[key];
  LVpredict=value[0]
  LVcounter=value[1]

  value=Stride[key];
  last_value=value[0]
  stride1=value[1]
  stride2=value[2]
  Scounter=value[3]
  Spredict=last_value+stride2;

  if(Scounter>LVcounter):
    confidence=Scounter;
    predict=Spredict;
  elif(Scounter<LVcounter):
     confidence=LVcounter;
     predict=LVpredict;
  elif(Scounter==LVcounter):
     confidence=Scounter;
     predict=Spredict;

  if(confidence>counterthres):
     if(answer==predict):
        pcorrect=pcorrect+1;
     else:
        pincorrect=pincorrect+1; 
  elif(confidence<=counterthres):
      if(answer==predict):
         npcorrect=npcorrect+1;
      else:
         npincorrect=npincorrect+1;              

  if(answer==Spredict):
     Scounter=Scounter+1;
     if(Scounter>countermax):
        Scounter=countermax;
  elif(answer!=Spredict):
     Scounter=Scounter-1;
     if(Scounter<0):
        Scounter=0;

  if(answer==LVpredict):
     LVcounter=LVcounter+1;
     if(LVcounter>countermax):
        LVcounter=countermax;
  elif(answer!=LVpredict):
      LVcounter=LVcounter-1;
      if(LVcounter<0):
         LVcounter=0;

  LVPT[key]=[loadval[i],LVcounter];
  
  temp=answer-last_value;
  temp=temp&(0xFF)
  if(temp==stride1):
    stride2=temp;
  stride1=temp;
  Stride[key]=[loadval[i],stride1,stride2,Scounter];  

total=pcorrect+pincorrect;
accuracy=(pcorrect*100)/total;
print accuracy;

cov=(pcorrect*100)/len(ip);

print cov;


  







  

