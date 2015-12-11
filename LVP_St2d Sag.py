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

LVPT={};


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
historyvalue=0;
confidence=0;



for i in range(0,len(ip)-1):
	key=(ip[i])%tsize;
	answer=loadval[i];

	LVpredict=LVPT[key]
	LVhistory=LVHRT[key]
	LVconfidence=LVPRT[LVhistory]

	value=Stride[key];
	last_value=value[0];
	stride1=value[1];
	stride2=value[2];
	Spredict=last_value+stride2;
	Shistory=SHRT[key]
	Sconfidence=SPRT[Shistory]

	if(Sconfidence>LVconfidence):
		confidence=Sconfidence;
		
		predict=Spredict
	elif(Sconfidence<LVconfidence):
		confidence=LVconfidence;
		
		predict=LVpredict
	elif(Sconfidence==LVconfidence):
		confidence=Sconfidence;
		
		predict=Spredict

	if(confidence>counterthres):
		if(answer==predict):
		    pcorrect=pcorrect+1;
		else:
		    pincorrect=pincorrect+1;
	elif(confidence<=counterthres):

		if(answer==predict):
			npcorrect=npcorrect+1;
        elif(answer!=predict):
        	npincorrect=npincorrect+1; 	    

	
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




total=pcorrect+pincorrect;
accuracy=(pcorrect*100)/total;
print accuracy;



ptotal=pcorrect+npincorrect;
cov=(pcorrect*100)/len(ip);

print cov;
            	
		

























    	




		    




		

		



	