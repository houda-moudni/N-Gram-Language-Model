import numpy as np
import re
import ast
from collections import Counter


def del_cost():
    return 1

def ins_cost():
    return 1

def sub_cost(a, b):
    if a == b :
        return 0
    else:
        return 2
        
def trans_cost(w01, w02, w11, w12):
    if w01 == w12 and w11 == w02:
        return 2
    else :
        return 4 
    

def back_trace(edit_matrix, source, target):
    
    dist_matrix = np.empty((len(source)+1, len(target)+1), dtype=object)
    
    dist_matrix[0,:] = 'D'
    dist_matrix[:,0] = 'L'
    dist_matrix[0,0] = '0'
    
    for i in range(1, len(source) + 1):
        for j in range(1, len(target) + 1):
            
            dele = edit_matrix[i-1, j] + del_cost()
            ins = edit_matrix[i, j-1] + ins_cost()
            sub = edit_matrix[i-1, j-1] + sub_cost(source[i-1], target[j-1])
            trans= (edit_matrix[i-2, j-2] + trans_cost(source[i-1], target[j-1], source[i-2], target[j-2])) if (i!=1 and j!=1) else None
            min_cost = min(dele, ins, sub) if trans is None else min(dele, ins, sub, trans)

            edit_ops = ""
            if min_cost == dele:
                edit_ops += 'D'
            if min_cost == ins:
                edit_ops += 'L'
            if min_cost == sub:
                edit_ops += 'G'
            if min_cost == trans:
                edit_ops += 'T'

            dist_matrix[i, j] = edit_ops
        
    return dist_matrix
                

def min_edit_distance(source, target, do_print_chart=False, do_back_trace=False):

    edit_matrix = np.zeros((len(source)+1, len(target)+1))
    edit_matrix[:, 0] = [i for i in range(len(source) + 1)]
    edit_matrix[0,:] = [j for j in range(len(target) + 1)]
    
    for i in range(1, len(source)+1):
        for j in range(1, len(target)+1):
            if i==1 or j==1:
                edit_matrix[i,j] = min(edit_matrix[i-1,j] + del_cost(), 
                                edit_matrix[i,j-1] + ins_cost() , 
                                edit_matrix[i-1,j-1] + sub_cost(source[i-1], target[j-1]))
            else:
                edit_matrix[i,j] = min(edit_matrix[i-1,j] + del_cost(), 
                                edit_matrix[i,j-1] + ins_cost() , 
                                edit_matrix[i-1,j-1] + sub_cost(source[i-1], target[j-1]),
                                edit_matrix[i-2,j-2] + trans_cost(source[i-1],target[j-1], source[i-2], target[j-2])
                                )


    if(do_print_chart):
        print(edit_matrix)
        
    if(do_back_trace):
        print(back_trace(edit_matrix,source,target))

    return edit_matrix[-1,-1]


    
class Auto_Corrector():

    def __init__(self, WORDS) -> None:
        self.WORDS = WORDS

    def candidates(self,word): 
        
        set_of_words= set(self.WORDS)
        words_with_med = [(w,min_edit_distance(w, word)) for w in set_of_words]
        words_with_med = sorted(words_with_med, key=lambda x: x[1])

        return words_with_med

    def candidates_correction(self,word , k=1):
        if(len(self.candidates(word)) > k):
            return self.candidates(word)[0:k]
        else :
            return self.candidates(word)
    
