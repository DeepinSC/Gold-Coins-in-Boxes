#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:17:18 2017

@author: rick (廖庭辉,2014141463109)

@Statement : this program is for the extra task in "The theory of Probability and Statistics"

@Background: N gold coins random distribute in M boxes;
            Initially, you hve open a box which has K coins inside;
            Now,You have 2 choices:
                1. Pick up K coins and quit;
                2. Give up the K coins in this box and open another box.
            Write a program to choose Automatically.
            
    
@ 数学解法：
    这部分用中文写了，英文写不了了...
    我们需要的概率P是：剩下N-K个金币，在M-1个盒子里，存在至少一个盒子有超过K个金币的概率；
    即求非P：M-1个盒子里，每个盒子放有都不超过K个金币的概率；
    =每个盒子都不超过K的金币发生的个数/N-K个金币放到M-1的组合数；
    分母组合数用隔板法可以直接求得,C(M-2,N-K+M-2)；
    分子麻烦一点，实质上是编程题的跳台阶问题：一共N-K阶，每次可以跳1~K阶，一共有多少种跳法。
    但不同于跳台阶，这里的盒子允许放0个金币，且盒子数是固定M-1；
    为了简化问题，先规定每次都要放至少1个，获得各个具体放法，然后求出每个放法放了多少个盒子，用组合数获得这个情况的总放法。
    跳台阶是递推公式：F(n) = F(n-1)+F(n-2)+...+F(n-K) (n>=K)
                   F(n-1) = F(n-2)+F(n-3)+...+F(n-K-1) (n>=K)
                   ...
                   F(1) = 1
                   F(0) = 1
    所以实际上，计算过程是一个K叉树O(n^K)，如果K和n太大的话，计算机会炸...
            
"""

from scipy.special import comb, perm
import random
# 计算跳台阶的每种情况经历的深度depth，保存在lst中
def cal_stage(lst,num_stage,max_step,curr_depth):
    if num_stage==0: #or num_stage==1:
        lst.append(curr_depth+1)
        return 
    if max_step<=num_stage:
        for i in range(max_step):
            cal_stage(lst,num_stage-i-1,max_step,curr_depth+1)
    if max_step>num_stage:
        for i in range(num_stage):
            cal_stage(lst,num_stage-i-1,max_step,curr_depth+1)
    return

# 计算分子
def cal_numerator(lst,num_stage,max_step,curr_depth,box):
    cal_stage(lst,num_stage,max_step,curr_depth)
    res = 0
    for i in range(len(lst)):
        res = res + comb(box,lst[i])
    return res

# 计算分母
def prob(K,M,N): #Calculate the conditional probablility
    lst = []
    remain_coins = N-K
    remain_boxes = M-1
    if remain_coins<=K :
        return 1 # 后面的盒子肯定都少于K金币
    if remain_boxes<=0:
        return 1
    numerator = cal_numerator(lst,remain_coins,K,-1,remain_boxes)
    denominator = comb(remain_coins+remain_boxes-1,remain_boxes-1)
    return numerator/denominator

#生成一个放有随机金币的盒子序列
def random_lst(M,N):
    lst = []
    remain_num = N
    while remain_num>0:
        rand = random.randint(1,remain_num)
        lst.append(rand)
        remain_num = remain_num-rand
    while len(lst)<M:
        lst.append(0)
    random.shuffle(lst)
    return lst

def main_process(M,N):
    lst = random_lst(M,N)
    print("找金币游戏开始！\n")
    print("真实的金币分布（计算机未知）",lst,"\n")
    print("---------------------------\n")
    i = 0
    while i<len(lst):
        K = lst[i]
        print("打开第",i,"个盒子，含有金币",lst[i],"\n")
        pro = prob(K,M,N)
        if pro<0.5:
            
            print("后面的盒子金币都不超过本盒子金币的概率为："+str(pro)+",后面还可能有更多金币！\n")
            i = i+1
            M = M-1
            N = N-K
        else:
            print("后面的盒子金币都不超过本盒子金币的概率为"+str(pro)+",后面不太可能有更多金币，选择放弃！\n")
            print("---------------------------\n")
            return K
    K = lst[i-1]
    print("---------------------------\n")
    print("找完了盒子，只有选择最后一个盒子，有金币数："+str(K)+"\n")
    return K


result = main_process(10,20)
print("最终计算机获得了金币数：",result)