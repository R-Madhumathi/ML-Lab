# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:59:10 2019

@author: MADHUMATHI
"""

def probAttr(data,attr,val):
    Total=data.shape[0]    #Get column length
    cnt = len(data[data[attr] == val]) #Count of Attribute [attr] equal to val
    return cnt,cnt/Total

def train(data,Attr,conceptVals,concept): 
    conceptProbs = {} #P(A)
    countConcept={}
    for cVal in conceptVals: #Get probablity and count of Yes and No
        countConcept[cVal],conceptProbs[cVal] = probAttr(data,concept,cVal)
    
    AttrConcept = {} #P(X/A)
    probability_list = {} #P(X)
    for att in Attr: #Create a tree for attribute
        probability_list[att] = {}
        AttrConcept[att] = {}
        for val in Attr[att]: #Create Tree for Attribute value
            AttrConcept[att][val] = {}
            a,probability_list[att][val] = probAttr(data,att,val) #Get Probablity for att equal to val
            for cVal in conceptVals: #Create Tree to hold yes and no values
                dataTemp = data[data[att]==val] #Calculate att equal to val and concept equal to cVal
                AttrConcept[att][val][cVal] = len(dataTemp[dataTemp[concept] == cVal])/countConcept[cVal]
            
    print("P(A) : ",conceptProbs,"\n")
    print("P(X/A) : ",AttrConcept,"\n")
    print("P(X) : ",probability_list,"\n")
    return conceptProbs,AttrConcept,probability_list

def test(examples,Attr,concept_list,conceptProbs,AttrConcept,probability_list):
    misclassification_count=0
    Total = len(examples)    #Get Number of testing set
    for ex in examples:
        px={}  #Dict to hold final value
        for a in Attr:    #Iterrate thorugh the Tree with Attributes (Refer problem to find the tree)
            for x in ex:  #Iterrate thorugh the Tree for given example
                for c in concept_list:   #Iterrate thorugh the Tree using concepts
                    if x in AttrConcept[a]:  #Check if the value of x refering in same sub-tree of P(X/A)
                        if c not in px: #If c not in px multiply P(A) with 1st Itteration (for 1st value of x)
                            px[c] = conceptProbs[c]*AttrConcept[a][x][c]/probability_list[a][x]
                        else:  #multiply px in next Itterations (for next values of x)
                            px[c] = px[c]*AttrConcept[a][x][c]/probability_list[a][x]
        print(px)
        classification = max(px,key=px.get)  #Key of Maximum of px is required Classification
        print("Classification :",classification,"Expected :",ex[-1],"\n")
        if(classification!=ex[-1]):
            misclassification_count+=1
    misclassification_rate=misclassification_count*100/Total
    accuracy=100-misclassification_rate
    print("\n\nMisclassification Count={}".format(misclassification_count))
    print("\n\nMisclassification Rate={}%".format(misclassification_rate))
    print("\n\nAccuracy={}%".format(accuracy))
    print("\n\n")
    
    
def main():
    import pandas as pd
    from pandas import DataFrame 
    data = DataFrame.from_csv('tennis.csv')
    #print(data)
    concept=str(list(data)[-1])
    concept_list = set(data[concept])
    Attr={}
    for a in list(data)[:-1]:    #Get attribute values
        Attr[a] = set(data[a])
    conceptProbs,AttrConcept,probability_list = train(data,Attr,concept_list,concept)

    examples = DataFrame.from_csv('tennis.csv')
    #print(examples)
    test(examples.values,Attr,concept_list,conceptProbs,AttrConcept,probability_list)

main()    