from basicBlock import BasicBlock
from indicators import *

import copy
import math
import sys

import optParser

import libraries.yacc as yacc


def printExpr(expr):
    if(isBinary(expr)):
        return printExpr(expr[1]) + " " + expr[0] + " " + printExpr(expr[2])
    elif(isUnary(expr)):
        return expr[0] + printExpr(expr[1])
    elif(isConst(expr)):
        return str(expr[1])
    elif(isId(expr)):
        return expr[1]


def toCode(instr):
    if(isAssigment(instr)):
        return instr[1] + " := " + printExpr(instr[2])
    if(isIfStmt(instr)):
        if(isinstance(instr[1], bool)):
            if instr[1] == False:
                return ""
            elif instr[1] == True:
                return "GOTO " + str(instr[2])
        else:
            return "IF " + printExpr(instr[1]) + " GOTO " + str(instr[2])


def fetchInstructions(fileName):
    try:
        with open(fileName, 'r') as f:
            instructions = []
            for line in f:
                inst = line.rstrip('\n').rstrip(' ')
                if(inst):
                    instructions.append(inst)
        return instructions
    except IOError as e:
        exit(e)


def getLeaders(instructions):
    leaders = []
    leaders.append(instructions[0])

    for i in range(len(instructions)):
        if(instructions[i].__contains__("GOTO")):
            if((i+1) != len(instructions)):
                leaders.append(instructions[i+1])
            try:
                index = int(instructions[i].split(' ')[-1])
                leaders.append(instructions[index-1])
            except ValueError as e:
                exit(e)

    return list(set(leaders))


def instanceBasicBlocks(instructions):
    leaders = getLeaders(instructions)
    basicBlocks = []

    for instruction in instructions:
        if leaders.__contains__(instruction):
            basicBlocks.append(BasicBlock(instruction))
        basicBlocks[-1].addInstruction(instruction)

    return basicBlocks


def neutralElimination(instr):
    if(isAssigment(instr) and isBinary(instr[2])):
        res = instr[2]
        [operator, left, right] = instr[2]
        if operator == '+':
            if(isValue(left, 0)):
                res = right
            elif (isValue(right, 0)):
                res = left
        elif operator == '-':
            if(isValue(right, 0)):
                res = left
            elif (isValue(left, 0)):
                if(isConst(right)):
                    res = ("const", -right[1])
                elif(isUnary(right)):
                    res = right[1]
                elif(isId(right)):
                    res = ("-", right)
        elif operator == '*':
            if (isValue(left, 0) or isValue(right, 0)):
                res = ('const', 0)
            elif isValue(left, 1):
                res = right
            elif isValue(right, 1):
                res = left
        elif operator == '/':
            if isValue(right, 1):
                res = left
            elif isValue(left, 0):
                res = ('const', 0)
        elif operator == '^':
            if isValue(right, 1):
                res = left
            elif isValue(right, 0):
                res = ('const', 1)
            elif isValue(left, 1):
                res = ('const', 1)
        return (instr[0], instr[1], res)
    return instr


def constantFolding(instr):
    if(isIfStmt(instr) and isBinary(instr[1])):
        [operator, left, right] = instr[1]
        if(isConst(left) and isConst(right)):
            if operator == '>':
                val = left[1] > right[1]
            elif operator == '<':
                val = left[1] < right[1]
            elif operator == '>=':
                val = left[1] >= right[1]
            elif operator == '<=':
                val = left[1] <= right[1]
            elif operator == '==':
                val = left[1] == right[1]
            return (instr[0], val, instr[2])

    if(isAssigment(instr) and isBinary(instr[2])):
        [operator, left, right] = instr[2]
        if(isConst(left) and isConst(right)):
            if operator == "+":
                val = left[1] + right[1]
            elif operator == '-':
                val = left[1] - right[1]
            elif operator == '*':
                val = left[1] * right[1]
            elif operator == '/':
                val = int(left[1] / right[1])
            elif operator == '^':
                val = left[1] ** right[1]
            elif operator == '>>':
                val = left[1] >> right[1]
            elif operator == '<<':
                val = left[1] << right[1]
            return (instr[0], instr[1], ("const", val))

    return instr


def strengthReduction(instr):
    if(isAssigment(instr) and isBinary(instr[2])):
        res = instr[2]
        [operator, left, right] = instr[2]
        if(isValue(right, 2) and operator == "^"):
            return (instr[0], instr[1], ('*', left, left))
        elif(operator == "*"):
            if(isValue(right, 2)):
                return (instr[0], instr[1], ('+', left, left))
            elif(isValue(left, 2)):
                return (instr[0], instr[1], ('+', right, right))
            elif(isConst(right) and isPerfectPower(right[1], 2)):
                res = ('<<', left, ('const', int(math.log(right[1], 2))))
                return (instr[0], instr[1], res)
            elif(isConst(left) and isPerfectPower(left[1], 2)):
                res = ('<<', right, ('const', int(math.log(left[1], 2))))
                return (instr[0], instr[1], res)

            elif(isConst(left) and isPerfectPower(left[1]+1, 2)):
                res1 = ('<<', right, ('const', int(math.log(left[1]+1, 2))))
                res2 = ('-', ('id', "tmp_"+instr[1]), ('id', instr[1]))
                return [(instr[0], "tmp_"+instr[1], res1), (instr[0], instr[1], res2)]

            elif(isConst(right) and isPerfectPower(right[1]+1, 2)):
                res1 = ('<<', left, ('const', int(math.log(right[1]+1, 2))))
                res2 = ('-', ('id', "tmp_"+instr[1]), ('id', instr[1]))
                return [(instr[0], "tmp_"+instr[1], res1), (instr[0], instr[1], res2)]

            elif(isConst(left) and isPerfectPower(left[1]-1, 2)):
                res1 = ('<<', right, ('const', int(math.log(left[1]-1, 2))))
                res2 = ('+', ('id', "tmp_"+instr[1]), ('id', instr[1]))
                return [(instr[0], "tmp_"+instr[1], res1), (instr[0], instr[1], res2)]

            elif(isConst(right) and isPerfectPower(right[1]-1, 2)):
                res1 = ('<<', left, ('const', int(math.log(right[1]-1, 2))))
                res2 = ('+', ('id', "tmp_"+instr[1]), ('id', instr[1]))
                return [(instr[0], "tmp_"+instr[1], res1), (instr[0], instr[1], res2)]

    return instr


def optimizeBlock(block):
    blockInstr = []
    blockInstr = block.getInstructions()
    new_blockInstr = []

    for i in range(len(blockInstr)):
        tmp = yacc.parse(blockInstr[i])

        optimized = strengthReduction(constantFolding(neutralElimination(tmp)))

        if(isinstance(optimized, list) and len(optimized) == 2):
            optCode1 = toCode(optimized[0])
            optCode2 = toCode(optimized[1])
            new_blockInstr.append(optCode1)
            new_blockInstr.append(optCode2)
        else:
            optCode = toCode(optimized)
            if optCode != "":
                new_blockInstr.append(optCode)

    block.setInstructions(new_blockInstr)
    return block


def constantPropagation(block):
    table = {}
    blockInstr = block.getInstructions()
    newBlockInstr = []

    for stmt in blockInstr:
        instr = yacc.parse(stmt)
        optInstr = constantPropInstr(instr, table)
        newBlockInstr.append(toCode(optInstr))

    block.setInstructions(newBlockInstr)
    return block


def constantPropInstr(instr, table):
    if isAssigment(instr) and isConst(instr[2]):
        table[instr[1]] = instr[2][1]

    elif isAssigment(instr):
        if(isBinary(instr[2])):
            [operator, left, right] = instr[2]
            if(isId(left) and left[1] in table.keys()):
                left = ("const", table[left[1]])
            if(isId(right) and right[1] in table.keys()):
                right = ("const", table[right[1]])
            return (instr[0], instr[1], (operator, left, right))
        elif(isId(instr[2]) and instr[2][1] in table.keys()):
            return (instr[0], instr[1], ("const", table[instr[2][1]]))
        elif(isUnary(instr[2])):
            left = instr[2][1]
            if(isId(left) and left[1] in table.keys()):
                return (instr[0],instr[1], ('const',(-1) * table[left[1]]))
    return instr


def main():
    if(len(sys.argv) == 1):
        fileName = 'test/test_examples/test.txt'
    elif(len(sys.argv) == 2):
        fileName = sys.argv[1]
    else:
        print("Usage: python3 blockCreator.py [path_to_file]")
        return

    instructions = fetchInstructions(fileName)
    blocks = instanceBasicBlocks(instructions)

    allIntr = []
    for block in blocks:
        optBlock = optimizeBlock(block)
        optInstructions = optBlock.instructions
        allIntr += optInstructions
    newBlocks = instanceBasicBlocks(allIntr)

    for i in range(len(newBlocks)):
        saveBlock = copy.deepcopy(newBlocks[i])
        while(True):
            otherOptimizations = constantPropagation(
                optimizeBlock(newBlocks[i]))
            if(otherOptimizations.getInstructions() == saveBlock.getInstructions()):
                break
            saveBlock = copy.deepcopy(otherOptimizations)
        print(otherOptimizations, end="")


if __name__ == "__main__":
    main()
