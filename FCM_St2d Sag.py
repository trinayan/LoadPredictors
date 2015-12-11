

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
loads=[]
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

Stride={};

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	count=0;
	Stride[key]=[0,0,0];

stride1=0;
stride2=0;

SHRT={};

for i in range(0,len(ip)): 
 key=(ip[i])%tsize;
 SHRT[key]=0;



SPRT={}
for i in range(0,historymax):
	
	SPRT[i]=0;

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;	


for i in range(0,len(ip)-1):
	key=(ip[i])%tsize;
	

	value=Stride[key];
	last_value=value[0];
	stride1=value[1];
	stride2=value[2];
	Spredict=last_value+stride2;
	Shistory=SHRT[key]
	Sconfidence=SPRT[Shistory]

	fcmvalue=FCM[key];
	hash1=fcmvalue[0]
	hash2=fcmvalue[1];
	hash3=fcmvalue[2];
	hash4=fcmvalue[3];

	line=(hash1)^(hash2*2)^(hash3*4)^(hash4*8);


	FCMpredict=Lookup[line]
	FCMhistory=FCMHRT[key];
	FCMconfidence=FCMPRT[FCMhistory];

	if(FCMconfidence>Sconfidence):
		confidence=FCMconfidence;
		predict=FCMpredict;
	elif(FCMconfidence<Sconfidence):
	    confidence=Sconfidence;
	    predict=Spredict;
	elif(FCMconfidence==Sconfidence):
	    confidence=FCMconfidence;
	    predict=FCMpredict;

	answer=loadval[i];

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

	if(answer==Spredict):
		Sconfidence=Sconfidence+1;
		if(Sconfidence>countermax):
			Sconfidence=countermax;
		Shistoryvalue=1;

	elif(answer!=Spredict):
	    Sconfidence=Sconfidence-1;
	    if(Sconfidence<0):
	        Sconfidence=0;
	    Shistoryvalue=0

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

	SPRT[Shistory]=Sconfidence;
	Shistory=Shistory<<1;
	Shistory=Shistory | Shistoryvalue;
	Shistory&=(1<<historylength)-1
	SHRT[key]=Shistory;

	temp=answer-last_value;
	temp=temp&(0xFF);

	if(temp==stride1):
		stride2=temp;
	stride1=temp;
	Stride[key]=[loadval[i],stride1,stride2];


accuracy=(pcorrect*100)/(pcorrect+pincorrect);

print accuracy;


cov=(pcorrect*100)/len(ip);

print (cov);



	         

	    

	    







	




