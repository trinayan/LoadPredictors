
tsize=2048;
countermax=3;
counterthres=1;
count=0;

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

FCM={};
Lookup={}

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    FCM[key]=[0,0,0,0,0];

hash1=0;hash2=0;hash3=0;hash4=0;

for i in range(0,tsize):
    Lookup[i]=0;

Stride={}
for i in range(0,len(ip)):
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

  value=Stride[key];
  last_value=value[0]
  stride1=value[1]
  stride2=value[2]
  Scounter=value[3]
  Spredict=last_value+stride2;

  fcmvalue=FCM[key]

  hash1=fcmvalue[0]
  hash2=fcmvalue[1]
  hash3=fcmvalue[2]
  hash4=fcmvalue[3]
  FCMcounter=fcmvalue[4]

  line=(hash1)^(hash2*2)^(hash3*4)^(hash4*8)

  FCMpredict=Lookup[line]

  if(FCMcounter>Scounter):
        confidence=FCMcounter;
        predict=FCMpredict;
  elif(FCMcounter<Scounter):
        confidence=Scounter;
        predict=Spredict;
  elif(FCMcounter==Scounter):
        confidence=FCMcounter;
        predict=FCMpredict;

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


  if(answer==FCMpredict):
        FCMcounter=FCMcounter+1;
        if(FCMcounter>countermax):
            FCMcounter=countermax
  elif(answer!=FCMpredict):
        FCMcounter=FCMcounter-1;
        if(FCMcounter<0):
            FCMcounter=0;

  if(answer==Spredict):
        Scounter=Scounter+1;
        if(Scounter>countermax):
           Scounter=countermax;
  elif(answer!=Spredict):
        Scounter=Scounter-1;
        if(Scounter<0):
           Scounter=0;

  temp=answer-last_value;
  temp=temp&(0xFF)
  if(temp==stride1):
      count=count+1;

      stride2=temp;
  stride1=temp;
  Stride[key]=[answer,stride1,stride2,Scounter]; 

  hash4=hash3;
  hash3=hash2;
  hash2=hash1;
  hash1=(answer & 0xFF)^((answer & 0xFF00)>>8)^((answer & 0xFF0000)>>16)^((answer & 0xFF000000)>>24) ;

  FCM[key]=[hash1,hash2,hash3,hash4,FCMcounter];



accuracy=(pcorrect*100)/(pcorrect+pincorrect);
print (accuracy);

ptotal=pcorrect+npincorrect;
cov=(pcorrect*100)/len(ip);

print (cov);




                    












