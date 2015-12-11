historylength=4;
historymax=pow(2,historylength);

counterthres=1;
countermax=3;

tsize=512;

f=open('linpack.txt', 'r')
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

L4V={};

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	count=0;
	L4V[key]=[0,0,0,0];

HRT={}
for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    HRT[key]=[0,0,0,0];

PRT1={}
PRT2={}
PRT3={}
PRT4={}
for i in range(0,historymax):
	
	PRT1[i]=0;
	PRT2[i]=0;
	PRT3[i]=0;
	PRT4[i]=0;

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;
historyvalue=0;
conf1=0;

historyvalue1=0;
historyvalue2=0;
historyvalue3=0;
historyvalue4=0

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	answer=loadval[i];

	value=L4V[key]

	predict1=value[0]
	predict2=value[1]
	predict3=value[2]
	predict4=value[3]

	value2=HRT[key];

	history1=value2[0]
	history2=value2[1]
	history3=value2[2]
	history4=value2[3]

	

	conf1=PRT1[history1];
	conf2=PRT2[history2]
	conf3=PRT3[history3]
	conf4=PRT4[history4];

	

	bestconf=max(conf1,conf2,conf3,conf4)

	if(conf1==bestconf):
		prediction=predict1;
	elif(conf2==bestconf):
		prediction=predict2;
	elif(conf3==bestconf):
	    prediction=predict3;
	elif(conf4==bestconf):
	    prediction=predict4;

	if(bestconf>counterthres):
		if(answer==prediction):
		   pcorrect=pcorrect+1;
		else:
		   pincorrect=pincorrect+1;
	elif(bestconf<=counterthres):
	    if(answer==prediction):
	       npcorrect=npcorrect+1;
	    else:
	       npincorrect=npincorrect+1;

	if(answer==predict1):
	    conf1=conf1+1;
	    if(conf1>countermax):
	       conf1=countermax;
	    historyvalue1=1;
	elif(answer!=predict1):
		conf1=conf1-1;
		if(conf1<0):
			conf1=0;
		historyvalue1=0;

	if(answer==predict2):
	    conf2=conf2+1;
	    if(conf2>countermax):
	       conf2=countermax;
	    historyvalue2=1;
	if(answer!=predict2):
	    conf2=conf2-1;
	    if(conf2<0):
	       conf2=0;
	    historyvalue2=0; 

	if(answer==predict3):
	    conf3=conf3+1;
	    if(conf3>countermax):
	       conf3=countermax;
	    historyvalue3=1;
	if(answer!=predict3):
	    conf3=conf3-1;
	    if(conf3<0):
	       conf3=0;
	    historyvalue3=0;  

	if(answer==predict4):
	    conf4=conf4+1;
	    if(conf4>countermax):
	       conf4=countermax;
	    historyvalue4=1;
	if(answer!=predict4):
	    conf4=conf4-1;
	    if(conf4<0):
	       conf4=0;
	    historyvalue4=0;  

	PRT1[history1]=conf1;
	PRT2[history2]=conf2;
	PRT3[history3]=conf3;
	PRT4[history4]=conf4;
	history1=history1<<1;
	history1=history1 | historyvalue1;
	history1&=(1<<historylength)-1;
	history2=history2<<1;
	history2=history2 | historyvalue2;
	history2&=(1<<historylength)-1;
	history3=history3<<1;
	history3=history3 | historyvalue3;
	history3&=(1<<historylength)-1;
	history4=history4<<1;
	history4=history4 | historyvalue4;
	history4&=(1<<historylength)-1;
	HRT[key]=[history1,history2,history3,history4];
	predict4=predict3;
	predict3=predict2;
	predict2=predict1;
	predict1=loadval[i];
	L4V[key]=[predict1,predict2,predict3,predict4];



accuracy=(pcorrect*100)/(pcorrect+pincorrect);
print accuracy;

cov=(pcorrect*100)/len(ip);

print cov;     

print L4V

	    

	      
	


























