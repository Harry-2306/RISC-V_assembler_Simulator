import sys

input_path = sys.argv[1]
output_path = sys.argv[2]

Memory = {
    0x00010000: 0, 0x00010004: 0, 0x00010008: 0, 0x0001000C: 0,
    0x00010010: 0, 0x00010014: 0, 0x00010018: 0, 0x0001001C: 0,
    0x00010020: 0, 0x00010024: 0, 0x00010028: 0, 0x0001002C: 0,
    0x00010030: 0, 0x00010034: 0, 0x00010038: 0, 0x0001003C: 0,
    0x00010040: 0, 0x00010044: 0, 0x00010048: 0, 0x0001004C: 0,
    0x00010050: 0, 0x00010054: 0, 0x00010058: 0, 0x0001005C: 0,
    0x00010060: 0, 0x00010064: 0, 0x00010068: 0, 0x0001006C: 0,
    0x00010070: 0, 0x00010074: 0, 0x00010078: 0, 0x0001007C: 0
}

Register = { 
    "x0": "00000", "zero": "00000", "r0": "00000",
    "x1": "00001", "ra": "00001", "r1": "00001",
    "x2": "00010", "sp": "00010", "r2": "00010",
    "x3": "00011", "gp": "00011", "r3": "00011",
    "x4": "00100", "tp": "00100", "r4": "00100",
    "x5": "00101", "t0": "00101", "r5": "00101",
    "x6": "00110", "t1": "00110", "r6": "00110",
    "x7": "00111", "t2": "00111", "r7": "00111",
    "x8": "01000", "s0": "01000", "fp": "01000", "r8": "01000",
    "x9": "01001", "s1": "01001", "r9": "01001",
    "x10": "01010", "a0": "01010", "r10": "01010",
    "x11": "01011", "a1": "01011", "r11": "01011",
    "x12": "01100", "a2": "01100", "r12": "01100",
    "x13": "01101", "a3": "01101", "r13": "01101",
    "x14": "01110", "a4": "01110", "r14": "01110",
    "x15": "01111", "a5": "01111", "r15": "01111",
    "x16": "10000", "a6": "10000", "r16": "10000",
    "x17": "10001", "a7": "10001", "r17": "10001",
    "x18": "10010", "s2": "10010", "r18": "10010",
    "x19": "10011", "s3": "10011", "r19": "10011",
    "x20": "10100", "s4": "10100", "r20": "10100",
    "x21": "10101", "s5": "10101", "r21": "10101",
    "x22": "10110", "s6": "10110", "r22": "10110",
    "x23": "10111", "s7": "10111", "r23": "10111",
    "x24": "11000", "s8": "11000", "r24": "11000",
    "x25": "11001", "s9": "11001", "r25": "11001",
    "x26": "11010", "s10": "11010", "r26": "11010",
    "x27": "11011", "s11": "11011", "r27": "11011",
    "x28": "11100", "t3": "11100", "r28": "11100",
    "x29": "11101", "t4": "11101", "r29": "11101",
    "x30": "11110", "t5": "11110", "r30": "11110",
    "x31": "11111", "t6": "11111", "r31": "11111"
}

RegisterValues = {
    "x0": 0, "x1": 0, "x2": 380, "x3": 0,
    "x4": 0, "x5": 0, "x6": 0, "x7": 0,
    "x8": 0, "x9": 0, "x10": 0, "x11": 0,
    "x12": 0, "x13": 0, "x14": 0, "x15": 0,
    "x16": 0, "x17": 0, "x18": 0, "x19": 0,
    "x20": 0, "x21": 0, "x22": 0, "x23": 0,
    "x24": 0, "x25": 0, "x26": 0, "x27": 0,
    "x28": 0, "x29": 0, "x30": 0, "x31": 0
}


RTypeInstructions = { 
    "add":  {"funct7": "0000000", "funct3": "000", "opcode": "0110011"},
    "sub":  {"funct7": "0100000", "funct3": "000", "opcode": "0110011"},
    "slt":  {"funct7": "0000000", "funct3": "010", "opcode": "0110011"},
    "srl":  {"funct7": "0000000", "funct3": "101", "opcode": "0110011"},
    "or":   {"funct7": "0000000", "funct3": "110", "opcode": "0110011"},
    "and":  {"funct7": "0000000", "funct3": "111", "opcode": "0110011"}
}

ITypeInstructions = {
    "lw": {"funct3": "010", "opcode": "0000011"},
    "addi": {"funct3": "000", "opcode": "0010011"},
    "jalr": {"funct3": "000", "opcode": "1100111"}
}

STypeInstructions = {
    "sw": {"funct3": "010", "opcode": "0100011"}
}

JTypeInstructions = {
    "jal": {"opcode": "1101111"}
}

BTypeInstructions = {
    "beq": {"funct3": "000", "opcode": "1100011"},
    "bne": {"funct3": "001", "opcode": "1100011"}
}

PC = 0  
def Test(Opcode, funct3):



def Binary(BinaryString):



def UnSigned(value):



def Process(element, Instruction, PC):
    global RegisterValues, Memory

    if Instruction == "RTypeInstructions":
        OperationUsed = ""
        funct7 = element[0:7]
        Rs2Value = element[7:12]
        Rs1Value = element[12:17]
        funct3 = element[17:20]
        RdValue = element[20:25]
        
        Rs1Register = Binary(Rs1Value)
        Rs2Register = Binary(Rs2Value)
        RdRegister = Binary(RdValue)
        
        Rs1StoredValue = RegisterValues[Rs1Register]
        Rs2StoredValue = RegisterValues[Rs2Register]
        
        for key, Values in RTypeInstructions.items():
            if Values["funct7"] == funct7 and Values["funct3"] == funct3: 
                OperationUsed = key 
                break
        
        if OperationUsed == "add":
            RdStoredValue = UnSigned(Rs1StoredValue+Rs2StoredValue)
        elif OperationUsed == "sub":
            RdStoredValue = UnSigned(Rs1StoredValue-Rs2StoredValue)
        elif OperationUsed == "slt":
            if Rs1StoredValue < Rs2StoredValue: 
                RdStoredValue =1
            else: 
                RdStoredValue = 0
        elif OperationUsed == "srl":
            RdStoredValue = UnSigned(Rs1StoredValue//(2**Rs2StoredValue))
        elif OperationUsed == "or":
            RdStoredValue = UnSigned(Rs1StoredValue|Rs2StoredValue)
        elif OperationUsed == "and":
            RdStoredValue = UnSigned(Rs1StoredValue &Rs2StoredValue)
        else:
            return PC + 4
        
        if RdRegister != "x0":
            RegisterValues[RdRegister]= RdStoredValue
        return PC+4
    
    elif Instruction == "ITypeInstructions":
        OperationUsed = ""
        ImmRaw = element[0:12]
        if ImmRaw[0] =='0': 
            ImmValue =int(ImmRaw,2)
        else: 
            ImmRaw = ImmRaw.replace("0", "-")
            ImmRaw = ImmRaw.replace("1", "0")
            ImmRaw = ImmRaw.replace("-", "1")
            ImmValue = -(int(ImmRaw,2) + 1)
        Rs1Value = element[12:17]
        funct3 = element[17:20]
        RdValue = element[20:25]
        opcode = element[-7:] 
    
        for key, Values in ITypeInstructions.items():
            if Values["funct3"] == funct3 and Values["opcode"] == opcode:
                OperationUsed = key
                break
    
        Rs1Register = Binary(Rs1Value)
        Rs1StoredValue = RegisterValues[Rs1Register]
    
        if OperationUsed == "addi":
            RdStoredValue = UnSigned(Rs1StoredValue + ImmValue)
        elif OperationUsed == "lw":
            MemoryAddress = UnSigned(Rs1StoredValue + ImmValue)
            if MemoryAddress in Memory:
                RdStoredValue = Memory[MemoryAddress] 
            else:
                RdStoredValue = 0  
        elif OperationUsed == "jalr":
            RdStoredValue = UnSigned(PC + 4)
            target = UnSigned(  Rs1StoredValue + ImmValue)
            RdRegister = Binary(RdValue)
            if RdRegister != "x0":
                RegisterValues[RdRegister] = RdStoredValue
            return target  
    
        RdRegister = Binary(RdValue)
        if RdRegister != "x0":
            RegisterValues[RdRegister] = RdStoredValue
        return PC + 4




def Error(Message):


OriginalInstructionsList = []
with open(input_path, "r") as file:
    for line in file:
        OriginalInstructionsList.append(line.strip())  


