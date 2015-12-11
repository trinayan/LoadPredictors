historylength=4;
historymax=pow(2,historylength);
counterthres=1;
countermax=3;
tsize=2048;





f=open('radixsort.txt', 'r')
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


FCM={}
Lookup={}

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    FCM[key]=[0,0,0,0];

hash1=0;hash2=0;hash3=0;hash4=0;

for i in range(0,tsize+1):
    Lookup[i]=0;

FCMHRT={};

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    FCMHRT[key]=0;

historylength=4;
historymax=pow(2,historylength);

FCMPRT={}
for i in range(0,historymax):
	
	FCMPRT[i]=0;

LVPT={}
for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	count=0;
	LVPT[key]=0;

LVHRT={};

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    LVHRT[key]=0;

LVPRT={}

for i in range(0,historymax):
	
	LVPRT[i]=0;

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;
historyvalue=0;

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	answer=loadval[i]

	LVpredict=LVPT[key]
	LVhistory=LVHRT[key]
	LVconfidence=LVPRT[LVhistory];

	fcmvalue=FCM[key];
	hash1=fcmvalue[0]
	hash2=fcmvalue[1];
	hash3=fcmvalue[2];
	hash4=fcmvalue[3];

	line=(hash1)^(hash2*2)^(hash3*4)^(hash4*8);

	FCMpredict=Lookup[line]
	FCMhistory=FCMHRT[key];
	FCMconfidence=FCMPRT[FCMhistory];

	if(FCMconfidence>LVconfidence):
		confidence=FCMconfidence;
		predict=FCMpredict;
	elif(FCMconfidence<LVconfidence):
	    confidence=LVconfidence;
	    predict=LVpredict;
	elif(FCMconfidence==LVconfidence):
	    confidence=FCMconfidence;
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
	    FCMconfidence=FCMconfidence+1;
	    if(FCMconfidence>countermax):
	       FCMconfidence=countermax;
	    FCMhistoryvalue=1;
	elif(answer!=FCMpredict):
	    FCMconfidence=FCMconfidence-1;
	    if(FCMconfidence<0):
	       FCMconfidence=0;
	    FCMhistoryvalue=0;

	if(answer==LVpredict):
	    LVconfidence=LVconfidence+1;
	    if(LVconfidence>countermax):
	       LVconfidence=countermax;
	    LVhistoryvalue=1;
	
	elif(answer!=LVpredict):
	    LVconfidence=LVconfidence-1;
	    if(LVconfidence<0):
	       LVconfidence=0;
	    LVhistoryvalue=0;

	LVPRT[LVhistory]=LVconfidence;
	LVhistory=LVhistory<<1;
	LVhistory=LVhistory | LVhistoryvalue;
	LVhistory&=(1<<historylength)-1;
	LVHRT[key]=LVhistory;

	LVPT[key]=loadval[i]

	FCMPRT[FCMhistory]=FCMconfidence;
	FCMhistory=FCMhistory<<1;
	FCMhistory=FCMhistory | FCMhistoryvalue
	FCMhistory&=(1<<historylength)-1;
	FCMHRT[key]=FCMhistory;

	Lookup[line]=loadval[i];

	hash4=hash3;
	hash3=hash2;
	hash2=hash1;
	hash1=(answer & 0xFF)^((answer & 0xFF00)>>8)^((answer & 0xFF0000)>>16)^((answer & 0xFF000000)>>24) ;
	
	FCM[key]=[hash1,hash2,hash3,hash4]




accuracy=(pcorrect*100)/(pcorrect+pincorrect);
print accuracy;

cov=(pcorrect*100)/len(ip);

print cov;


	
print FCM
	












