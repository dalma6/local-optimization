from basicBlock import BasicBlock

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

    return block


def main():
    fileName = 'test/test1.txt'
    instructions = fetchInstructions(fileName)
    blocks = instanceBasicBlocks(instructions)
    for block in blocks:
        print optimizeBlock(block)
    
if __name__ == "__main__":
    main()