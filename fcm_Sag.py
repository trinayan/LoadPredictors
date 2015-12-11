tsize=2048;

historylength=4;
historymax=pow(2,historylength);

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
Lookup={};

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    FCM[key]=[0,0,0,0];

hash1=0;hash2=0;hash3=0;hash4=0;

for i in range(0,tsize):
    Lookup[i]=0;



HRT={};

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    HRT[key]=0;





PRT={}
for i in range(0,historymax):
	
	PRT[i]=0;


pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	answer=loadval[i];

	fcmvalue=FCM[key];

	hash1=fcmvalue[0];
	hash2=fcmvalue[1];
	hash3=fcmvalue[2];
	hash4=fcmvalue[3];

	line=(hash1)^(hash2*2)^(hash3*4)^(hash4*8);

	predict=Lookup[line];

	history=HRT[key];

	confidence=PRT[history];

	if (confidence>1):
		if(answer==predict):
			pcorrect=pcorrect+1;
			confidence=confidence+1;
			if(confidence>3):
				confidence=3;
			historyvalue=1;
		elif(answer!=predict):
		    pincorrect=pincorrect+1;
		    confidence=confidence-1;
		    if(confidence<0):
		    	confidence=0;
		    historyvalue=0;

	elif (confidence<=1):
		if(answer==predict):
			npcorrect=npcorrect+1;
			confidence=confidence+1;
			if(confidence>3):
				confidence=3;
			historyvalue=1;
		elif(answer!=predict):
		    npincorrect=npincorrect+1;
		    confidence=confidence-1;
		    if(confidence<0):
		    	confidence=0;
		    historyvalue=0;

	PRT[history]=confidence;
	history=history<<1;
	history=history | historyvalue;
	history&=(1<<historylength)-1;
	HRT[key]=history;

	Lookup[line]=loadval[i];

	hash4=hash3;
	hash3=hash2;
	hash2=hash1;
	hash1=(answer & 0xFF)^((answer & 0xFF00)>>8)^((answer & 0xFF0000)>>16)^((answer & 0xFF000000)>>24) ;
	
	FCM[key]=[hash1,hash2,hash3,hash4]


total=pcorrect+pincorrect;


accuracy=(pcorrect*100)/total;
print accuracy;

ptotal=pcorrect+npincorrect;
cov=(pcorrect*100)/ptotal;

print cov;	















