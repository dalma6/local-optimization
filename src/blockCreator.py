from basicBlock import BasicBlock
import libraries.yacc as yacc
import optParser

def fetchInstructions(fileName):
  
    try: 
        with open(fileName, 'r') as f:
            instructions = []
            for line in f:
                instructions.append(line.rstrip('\n').rstrip(' '))
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

def optimizeBlock(block):
    #TODO: ovde treba da se npr proveri sa yacc i to. I da se vidi kako da se optimizuje 
    # mozda prolazak kroz svaku instrukciju parserom moze dati neki info dal imamo neki od slucajeva kad se 
    # vrsi lokalna optimizacija? Tako nesto... :) 
    
    # Vazi, to cu ja napraviti kad pokrenm sve i vidim kako tacno izgleda svaki blok.

    blockInstr = []
    blockInstr = block.getInstructions()

    for i in range(len(blockInstr)):
        tmp = yacc.parse(blockInstr[i])
        if(tmp[0] == "assign"):
            if(len(tmp[3]) == 3 ):           # u pitanju je binarni operator
                [operator, operand1, operand2 ] = tmp[3]
                if(operand1[0] == "const" and operand2[0] == "const"):
                    if operator == "+":
                        res = operand1[1] + operand2[1]
                    elif operator == '-':
                        res = operand1[1] - operand2[1]
                    elif operator == '*':
                        res = operand1[1] * operand2[1]
                    elif operator == '/':
                        res = operand1[1] / operand2[1]
                    blockInstr[i] = tmp[1] + " " + tmp[2] + " " + str(res)
                

    return block


def main():
    fileName = 'test/test_examples/test1.txt'
    instructions = fetchInstructions(fileName)
    blocks = instanceBasicBlocks(instructions)
    for block in blocks:
        print optimizeBlock(block)
    
if __name__ == "__main__":
    main()