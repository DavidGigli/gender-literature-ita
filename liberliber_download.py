import time
from selenium import webdriver


in_autori=open("/home/masterbd/progetto/autori+wiki_finito.txt","r").readlines()
in_url=open("/home/masterbd/progetto/autori_a_z.txt","r").readlines()

lista_url=[]
autori=[x.split("|") for x in in_autori]
url=[x.split("|") for x in in_url]
#join=[x+y for x in in_autori for y in in_url if (x.split("|")[1]==y.split("|")[0] and (int(x.split("|")[3].strip())>1799 and (x.split("|")[3].strip()=="italiano" or x.split("|")[3].strip()=="italiana")))]

join=[x.rstrip()+" | "+y.split("|")[1] for x in in_autori for y in in_url if (x.split("|")[1].strip()==y.split("|")[0].strip())]
italian=[x for x in join if (x.split("|")[4].strip()=="italiano" or x.split("|")[4].strip()=="italiana")]

print(italian[1])
epoc=[]
for item in italian:
	if item.split("|")[3].strip()=="":
		print(item)
	elif int(item.split("|")[3].strip())>1799:
		epoc.append(item)
print(epoc)

out_aut=open("/home/masterbd/progetto/elenco_autori.txt","w")
for item in epoc:
	out_aut.write(item)
out_aut.close()
#for item in join
#join=[x.split("|")[0].strip() for x in in_autori if (int(x.split("|")[3].strip())>1799 and (x.split("|")[3].strip()=="italiano" or x.split("|")[3].strip()=="italiana"))]
