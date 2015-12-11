
tsize=2048;
counter_max=3
counter_thres=1

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

FCM={};
Lookup={}

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    FCM[key]=[0,0,0,0,0];

 

hash1=0;hash2=0;hash3=0;hash4=0;

for i in range(0,2049):
    Lookup[i]=0;

LVPT={};

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	count=0;
	LVPT[key]=[0,0];

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;


for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	answer=loadval[i]

	value=LVPT[key]
	LVpredict=value[0]
	LVcounter=value[1]

	fcmvalue=FCM[key]

	hash1=fcmvalue[0]
	hash2=fcmvalue[1]
	hash3=fcmvalue[2]
	hash4=fcmvalue[3]
	FCMcounter=fcmvalue[4]

	line=(hash1)^(hash2*2)^(hash3*4)^(hash4*8)
	

	FCMpredict=Lookup[line]

	if(FCMcounter>LVcounter):
		confidence=FCMcounter;
		predict=FCMpredict;
	elif(FCMcounter<LVcounter):
	    confidence=LVcounter;
	    predict=LVpredict;
	elif(FCMcounter==LVcounter):
	    confidence=FCMcounter;
	    predict=FCMpredict;

	if(confidence>counter_thres):
	   if(answer==predict):
	      pcorrect=pcorrect+1;
	   else:
	      pincorrect=pincorrect+1;
	elif(confidence<=counter_thres):
	    if(answer==predict):
	       npcorrect=npcorrect+1;
	    else:
	       npincorrect=npincorrect+1;         

	if(answer==FCMpredict):
		FCMcounter=FCMcounter+1;
		if(FCMcounter>counter_max):
			FCMcounter=counter_max
	elif(answer!=FCMpredict):
	    FCMcounter=FCMcounter-1;
	    if(FCMcounter<0):
	    	FCMcounter=0

	if(answer==LVpredict):
	    LVcounter=LVcounter+1;
	    if(LVcounter>counter_max):
	       LVcounter=counter_max;
	elif(answer!=LVpredict):
	    LVcounter=LVcounter-1;
	    if(LVcounter<0):
	       LVcounter=0;

	LVPT[key]=[loadval[i],LVcounter]

	Lookup[line]=loadval[i]

	hash4=hash3;
	hash3=hash2;
	hash2=hash1;
	hash1=(answer & 0xFF)^((answer & 0xFF00)>>8)^((answer & 0xFF0000)>>16)^((answer & 0xFF000000)>>24) ;

	FCM[key]=[hash1,hash2,hash3,hash4,FCMcounter];


accuracy=(pcorrect*100)/(pcorrect+pincorrect);
print accuracy;

ptotal=pcorrect+npincorrect;
cov=(pcorrect*100)/len(ip);

print cov;













