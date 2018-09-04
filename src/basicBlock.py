class BasicBlock:
    def __init__(self, lead):
       self.lead = lead
       self.instructions = []

    def addInstruction(self,instruction):
        self.instructions.append(instruction)
    
    def getInstructions(self):
        return self.instructions
    
    def getLead(self):
        return self.lead

    def __str__(self):
        str = "-----------\n"
        for instr in self.instructions:
            if(instr != ""):
                str += instr + "\n"
        str += "-----------"
        return str

