import networkx as nx
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


file= open("twitter_combined.txt","r")
w= file.readlines()

#w=[w[i] for i in range(100000)]
#print(w)
d_count=set()

#dict to store ind to id
ind_id=dict()
#dict to store id to ind
id_ind=dict()

it=0

for i in w:
    spc_sep=i.split(' ')    
    spc_sep[1]=spc_sep[1].strip()    
    d_count.add(spc_sep[0])
    d_count.add(spc_sep[1])   

ct= len(d_count)
#ct= 81306
print(ct)  #81306 nodes confirmed in the dataset

#init for page rank
r=[1/ct]
r=r*ct

for i in d_count:
    id_ind[i]=it
    ind_id[it]=i
    it+=1

#stores number of outlinks for each node
out_links={}

for i in w:
    spc_sep=i.split(' ')
    spc_sep[1]=spc_sep[1].strip()

    if(spc_sep[0] in out_links):
        out_links[spc_sep[0]]+=1
    else:
        out_links[spc_sep[0]]=1
    
print("Done")

#stores in_links for each user node {dict of lists}
in_links={}

#populating in_links
for i in w:
    spc_sep=i.split(' ')
    spc_sep[1]=spc_sep[1].strip()

    if spc_sep[1] in in_links:
        in_links[spc_sep[1]].append(spc_sep[0])
    else:
        in_links[spc_sep[1]]=[spc_sep[0]]
        

#values for pagerank. beta and error for convergence
beta=0.8
ee=0.001
print("Done2")
iter=0

#for visualising r values over iterations
plt.axis([1, 21, 0, 4.0])
plt.ion()

xx= [i for i in range(1,21)]
xtix= [ind_id[i-1] for i in xx]


#loop for converging
while(1):
    #print("iter",iter)
    iter+=1
    r_dash=[0]*ct   
    
    for j in d_count:        
        fl=0
        sum_i=0        

        if j in in_links:
            links_i=in_links[j]

            for k in links_i:
                sum_i+=((beta*r[id_ind[k]])/out_links[k])                                                     
        
        r_dash[id_ind[j]]=sum_i
        
    #print(r_dash)
    S=0

    for j in d_count:
        S+=r[id_ind[j]]
    #print((1-S)/ct)
    for j in d_count:        
        r_dash[id_ind[j]]=r_dash[id_ind[j]]+((1-S)/ct)

    #print(r_dash)
    l_cond=0
    for j in range(len(r)):
        l_cond+=abs(r_dash[j]-r[j])

    
    #print(r)

    yy= [i*100000 for i in r[0:20]]

    plt.plot(xx,yy)
    plt.xticks(xx,xtix,rotation='vertical')
    plt.draw()
    plt.pause(0.05)

    r=r_dash

    if(l_cond<ee):
        break;

#print(r)

fin=[]
tem=0
for i in r:
    temp=[]
    temp.append(tem)
    temp.append(i)    
    tem+=1
    fin.append(temp)

fin.sort(key=lambda x: x[1],reverse=True)

SUM=0

for i in r:
    SUM+=i

pg_rnk={}
node_list=[]

for i in fin:
    pg_rnk[ind_id[i[0]]]=int(((i[1]*100)/SUM)*10000)
    node_list.append(ind_id[i[0]])
    
print("done3")   
#pg_rnk stores end values normalized and magnified by 10^5 as integer for dir graph

nodes=[]
edges=[]
sizes=[]
labels={}

for i in w[0:10]:
    spc_sep=i.split(' ')
    spc_sep[1]=spc_sep[1].strip()
    edges.append([spc_sep[0],spc_sep[1]])
    if spc_sep[0] not in nodes:
        nodes.append(spc_sep[0])
        sizes.append(pg_rnk[spc_sep[0]])
    if spc_sep[1] not in nodes:
        nodes.append(spc_sep[1])
        sizes.append(pg_rnk[spc_sep[1]])

ite=0
for i in nodes:
    labels[i]=sizes[ite]
    ite+=1

fig2=plt.figure()

g = nx.DiGraph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)

nx.draw_random(g, node_size = sizes, labels=labels, with_labels=True)    
fig2.show()


        


    
                
                
                
        
        
    

    


    
        
        

    
