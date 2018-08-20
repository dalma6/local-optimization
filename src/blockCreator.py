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

    for instruction in instructions:
        if leaders.__contains__(instruction):
            print("---------")
            print(instruction)
        else:
            print(instruction)
    print("----------")

# TODO: napraviti sad klasu za bazicni blok umesto da radim ovo.


def main():
    fileName = 'test/test1.txt'
    instructions = fetchInstructions(fileName)
    instanceBasicBlocks(instructions)


if __name__ == "__main__":
    main()