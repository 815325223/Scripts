#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
import time

class AdditionAndSubtraction():
    """加减法
    param:
        ctype:  1(加法) 2(减法) 0(加减混合) default: 1
        count:  算数个数    default: 2
        result: 算数结果的区间  default: [1, 20]
        num:    题目数  default: 100
        col:    每行个数,列数   default: 4
    """
    def __init__(self, ctype=1, count=2, result=[1, 20], num=100, col=4):
        self.ctype = {1:["+"], 2:["-"], 0:["+", "-"]}[ctype]
        self.count = int(count)
        self.min, self.max = [int(x) for x in result]
        self.num = int(num)
        self.col = int(col)
    
    def createFormula(self):
        outFormula = []
        if self.count >= 2:
            params = [random.randint(self.min, self.max) for i in range(self.count)]
            operators = [random.choice(self.ctype) for i in range(self.count-1)] + ["="]
            formula = " ".join(["{} {}".format(*x) for x in list(zip(params, operators))])
            calc = eval(formula.split("=")[0])
            if calc >= self.min and calc <= self.max:
                outFormula = [formula, calc]
        return outFormula
    
    def createNumFormula(self):
        flag = 0
        result = []
        while flag < self.num:
            tmp = self.createFormula()
            if tmp and tmp not in result:
                flag += 1
                result.append(tmp)
        return result
    
    def writexls(self):
        result = self.createNumFormula()
        filename = "加减法_{}_{}.xls".format(time.strftime("%Y%m%d%H%M%S", time.localtime()), self.num)
        with open(filename, "w") as fp:
            flag = 0
            while flag < len(result):
                fp.write("\t".join([x[0] for x in result[flag:flag+self.col]])+"\n")
                flag += self.col


AdditionAndSubtraction().writexls()
