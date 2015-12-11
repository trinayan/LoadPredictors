
import matplotlib.pyplot as plt
import numpy as np


historylength=16;
historymax=pow(2,historylength);

tsize=512;

f=open('blackscholes.txt', 'r')
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


LVPT={}

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	count=0;
	LVPT[key]=0;



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
historyvalue=0;

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	answer=loadval[i];
	predict=LVPT[key];

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

	LVPT[key]=loadval[i];






total=pcorrect+pincorrect;


accuracy=(pcorrect*100)/total;
print accuracy;

cov=(pcorrect*100)/len(ip);

print cov;
		    	




