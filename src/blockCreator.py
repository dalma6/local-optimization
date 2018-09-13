import math
from basicBlock import BasicBlock
import libraries.yacc as yacc
from indicators import *
import optParser


def printExpr(expr):
    if(isBinary(expr)):
        return printExpr(expr[1]) + " " + expr[0] + " " + printExpr(expr[2])
    if(isUnary(expr)):
        return expr[0] + printExpr(expr[1])
    if(isConst):
        return str(expr[1])
    if(isId):
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
                val = left[1] / right[1]
            elif operator == '^':
                val = left[1] ** right[1]
            return (instr[0], instr[1], ("const", val))

    return instr


'''
def strengthReduction(tmp):
    [operator, left, right] = tmp[3]
    res = tmp[3]
    if right[0] == 'const':
        if operator == '^' and right[1] == 2:
            operator = '*'
            right[1] = left[1]
            res = left[1] * left[1]
        elif operator == '*' and isPerfectPower(right[1], 2):
            operator = '<<'
            right[1] = math.log(right[1], 2)
        elif operator == '*' and isPerfectPower(right[1], 3):
            operator = '<<'
            right[1] = math.log(right[1], 3)
        tmp[0] = operator
        tmp[1] = left[1]
        tmp[2] = right[1]
        return (tmp[0], tmp[1], tmp[2])
'''


def optimizeBlock(block):
    blockInstr = []
    blockInstr = block.getInstructions()

    for i in range(len(blockInstr)):
        tmp = yacc.parse(blockInstr[i])
        optimized = constantFolding(neutralElimination(tmp))
        optCode = toCode(optimized)
        blockInstr[i] = optCode
    return block


def main():
    fileName = 'test/test_examples/testNeutralElimination.txt'
    instructions = fetchInstructions(fileName)
    blocks = instanceBasicBlocks(instructions)
    for block in blocks:
        print(optimizeBlock(block))


if __name__ == "__main__":
    main()
