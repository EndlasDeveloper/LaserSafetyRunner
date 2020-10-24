import sys
import array as arr


########################################################################
# Class: Registers
# Description: Class to store the state of the registers in the t34
# emulator. Exclusively used in the Monitor class.
########################################################################
class Registers:
    # Masks for setting flags in SR
    Negative = 128
    Overflow = 64     # Ignored so its none for now
    Break = 16
    Decimal = 8
    Interrupt = 4
    Zero = 2
    Carry = 1

    def __init__(self, monitor):
        # Program counter (16 bit)
        self.PC = 0
        # Accumulator (8 bit)
        self.AC = 0
        # X register (8 bit)
        self.X = 0
        # Y register (8 bit)
        self.Y = 0
        # status register (8-bit)
        self.SR = 0b00100000        # initialize to all zeros except for the unused bit
        # stack pointer (8-bit)
        self.SP = 0
        # get stack for the system
        self.m = monitor

        self.v = 255

    ########################################################################
    # Name: exe_instruction
    # Description: accepts an instruction string and an optional operand.
    # Then performs the correct manipulation on the registers based on the
    # input.
    ########################################################################
    def exe_instruction(self, inst, operand=0):

        if inst == 'ADC':   # NZCV
            self.AC += self.m.stack[self.SP]
            if self.AC > 255:
                self.SR = self.SR | self.Carry
                self.AC = self.AC & self.v

        # push PC+2, push SR
        elif inst == 'BRK':             # IB
            self.SP -= 1
            self.m.stack[self.SP] = self.PC + 2  # push PC + 2
            self.SP -= 1
            self.m.stack[self.SP] = self.SR      # push status reg onto stack
            self.SP -= 1
            self.SR = self.SR | 20      # set B (break) and I (Interrupt) flags

        elif inst == 'CLD':        # D - set decimal flag to 0
            self.SR = self.SR & 247

        elif inst == 'CLI':     # I - set interrupt flag to 0
            self.SR = self.SR & 251

        elif inst == 'CLV':     # V - set overflow flag to 0
            self.SR = self.SR & 191

        elif inst == 'DEX':     # NZ
            if self.X < 128:    # y is positive
                if self.X - 1 < 0:  # number is go negative upon decrement
                    self.X = 0xff
                    self.SR = self.SR | self.Negative   # set N flag
                else:
                    self.X -= 1

        elif inst == 'DEY':     # NZ
            if self.Y == 0:  # number is go negative upon decrement
                self.Y = 0xff
                self.SR = self.SR | self.Negative   # set N flag
            else:
                self.Y -= 1

        elif inst == 'LDX':     # NZ
            self.X = operand
            if self.X < 0:
                self.SR = self.SR | self.Negative
                # need to account for 2's complement

        elif inst == 'LDA':     # NZ
            self.AC = operand
            if self.AC < 0:
                self.SR = self.SR | self.Negative
                # need to account for 2's complement

        elif inst == 'CLC':     # set Carry bit to 0
            self.SR = self.SR & 254

        elif inst == 'INX':     # NZ
            if self.X + 1 > 255:
                self.X = 0
            else:
                self.X += 1
            if self.X < 128:
                self.SR = self.SR & 127
            else:
                self.SR = self.SR | self.Negative

        elif inst == 'INY':     # NZ
            if self.Y + 1 > 255:
                self.Y = 0
            else:
                self.Y += 1

            if self.Y < 128:
                self.SR = self.SR & 127
            else:
                self.SR = self.SR | self.Negative

        elif inst == 'NOP':     # affects no flags
            pass

        # pull PC, PC + 1-> PC
        elif inst == 'RTS':     # affects no flags
            pass
        elif inst == 'RTI':     # from stack
            pass
        elif inst == 'SEC':     # C -> sets bit to 1
            self.SR = self.SR | self.Carry

        elif inst == 'SED':     # D -> sets bit to 1
            self.SR = self.SR | self.Decimal

        elif inst == 'SEI':     # I -> sets bit to 1
            self.SR = self.SR | self.Interrupt

        elif inst == 'TAX':     # NZ
            self.X = self.AC
            if self.X > 127:
                self.SR = self.SR | self.Negative

        elif inst == 'TAY':     # NZ
            self.Y = self.AC
            if self.Y > 127:
                self.SR = self.SR | self.Negative

        elif inst == 'TSX':     # NZ
            self.X = self.SP
            if self.X > 127:
                self.SR = self.SR | self.Negative

        elif inst == 'TXA':
            self.AC = self.X
            if self.AC > 127:
                self.SR = self.SR | self.Negative

        elif inst == 'TXS':     # affects no flags
            self.SP = self.X

        elif inst == 'TYA':     # NZ
            self.AC = self.Y
            if self.AC > 127:
                self.SR = self.SR | self.Negative

        elif inst == 'PHP':     # NZ
            self.m.stack[self.SP] = self.SP

            self.SP -= 1
        elif inst == 'PLA':
            self.AC = self.m.stack[self.SP]
            self.SP += 1        # pop from the stack

        elif inst == 'PLP':
            self.SR = self.m.stack[self.SP]
            self.SP += 1        # pop from the stack

        elif inst == 'PHA':
            self.SP -= 1            # move pointer to next available memory space for saving
            self.m.stack[self.SP] = self.AC

        elif inst == 'ASL':  # NZC
            flag = False
            if self.AC & 128 > 0:       # is there a 1 in the 8th bit?
                flag = True

            self.AC = self.AC << 1

            if self.AC > 255:       # set carry flag if a 1 made it's way outside the register
                self.SR = self.SR | self.Carry

            if flag is True:            # it was negative, so set sign bit to 1
                self.AC = self.AC | self.Negative
            self.AC = self.AC & self.v  # clear out any zeros that

        elif inst == 'LSR':
            self.AC = self.AC >> 1

        elif inst == 'ROL':     # NZC
            flag = False
            if self.AC & 128 > 0:
                flag = True
            self.AC = self.AC << 1
            if flag is True:
                self.AC += 1
            self.AC = self.AC & self.v

        elif inst == 'ROR':     # NZC
            flag = False
            if self.AC % 2 == 1:
                flag = True
            self.AC = self.AC >> 1
            if flag is True:
                self.AC = self.AC | 128
                self.SR = self.SR | 128

        else:
            print('Instruction not found in Register class. Inst: ' + inst)


########################################################################
# Class: Monitor
# Description: Class to handle managing the updating of registers and
# outputting the state of the system when needed.
########################################################################
class Monitor:
    """
    When code is executed the Monitor should for each step display:
    the program counter at the step, the OP-code that was executed, the interpret instruction, the addressing mode,
    any operands, the value of the A register after execution, the value of the X register after execution, the value of the
    Y register after execution, current stack pointer, and the bits in the status register.
    """
    instruction_sizes = {'ADC': 2, 'BRK': 1, 'CLD': 1, 'CLI': 1, 'CLV': 1, 'DEX': 1, 'DEY': 1, 'LDX': 2,
                         'LDA': 2, 'CLC': 1, 'INX': 1, 'INY': 1, 'NOP': 1, 'RTS': 1, 'RTI': 1,
                         'SEC': 1, 'SED': 1, 'SEI': 1, 'TAX': 1, 'TAY': 1, 'TSX': 1, 'TXS': 1, 'TYA': 1, 'PHP': 1,
                         'PLA': 1, 'PLP': 1, 'PHA': 1, 'ASL': 1, 'LSR': 1, 'ROL': 1, 'ROR': 1, 'TXA': 1 }
    implied_instructions = ['ADC', 'BRK', 'CLD', 'CLI', 'CLV', 'DEX', 'DEY', 'LDX', 'LDA', 'CLC', 'INX', 'INY',
                            'NOP', 'RTS', 'RTI', 'SEC', 'SED', 'SEI', 'TAX', 'TAY', 'TSX', 'TXS', 'TYA', 'PHP',
                            'PLA', 'PLP', 'TYA', 'PHA', 'TXA']
    implied_opcodes = ['0x69', '0x0', '0xd8', '0x58', '0xb8', '0xca', '0x88', '0xa2', '0xa9', '0x18', '0xe8',
                       '0xc8', '0xea', '0x60', '0x40', '0x38', '0xf8', '0x78', '0xaa', '0xa8', '0xba', '0x9a',
                       '0x98', '0x08', '0x68', '0x28', '0x98', '0x48', '0x8a']
    accumulator_instructions = ['ASL', 'LSR', 'ROL', 'ROR', ]
    accumulator_opcodes = ['0xa', '0x4a', '0x2a', '0x6a', ]

    flag = False  # flags so display header only appears once

    ########################################################################
    # Constructor
    # Description: Initializes class variables and creates a map of instruction
    # to opcode and vice-versa.
    ########################################################################
    def __init__(self, stack):
        self.stack = stack
        self.r = Registers(self)
        self.r.SP = 0xff
        self.op_to_instruction = {}
        self.instruction_to_op = {}
        for i in range(0, len(self.implied_opcodes)):
            self.op_to_instruction[self.implied_opcodes[i]] = self.implied_instructions[i]
            self.instruction_to_op[self.implied_instructions[i]] = self.implied_opcodes[i]

        for i in range(0, len(self.accumulator_instructions)):
            self.op_to_instruction[self.accumulator_opcodes[i]] = self.accumulator_instructions[i]
            self.instruction_to_op[self.accumulator_instructions[i]] = self.accumulator_opcodes[i]

    ########################################################################
    # Name: display
    # Description: Accepts opcode, instruction and addressing mode as string.
    # Handles displaying the processor state after each execution.
    ########################################################################
    def display(self, opcode, inst, amod):
        # set string for status register for output
        sr_str = str(bin(self.r.SR)).replace('0b', '')
        for i in range(0, 8-len(sr_str)):
            sr_str = '0' + sr_str

        # set strings for registers for output
        pc_str = str(hex(self.r.PC)).replace('0x', '').upper()
        opcode_str = opcode.replace('0x', '').upper()
        ac_str = str(hex(self.r.AC)).replace('0x', '').upper()
        x_str = str(hex(self.r.X)).replace('0x', '').upper()
        y_str = str(hex(self.r.Y)).replace('0x', '').upper()
        sp_str = str(hex(self.r.SP)).replace('0x', '').upper()

        # adjust the size of the string to fit for output
        if len(pc_str) == 1:
            pc_str = '00' + pc_str
        if len(opcode_str) == 1:
            opcode_str = '0' + opcode_str
        if len(ac_str) == 1:
            ac_str = '0' + ac_str
        if len(x_str) == 1:
            x_str = '0' + x_str
        if len(y_str) == 1:
            y_str = '0' + y_str
        if len(sp_str) == 1:
            sp_str = '0' + sp_str
        if self.flag is False:
            print('\n PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC')
            self.flag = True
        print(' ' + pc_str, end='')
        if opcode == '00':
            opcode = '00'
            print('  ' + opcode, end='')
        else:
            print('  ' + opcode_str, end='')
        print('  ' + inst, end='')
        print('   ' + amod, end='')
        print(' -- --', end='')
        print('  ' + ac_str, end='')
        print(' ' + x_str, end='')
        print(' ' + y_str, end='')
        print(' ' + sp_str, end='')
        print(' ' + sr_str)

    ########################################################################
    # Name: execute
    # Description: Accepts an address as an int to begin executing instructions.
    # Loops until a break instruction is reached.
    ########################################################################
    def execute(self, address):
        self.r.PC = address             # set the initial program counter register
        opcode = self.stack[self.r.PC]  # get contents of start address
        opcode_str = str(hex(opcode))  # get the contents as a string for readability in coming code

        while opcode != 0x0:            # while the instruction isn't break

            if opcode_str in self.op_to_instruction:    # address mode is implied
                if opcode_str in self.implied_opcodes:
                    amod = 'impl'

                else:                                   # address mode is accumulate
                    amod = '   A'
            else:                                       # error
                print('***ERROR: could not find opcode in either list. opcode: ' + opcode_str)

            if opcode != 0x0:
                i = self.op_to_instruction[opcode_str]  # get instruction

                if len(opcode_str) == 1:
                    opcode_str += '0' + opcode_str
                if self.instruction_sizes[i] == 1:
                    self.r.exe_instruction(i)  # execute instruction on register
                    self.display(opcode_str, i, amod)  # display the system state
                else:
                    self.r.exe_instruction(i, self.stack[self.r.PC+1])  # execute instruction on register
                    self.display(opcode_str, i, amod)  # display the system state
                self.r.PC += self.instruction_sizes[i]
                opcode = self.stack[self.r.PC]  # get contents of next address
                opcode_str = str(hex(opcode))   # get the contents as a string for readability in coming code

        if opcode == 0x0:
            self.r.exe_instruction('BRK')
            self.display('00', 'BRK', 'impl')  # one last system state display
            self.flag = False   # reset display flag in case this object is used again for another execution


########################################################################
# Name: print_address_range
# Description: takes the start address, end address and the stack
# to print the contents of the stack within the range of the addresses.
########################################################################
def print_address_range(begin, end, stack):
    for i in range(begin, end+1):
        if i % 8 == 0:
            print('\n', end='')
            print(str(hex(i)).lstrip('0x').upper() + ':', end=' ')

        if stack[i] == 0:
            print('00', end='')
        print(str(hex(stack[i])).lstrip('0x').upper(), end=' ')
    print('\n', end='')


####################################################################
# Name: parse_file
# Description: Accepts the file name to open and parse. The file
# should be an object file of a specific format. The addresses
# contained in the .o file are mapped with their corresponding
# bytes. Returns said dictionary.
####################################################################
def parse_file(file_name):
    program_line = []
    program_map = {}
    index = 0
    with open(file_name) as file:
        for line in file:
            line = line.lower()
            line = line.replace(':', '')
            line = line.strip()
            program_line.append(line.split(' '))
            # print(program_line)
            try:
                if len(program_line[index]) == 2:
                    program_map["0x" + program_line[index][0]] = program_line[index][1]
                elif len(program_line[index]) == 3:
                    program_map["0x" + program_line[index][0]] = [program_line[index][1], program_line[index][2]]
            except ValueError:
                print("something went wrong while parsing")
            index += 1
    return program_map


######################################################################
# Name: init_memory
# Description: initializes a zero array of size 2^16 for the
# t34 stack emulation. Each element is 1 byte (unsigned char as int)
# Returns the zero array.
######################################################################
def init_memory():
    stack_as_list = []
    memory_size = 65536                   # 2^16 bytes in memory
    for i in range(0, memory_size):
        stack_as_list.append(0)           # set the value in memory to zero

    return arr.array('i', stack_as_list)  # returns array of unsigned char (size = 1 byte)


#################################################################
# Name: write_to_memory
# Description: Takes address and contents as strings, converts
# them to hex, then writes the contents to the address in memory.
# Returns the stack when finished.
#################################################################
def write_to_memory(address, contents, stack):

    # parse the string to its individual components
    contents = contents.split(' ')

    # convert the start address to an int
    address = int(address, 16)

    # convert each component in contents to hex
    for i in range(0, len(contents)):
        value = int(contents[i], 16)
        stack[address+i] = value
    return stack


###############################################################
# Name: write_program_to_memory
# Description: Takes the parsed input o file map and writes the
# bytes to emulated t34 memory. Returns the newly updated stack.
###############################################################
def write_program_to_memory(stack, program_map):
    for key in program_map:
        index = int(key, 16)                            # get the index into the arr as int
        if isinstance(program_map[key], str):           # if the key gives a 1 byte instruction
            stack[index] = int(program_map[key], 16)
        else:                                           # 2 byte instruction case
            stack[index] = int(program_map[key][0], 16)
            stack[index+1] = int(program_map[key][1], 16)
    return stack

