import sys
import re
 
input_path = sys.argv[1]
output_path = sys.argv[2]
#First defining all the registers with their ABI names and Alterate Name
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
    "beq":"000","bne":"001","opcode":"1100011"
    }

def Error(Message): 
    with open("output.txt", "w") as f:  
        f.write(Message)  
    sys.exit() 

def twcoex20(n):
    if n >= 0:
        return format(n, '021b')
    else:
        return format((2**21) + n, '021b')

def get_instructions(filename):
    instructions = []
    with open(filename, "r") as f:
        for line in f:
            # Strip whitespace and skip blank lines or comments
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Skip a specific line if needed (like "addi x0, x0, 0")
            if line == "addi x0, x0, 0":
                continue

            # Insert a space after commas so that registers and immediates are tokenized separately
            line = line.replace(",", ", ")
            tokens = line.split()

            # Append tokens if the line is not empty
            if tokens:
                instructions.append(tokens)
    return instructions

l1 = get_instructions(input_path)
Final = []
BType = []
BTypePos  = []
def ConvertInstruction(InstructionType,List): 
    if InstructionType == "RTypeInstructions": 
        MainLines = ""
        InstructionDict = RTypeInstructions
    
        FirstCommand = List[0] 

        if FirstCommand in InstructionDict:
            if len(List) == 4:
                Destination = List[1]
                SourceRegister1 = List[2] 
                SourceRegister2 = List[3]


                if not Destination.endswith(',') or not SourceRegister1.endswith(','):  
                    Error(f"Syntax error: Missing ',' in '{FirstCommand}")  

                Destination = Destination.strip(',')  
                SourceRegister1 = SourceRegister1.strip(',')  

                if Destination not in Register or SourceRegister1 not in Register or SourceRegister2 not in Register:  
                    Error(f"Invalid register usage in '{FirstCommand}")

                try:  
                    MainLines = MainLines + InstructionDict[FirstCommand]['funct7'] 
                    MainLines = MainLines + Register[SourceRegister2] 
                    MainLines = MainLines + Register[SourceRegister1] 
                    MainLines = MainLines + InstructionDict[FirstCommand]['funct3'] 
                    MainLines = MainLines + Register[Destination] 
                    MainLines = MainLines + InstructionDict[FirstCommand]['opcode'] + '\n'
                    Final.append(MainLines)
                
                except KeyError: 
                    Error(f"Error in Processing")
    
    elif InstructionType == "ITypeInstructions": 
        MainLines = ""
        InstructionDict = ITypeInstructions

        FirstCommand = List[0] 

        if FirstCommand in InstructionDict:

            #for instructions having format: jalr ra, a5, -07
            if len(List) == 4:
                InputType = "Normal" #this variable keeps track of the input format, for error handling
                ReturnAddressRegister = List[1]
                SourceRegister1 = List[2] 
                Immediate = List[3]

            #for instructions having format: jalr ra, -07(a5)
            elif len(List) == 3 and "(" in List[2] and ")" in List[2]:
                InputType = "Parenthesis"

                #removing parenthesis and splitting to get the values
                List[2] = List[2].replace("(", " ")
                List[2] = List[2].replace(")", " ")
                List = List[:2] + List[2].split()
                
                ReturnAddressRegister = List[1]
                Immediate = List[2]
                SourceRegister1 = List[3]

            if (int(Immediate) < -2048) or (int(Immediate) > 2047):
                Error(f"Immediate value out of range in '{FirstCommand}'")

            if not ReturnAddressRegister.endswith(',') or (not SourceRegister1.endswith(',') and InputType == "Normal"):  
                Error(f"Syntax error: Missing ',' in '{FirstCommand}")  

            ReturnAddressRegister = ReturnAddressRegister.strip(',')   
            SourceRegister1 = SourceRegister1.strip(',')
            
            if ReturnAddressRegister not in Register or SourceRegister1 not in Register:  
                Error(f"Invalid register usage in '{FirstCommand}")

            try:  
                MainLines = MainLines + format(int(Immediate) & 0xFFF, '012b')  #format() converts the immediate to 12 bit 2's compliment
                MainLines = MainLines + Register[SourceRegister1] 
                MainLines = MainLines + InstructionDict[FirstCommand]['funct3'] 
                MainLines = MainLines + Register[ReturnAddressRegister] 
                MainLines = MainLines + InstructionDict[FirstCommand]['opcode'] + '\n'
                Final.append(MainLines)
            
            except KeyError: 
                Error(f"Error in Processing")
    
    elif InstructionType == "STypeInstructions": 
        MainLines = ""
        InstructionDict = STypeInstructions
        
        FirstCommand = List[0] 

        if FirstCommand in InstructionDict:
            if len(List) == 3 and "(" in List[2] and ")" in List[2]: #same format as in ITypeInstructions
                List[2] = List[2].replace("(", " ")
                List[2] = List[2].replace(")", " ")
                List = List[:2] + List[2].split()
                
                DataRegister = List[1]
                Immediate = List[2]
                SourceRegister1 = List[3]

                if (int(Immediate) < -2048) or (int(Immediate) > 2047):
                    Error(f"Immediate value out of range in '{FirstCommand}'")

                if not DataRegister.endswith(','):  
                    Error(f"Syntax error: Missing ',' in '{FirstCommand}")  

                DataRegister = DataRegister.strip(',')    

                if DataRegister not in Register or SourceRegister1 not in Register:  
                    Error(f"Invalid register usage in '{FirstCommand}")

                Immediate = format(int(Immediate) & 0xFFF, '012b')

                try:  
                    MainLines = MainLines + Immediate[:7]
                    MainLines = MainLines + Register[DataRegister] 
                    MainLines = MainLines + Register[SourceRegister1] 
                    MainLines = MainLines + InstructionDict[FirstCommand]['funct3'] 
                    MainLines = MainLines + Immediate[7:]        
                    MainLines = MainLines + InstructionDict[FirstCommand]['opcode'] + '\n'
                    Final.append(MainLines)
                
                except KeyError: 
                    Error(f"Error in Processing")
    
    elif InstructionType == "JTypeInstructions":
        global l1  # Ensure l1 is available globally

        MainLines = ""
        # Verify exactly three tokens: mnemonic, rd, immediate/label
        if len(List) != 3:
            raise ValueError(f"Invalid syntax for J-type instruction: {' '.join(List)}")
        
        mnemonic = List[0]
        rd = List[1]
        imm_str = List[2]
        
        # Check that the destination register ends with a comma
        if not rd.endswith(','):
            Error(f"Syntax error: Missing ',' after destination register in '{mnemonic}'")
        rd = rd.strip(',')
        
        if rd not in Register:
            Error(f"Invalid register usage in '{mnemonic}'")
        
        # Determine the offset: if imm_str is numeric, convert; otherwise, resolve as label
        try:
            offset = int(imm_str)
        except ValueError:
            found = False
            for instr in l1:
                # Look for a label; assumes labels are given as "label:" in the first token
                if instr[0].endswith(':'):
                    label = instr[0].split(':')[0]
                    if label == imm_str:
                        # Calculate the offset (in bytes) using a 4-byte instruction width
                        offset = (l1.index(instr) - l1.index(List)) * 4
                        found = True
                        break
            if not found:
                Error(f"Label '{imm_str}' not found in instruction list.")
        
        # Convert the offset into a 21-bit two's-complement binary string.
        # Make sure you have a helper function twcoex20 defined.
        imm21 = twcoex20(offset)  # e.g., "0xxxxxxxxxxxxxxxxxxxxx"
        
        # Reassemble the immediate bits per RISC‑V JAL encoding:
        #   - Bit 20 (sign)      : imm21[0]
        #   - Bits 10:1          : imm21[10:20]
        #   - Bit 11             : imm21[9]
        #   - Bits 19:12         : imm21[1:9]
        imm_bit20 = imm21[0]
        imm_10_1  = imm21[10:20]
        imm_bit11 = imm21[9]
        imm_19_12 = imm21[1:9]
        imm_encoded = imm_bit20 + imm_10_1 + imm_bit11 + imm_19_12
        
        # Form the final binary instruction:
        # [immediate (20 bits)] + [rd (5 bits)] + [opcode (7 bits)]
        MainLines = imm_encoded + Register[rd] + JTypeInstructions[mnemonic]["opcode"] + "\n"
        Final.append(MainLines)

        
    else:
        raise ValueError(f"Unknown instruction: {List[0]}")
        

#Add All the instructions here 
MainInstructions = {
    "RTypeInstructions": ["add", "sub", "slt", "srl", "or", "and"],
    "ITypeInstructions": ["lw", "addi", "jalr"],
    "STypeInstructions": ["sw"],
    "BTypeInstructions" : ["beq","bne","opcode"],
    "JTypeInstructions" : ["jal"]
}


#Reading from the file
NumberOfLines = 0
bool = False
Absolute = False
with open(input_path) as file: 
    for line in file: 
        if line == "\n" or line == "addi x0, x0, 0": 
            continue
        elif bool == True and len(line) != 0:
            Error()
        elif bool == True and len(line) == 0:
            break
        else: 
            NumberOfLines = NumberOfLines + 1
            Current = line.strip() #"add rd, rs1,rs2"
            Current = Current.replace(",", ", ") #"add rd, rs1, rs2"
            List = Current.split() #['add', 'rd,', 'rs1,', 'rs2']
            FirstCommand = List[0] #"add


            if(List[0].endswith(':')): 
                List.pop(0)
            FirstCommand = List[0]
            InstructionType = None
            for Key, Values in MainInstructions.items():
                if FirstCommand in Values:
                    InstructionType = Key
                    break  

            if FirstCommand == "beq" or FirstCommand == "bne" or FirstCommand == "opcode": 
                continue
            elif InstructionType != BTypeInstructions and InstructionType != None:
                ConvertInstruction(InstructionType, List)
                #Check for label and then copy paste the same code after storing the label in a list
            else: 
                Error("There is error in test case")



def removespaces(s): #removes the spaces for all the instructions
    s1=""
    for i in s:
        if i!=" ":
            s1+=i
    return s1

def decimal(n):          #converts binary to decimal(only used in the two's complement function)
    temp=n
    n1=0
    for i in range(len(str(n))):
        n1+=((temp%10)*(2**i))
        temp=temp//10
    return n1

def binconverter(n):  #standard algorithm to convert base 10 to binary
    bin=""
    while n!=0:
        bin+=str(n%2)
        n=n//2
    return bin[::-1]

def twcoex12(n):
    if n>0:
        a=binconverter(n)
        return ("0"*(12-len(a)))+a
    elif n<0:
        a=binconverter(abs(n))
        a=("0"*(12-len(a)))+a
        b=""
        for i in a:
            if i=="0":
                b+="1"
            else:
                b+="0"
        c=binconverter(decimal(int(b))+1)
        return ((c[0]*(12-len(c)))+c)
    else:
        return '0'*12

def reverse(s):     #this is to reverse the notation and all that stuff
    return s[::-1]

btinstructions={"beq":"000","bne":"001","opcode":"1100011"} #stored opcode separately because its the same for every b-instruction

register = { 
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






## error case 10: wrong instruction name
##error case 13: more than one b-type command in an instruction

def lab_exi(l1):            ## Handles error case1: wrong label name can be used when calling b type instructions
    lt=[]
    le=[]
    ld=[]
    for i in l1:
        if ':' in i[0]:
            ld.append(i[0].split(':')[0])
        if 'beq' in i[0] or 'bne' in i[0]:
            if i[2].isalnum() and len(i[2])>1:
                le.append(i[2])
    for j in le:
        if j in ld:
            lt.append("PASS")
        else:
            lt.append("Syntax error: label name used in instruction does not exist")    
    return lt        
def label_synt(l1):          #handles error case 2(checks if the labels follow the proper nomenclature or not)
    lt=[]
    for i in range(len(l1)):
        if ":" in l1[i][0]:
            l2=l1[i][0].split(":")[0]
            if l1[i][0][l1[i][0].index(":")-1] in "        ": #
                lt.append("Syntax error:no spaces between label and column")
            else:
                lt.append("PASS")
            if l2[0] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                lt.append("syntax error:label name should start with a character")
            else:
                lt.append("PASS")
    return lt

def lab_uni(l1):            ## error case 3: using the same label to mark different lines
    lt=[]
    lf=[]
    
    for i in l1:
        if ':' in i[0]:
            lf.append(i[0].split(':')[0])
    for j in lf:
        if lf.count(j)>1:
            lt.append('Syntax Error: Same label used to denote to mark two different instructions')
        else:
            lt.append('PASS')
    
    return lt

def op_mi(l1):                  ## error case 4: missing operand
    lt=[]
    lf=[]
    for i in l1:
        if 'beq' in i[0] or 'bne' in i[0]:
            lf.append(i)
    for j in lf:
        if len(j)<3:
            lt.append('incomplete instruction')
        elif j[1]=='' or j[2]=='':
            lt.append('Syntax error:Missing operand')
        else:
            lt.append("PASS")
    return lt


def ex_op(l1):                  ## error case 5: extra operand(s)

    li=[]
    lt=[]
    for i in l1:
        if 'beq' in i[0] or 'bne' in i[0]:
            li.append(i)
    for j in li:
        if len(j)>3:
            lt.append('Syntax error: Operands entered more than the number of operands allowed ')   
        else:
            lt.append("PASS")
    return lt


def op_ex(l1):              ## error case 7: wrong operand name
    lt=[]
    lf=[]
    for i in l1:
        if 'beq' in i[0] or 'bne' in i[0]:
            lf.append(i)
    for j in lf:
        if ':' in j[0]:
            l2=j[0].split(':')
            if (l2[1][3:] in register.keys()) and (j[1] in register.keys()):
                lt.append("PASS")
            else:
                lt.append("Syntax error: Undefined operand entered")
        else:
            if (j[0][3:]) in register.keys() and (j[1] in register.keys()):
                lt.append("PASS")
            else:
                lt.append("Syntax error: Undefined operand entered")
    return lt



def comm(l1):               #checks if the instruction has too many commas or is it okay (will use the other list)
    lt=[]

    for i in l1:
        if 'beq' in i or 'bne' in i:
            if i.count(',')==2:
                lt.append('PASS')
            else:
                lt.append('Syntax error: Missing expression(,)')
    return lt



def ovsho(l1):              ## error case 11: overshooting the program bounds by wrong immediate value
    d1={}
    lt=[]
    for i in range(len(l1)):
        if 'beq' in l1[i][0] or 'bne' in l1[i][0]:
            if not (l1[i][2].isalnum() and len(l1[i][2])>1):
                
                d1[i+1]=int(l1[i][2])
    for i in d1:
        if d1[i]>=0:
            if i+(d1[i]/4)<=len(l1):
                lt.append('PASS')
            else:
                lt.append("Syntax error: Program counter out of range")
        else:
            if (i)-(d1[i]/4)>=1:
                lt.append("PASS")
            else:
                lt.append("Syntax error: Program counter out of range")
    return lt


BTypePos = []
MainLines = []
with open(input_path,"r") as f:
    l1=f.readlines()
    l2=[] #
    l3=[]
    for i in range(len(l1)):             #this loop removes "\n" from all the lines
        s1=removespaces(l1[i])
        l3.append(l1[i][:len(s1)])
        l2.append(l1[i][:len(s1)-1].split(','))
        l1[i]=s1[:len(s1)].split(",")


    i = -1
    lf=list(set(lab_exi(l1) +label_synt(l2)+lab_uni(l1)+op_mi(l1)+ex_op(l1)+op_ex(l1)+comm(l3)+ovsho(l1)))               #this stores the list of instructions converted to binary
    lff=[]
    if lf==['PASS'] or lf == []:
        for j in l1:
            i = i + 1
            if "beq" in j[0] or "bne" in j[0]:
                BTypePos.append(i)
                bf=""       #stores the b-type instruction in binary
                main_inst="beq" if "beq" in j[0] else "bne"
                funct3=btinstructions[main_inst]          #stores binary equivalent of funct 3 for the instruction
                opcode=btinstructions["opcode"]           #self explanatory
                imm4=""
                if ":" in j[0]:
                    l5=j[0].split(":")
                    rs1=register[l5[1][3:]]
                else:
                    rs1=register[j[0][3:]]                    #stores the 5 bit value in the register                      
                rs2=register[j[1]] 
                if j[2].isalnum() and len(j[2])>1:
                    for k in l1:                          #-1 checks the magnitude and accomodates for negative numbers
                        if j[2] in k[0]:            
                            if l1.index(k)-l1.index(j)>0:
                                imm4=((twcoex12((l1.index(k)-l1.index(j))*4)))
                            else:
                                imm4=((twcoex12((l1.index(k)-l1.index(j)+1)*4)))
                            break
                else:
                    imm4=((twcoex12(int(j[2]))))

                
                bf=imm4[-12]+imm4[-10:-4:1]+rs2+rs1+funct3+"" + (imm4[-4]+imm4[-3]+imm4[-2]+imm4[-1]+"" +imm4[-11])+"" +opcode+'\n'
                lff.append(bf)
        MainList = lff
    else:
        print("error detected")
        for k in lf:
            if k!='PASS':
                print(k)


#writing to output file
if "00000000000000000000000001100011\n" not in MainList: 
 Error("Missing Virtual Halt") 
k = 0
j = 0
FinalString = ""
for i in range(len(Final) + len(MainList)): 
    if i in BTypePos: 
        FinalString = FinalString + MainList[j]
        j = j + 1
    else: 
        FinalString = FinalString + Final[k]
        k = k + 1

with open(output_path,'w') as file: 
    file.write(FinalString)
