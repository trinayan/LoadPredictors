

f=open('blackmulti.txt', 'r')
table=[]
for line in f:
	
	   table.append(line);

print len(table);
print len(table[3]);
count=0;
threadid=[]
ip=[]
loadval=[]

for i in range(3,len(table)-1):

	string=table[i];
	
	thread=string[0];
	thread=int(thread)
	threadid.append(thread);
			
	instructions=string[3:16]
	instructions=int(instructions,16);
	ip.append(instructions);

	loads=string[-23:]
	loads=int(loads);
	loadval.append(loads);

	
pcorrect=pincorrect=npcorrect=npincorrect=0;


LVPT1={};
LVPT2={};
LVPT3={};
LVPT4={};

for i in range(0,len(ip)):
	key=ip[i]%512;
	LVPT1[key]=[0,0];
	LVPT2[key]=[0,0];
	LVPT3[key]=[0,0];
	LVPT4[key]=[0,0];

correct=0;	
incorrect=0;

for i in range(0,len(ip)):
	key=ip[i]%512;
	answer=loadval[i];
	tid=threadid[i];

	if(tid==0):
		value=LVPT1[key];
		predict=value[0]
		confidence=value[1];
	elif(tid==1):
		value=LVPT2[key];
		predict=value[0]
		confidence=value[1];
	elif(tid==2):
		value=LVPT3[key];
		predict=value[0]
		confidence=value[1];
	elif(tid==3):
		value=LVPT4[key];
		predict=value[0]
		confidence=value[1];	

	if(confidence>1):
	   if(answer==predict):
	   	pcorrect=pcorrect+1;
	   	confidence=confidence+1;
	   	if(confidence>=3):
	   		confidence=3

	   	elif(answer!=predict):
	   	 pincorrect=pincorrect+1;
	   	 confidence=confidence-1;
	   	 if(confidence<=0):
	   	    confidence=0;
	elif(confidence<=1):
	    if(answer==predict):
	       npcorrect=npcorrect+1;
	       confidence=confidence+1;
	       if(confidence>=3):
	          confidence=3;
	    elif(answer!=predict):
	        npincorrect=npincorrect+1;
	        confidence=confidence-1;
	        if(confidence<=0):
	           confidence=0;

	if(tid==0):
		LVPT1[key]=[loadval[i],confidence];
		
	elif(tid==1):
		LVPT2[key]=[loadval[i],confidence];
		
	elif(tid==2):
		LVPT3[key]=[loadval[i],confidence];
		
	elif(tid==3):
		LVPT4[key]=[loadval[i],confidence];
		           

total=pcorrect+pincorrect;
accuracy=(pcorrect*100)/total;
print (accuracy);
ptotal=pcorrect+npincorrect;
cov=(pcorrect*100)/len(ip);
print (cov);

print LVPT1;
print LVPT4;

