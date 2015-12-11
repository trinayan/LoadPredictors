
tsize=128;


historylength=4;
historymax=pow(2,historylength);

f=open('mcf.txt', 'r')
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

Stride={};

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	count=0;
	Stride[key]=[0,0,0];

stride1=0;
stride2=0;

HRT={};

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    HRT[key]=0;

print len(HRT);



PRT={}
for i in range(0,historymax):
	
	PRT[i]=0;

print len(PRT);

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;
historyvalue=0;	

for i in range(0,len(ip)-1):
	key=(ip[i])%tsize;
	answer=loadval[i];
	value=Stride[key];

	last_value=value[0];
	stride1=value[1];
	stride2=value[2];
	predict=last_value+stride2;

	historyindex=HRT[key];
	confidence=PRT[historyindex];

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
	
	PRT[historyindex]=confidence;
	historyindex=historyindex<<1;
	historyindex=historyindex | historyvalue;
	historyindex&=(1<<historylength)-1;
	HRT[key]=historyindex;

	temp=answer-last_value;
	temp=temp&(0xFF);

	if(temp==stride1):
		stride2=temp;
	stride1=temp;
	Stride[key]=[loadval[i],stride1,stride2];


total=pcorrect+pincorrect;
accuracy=(pcorrect*100)/total;
print accuracy;
ptotal=pcorrect+npincorrect;
cov=(pcorrect*100)/ptotal;
print cov;








