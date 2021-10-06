'''
Data Mining Assignment 2, K-Means
2016253072
명수환(Myeong Suhwan)

'''

import re
import random
import time
import math



def getDataFromFile(filename):
    input_file = open(filename, 'r')
    gene_id = dict()
    
    line_num = 0
    for line in input_file:
        time_point_data = line.split()
        gene_id[line_num] = time_point_data
        
        line_num += 1
        
        
    return gene_id

def randClustering(gene_id):
    cluster = list() # k개의 cluster 생성, k : 10
    
    k = 10
    init_mem_num_in_cluster = int(len(gene_id) / k)
    line_num = 0

    for i in range(0,len(gene_id)-1,init_mem_num_in_cluster):
        same_cluster = list()
        for i in range(init_mem_num_in_cluster):
            same_cluster.append(line_num)
            line_num += 1    
        cluster.append(same_cluster)

    return cluster

def getKMeans(cluster,cluster_num,gene_id):
    kmeans = [0,0,0,0,0,0,
                0,0,0,0,0,0,] #* 12-dimension
    #print(gene_id[cluster[0][0]][1])
    #print("cluster",cluster_num," => ",cluster[cluster_num])
    if len(cluster[cluster_num]) == 1:
        return gene_id[cluster[cluster_num][0]]

    for i in range(DIMENSION):
        #print(float(gene_id[cluster[0][0]][i]) - float(gene_id[cluster[0][1]][i]))
        tmp = float(gene_id[cluster[cluster_num][0]][i]) + float(gene_id[cluster[cluster_num][1]][i])
        tmp /= 2
        kmeans[i] = tmp
    #print("sum : ",kmeans)
    
    return kmeans

def getDistance(kmeans, object):
    dist = 0
    #print("kmeans : ", kmeans)
    #print("data object : ", object)
    for dimension in range(DIMENSION):
        dist_dimesion = float(kmeans[dimension]) - float(object[dimension])
        tmp = pow(dist_dimesion,2)
        dist += tmp
    dist = math.sqrt(dist)
    
    return dist

def Reassign(obj_num, to,from_cluster_num,cluster):
    print(obj_num,"이", "cluster",to,"에 추가되었습니다.")

    #* add to new cluster
    cluster[to].append(obj_num)#obj말고 obj의 라인 넘버를 줘야함
    #print(cluster[to])
    #* remove from old cluster
    #print(cluster[from_cluster_num])
    
    cluster[from_cluster_num].remove(obj_num)
    #print(cluster[from_cluster_num])



def main():
    start_time = time.time()
    global DIMENSION,k
    DIMENSION = 12
    k = 10
    filename = 'assignment2_input.txt' #500
    #filename = 'test1.txt'

    gene_id = getDataFromFile(filename)
    #print(len(gene_id))
    cluster = randClustering(gene_id)
    print("Start . . . ")
    print(cluster)
    for num in range(k):
        print("cluster",num,cluster[num])
        for i in range(len(cluster[num])):
            print(gene_id[cluster[num][i]])
        print("\n")
    #print(cluster)
    #print("cluster",0,":",cluster[0][0], cluster[0][1])

    # * get K-means value at all clusters
    
    change = True
    count_for_debug = 0
    while change:
        print("=============================================\n\n\n")
        print(count_for_debug+1,"번 반복하였습니다.")
        count_for_debug += 1
        change = False
        for cluster_num in range(k):
                
            
            print("Cluster : ", cluster_num)
            print("클러스터 내 오브젝트의 개수",len(cluster[cluster_num]))
            iter_index = 0
            while iter_index < len(cluster[cluster_num]):

                for i in range(k):
                    if cluster_num == i:
                        continue
                    if not (cluster[cluster_num] and cluster[i]):
                        continue
                    
                    kmeans = getKMeans(cluster,cluster_num,gene_id) # [0,1]
                    #print(cluster[cluster_num])
                    #print(iter_index)
                    distance = getDistance(kmeans,gene_id[cluster[cluster_num][iter_index]]) #!
                    #print("distance : ",distance) # * distance between k-means and an object in a cluster
                    #print("kmeans :",kmeans)
                    
                    #print("cluster num: ",cluster_num,cluster[cluster_num],"with cluster ", i)
                    if cluster[cluster_num] and cluster[i]:
                        
                        kmeans = getKMeans(cluster,i,gene_id)#* i cluster의 K-Means
                        
                    
                        
                        dist = getDistance(kmeans,gene_id[cluster[cluster_num][iter_index]]) # * i cluster의 K-Means까지의 Distance
                        
                        #print("dist : ",dist)
                        #print(cluster[cluster_num][iter_index],"오브젝트에 대하여 ", end=" ")
                        #print("cluster",cluster_num,"의 K-Means와","cluster",i,"의 K-Means중 가까운 것을 찾는 중입니다.")
                        if dist < distance:
                            print(cluster[cluster_num][iter_index],"오브젝트에 대하여 ", end=" ")
                            print("cluster",cluster_num,"의 K-Means와","cluster",i,"의 K-Means중 가까운 것을 찾는 중입니다.")
                            print("거리가 더 가까운 K-Means를 찾았습니다.")
                            #print("shorter distance : ", dist)
                            #print(">cluster : ", i)
                            obj_num = cluster[cluster_num][iter_index]
                            #print("obj number>>",obj_num)
                            to = i
                            Reassign(obj_num,to,cluster_num,cluster)
                            print("\n")
                            change = True
                            iter_index -= 1
                            if iter_index < 0:
                                iter_index = 0
                            #! in here, Have to change to shortest cluster
                    
                    
                    else:
                        continue

                iter_index += 1
                
        # cluster_num = 1
        # kmeans = getKMeans(cluster,cluster_num,gene_id)
        # distance = getDistance(kmeans,gene_id[cluster[cluster_num][0]])
        # print(distance)
        #? and then, find the shortest distance with other K-Means of other clusters.
        #? after finding, Re-assign objects to clusters based on the distance that I've found.
        
        

    #print(cluster)
    print("\n\n")
    for i in range(k):
        cluster[i].sort()
        print(i,"번 클러스터 :","SIZE: ",len(cluster[i]), cluster[i])
        print("\n")
    print("Time Elapsed : ", time.time() - start_time)

if __name__ == '__main__':
    main()