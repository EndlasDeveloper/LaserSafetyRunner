from main import *
import unittest


#############################################################
# Unit tests for initializing the stack for the T34 emulator
#############################################################
class TestT34EmulatorStackInitialization(unittest.TestCase):

    # test that the stack array is the size of the T34 stack
    def test_memory_size(self):
        t = init_memory();
        self.assertEqual(65536, len(t))

    # test that the stack array is initialized to a zero array
    def test_is_zero_array(self):
        t = init_memory()
        for i in range(0, len(t)):
            self.assertEqual(0, t[i])


#############################################################
# Unit tests for initializing the emulated registers for T34
#############################################################
class TestT34EmulatorRegisterInitialization(unittest.TestCase):
    def test_registers_are_zero(self):

        # test the Register class only
        r = Registers(0)
        self.assertEqual(0, r.PC)
        self.assertEqual(0, r.AC)
        self.assertEqual(0, r.X)
        self.assertEqual(0, r.Y)
        self.assertEqual(0b00100000, r.SR)
        self.assertEqual(0, r.SP)

        # test the Register class nested with Monitor
        stack = init_memory()
        m = Monitor(stack)
        self.assertEqual(0, m.r.PC)
        self.assertEqual(0, m.r.AC)
        self.assertEqual(0, m.r.X)
        self.assertEqual(0, m.r.Y)
        self.assertEqual(0b00100000, m.r.SR)
        self.assertEqual(0xff, m.r.SP)


#############################################################
# Unit tests for parsing on object file into a map for access
#############################################################
class TestFileParsing(unittest.TestCase):

    # test the parsing function outputs the expected dictionary
    def test_sample_1_is_correct(self):
        pm = parse_file('sample_1.o')
        self.assertEqual(1, len(pm))
        self.assertEqual('ea', pm['0x300'])

    def test_sample_2_is_correct(self):
        pm = parse_file('sample_2.o')
        self.assertEqual(8, len(pm))
        self.assertEqual('78', pm['0xf000'])
        self.assertEqual('a2', pm['0xf002'][0])
        self.assertEqual('ff', pm['0xf002'][1])


#############################################################
# Unit tests writing program to memory array from o file
#############################################################
class TestWritingProgramToMemory(unittest.TestCase):

    # test sample_1.o - only one line in o file, single byte to write
    def test_single_entry_memory_write(self):
        stack = init_memory()
        pm = parse_file('sample_1.o')
        stack = write_program_to_memory(stack, pm)
        for i in range(0, len(stack)):
            if i != int(0x300):
                self.assertEqual(0, stack[i])
            else:
                self.assertEqual(0xea, stack[i])

    # test sample_3.o - only 1 line in o file, dual byte to write
    def test_single_entry_two_byte_memory_write(self):
        stack = init_memory()
        pm = parse_file('sample_3.o')
        stack = write_program_to_memory(stack, pm)
        self.assertEqual(0xaa, stack[int(0x400)])
        self.assertEqual(0xd, stack[int(0x401)])

    # test sample_4.o - multiple lines (3) in object file, single byte to write per line
    def test_multiple_entry_single_byte_memory_write(self):
        stack = init_memory()
        pm = parse_file('sample_4.o')
        stack = write_program_to_memory(stack, pm)
        self.assertEqual(0xd8, stack[int(0xf001)])

    # test sample_2.o - 8 entries in o file, has 1 and 2 bytes to write per line
    def test_multiple_entry_mixed_byte_size_memory_write(self):
        stack = init_memory()
        pm = parse_file('sample_2.o')
        stack = write_program_to_memory(stack, pm)
        self.assertEqual(0xD8, stack[0xf001])
        self.assertEqual(0xa9, stack[0xf005])
        self.assertEqual(0x00, stack[0xf006])


###################################################################
# Unit tests for writing to memory locations after initialization
###################################################################
class TestWritingToMemory(unittest.TestCase):
    # test for writing to memory with a single entry
    def test_single_write(self):
        stack = init_memory()
        stack = write_to_memory('0', 'AA', stack)
        self.assertEqual(0xaa, stack[0])
        self.assertEqual(0x00, stack[1])

    # test for writing to memory with multiple entries
    def test_multiple_write(self):
        stack = init_memory()
        stack = write_to_memory('0', 'AA AB', stack)
        self.assertEqual(0xaa, stack[0])
        self.assertEqual(0xab, stack[1])


###################################################################
# Unit tests for executing instructions from memory.
###################################################################
class TestExecuteFromMemory(unittest.TestCase):

    # test simplest case where only a break is executed
    def test_brk_only(self):
        stack = init_memory()
        m = Monitor(stack)
        m.execute(1)        # pass 0 as index - should be a zero array at this point

        self.assertEqual(1, m.r.PC)
        self.assertEqual(0, m.r.AC)
        self.assertEqual(0, m.r.X)
        self.assertEqual(0, m.r.Y)
        self.assertEqual(0b00110100, m.r.SR)
        self.assertEqual(0xfc, m.r.SP)

    # only 1 immediate type instruction is tested (no register changing)
    def test_single_instruction_immediate(self):
        stack = init_memory()
        pm = parse_file('sample_1.o')
        stack = write_program_to_memory(stack, pm)
        m = Monitor(stack)
        m.execute(0x300)                    # contents @ 0x300 should be NOP

        self.assertEqual(0x301, m.r.PC)     # 301 because one non-brk instruction was executed
        self.assertEqual(0, m.r.AC)
        self.assertEqual(0, m.r.X)
        self.assertEqual(0, m.r.Y)
        self.assertEqual(0b00110100, m.r.SR)
        self.assertEqual(0xfc, m.r.SP)

    # test an instruction that manipulates the y register
    def test_single_instruction_immediate_y_reg(self):
        stack = init_memory()
        pm = parse_file('single_implied_inst_y_reg.o')
        stack = write_program_to_memory(stack, pm)
        m = Monitor(stack)
        m.execute(0x300)                    # contents @ 0x300 should be NOP

        self.assertEqual(0x301, m.r.PC)     # 301 because one non-brk instruction was executed
        self.assertEqual(0, m.r.AC)
        self.assertEqual(0, m.r.X)
        self.assertEqual(1, m.r.Y)          # instruction was increment y (INY)
        self.assertEqual(0b00110100, m.r.SR)
        self.assertEqual(0xfc, m.r.SP)

    # test instruction that manipulates the accumulator
    def test_instruction_immediate_ac_reg(self):
        stack = init_memory()
        pm = parse_file('test_instruction_immediate_ac_reg.o')
        stack = write_program_to_memory(stack, pm)
        m = Monitor(stack)
        m.execute(0x300)                    # contents @ 0x300 should be NOP

        self.assertEqual(0x302, m.r.PC)     # 301 because one non-brk instruction was executed
        self.assertEqual(1, m.r.AC)
        self.assertEqual(0, m.r.X)
        self.assertEqual(1, m.r.Y)          # instruction was increment y (INY)
        self.assertEqual(0b00110100, m.r.SR)
        self.assertEqual(0xfc, m.r.SP)

    # stack pointer instruction test
    def test_instruction_implied_sp_reg(self):
        stack = init_memory()
        pm = parse_file('single_implied_instruction_sp_reg.o')
        stack = write_program_to_memory(stack, pm)
        m = Monitor(stack)
        m.execute(0x300)                    # contents @ 0x300 should be NOP

        self.assertEqual(0x303, m.r.PC)     # 301 because one non-brk instruction was executed
        self.assertEqual(1, m.r.AC)
        self.assertEqual(0, m.r.X)
        self.assertEqual(1, m.r.Y)          # instruction was increment y (INY)
        self.assertEqual(0b00110100, m.r.SR)
        self.assertEqual(0xfb, m.r.SP)
        self.assertEqual(1, m.stack[0x0fe])

    # test the registers handling negative values
    def test_when_y_reg_is_negative(self):
        #     300  88  DEY  impl ---- 00 00 FF FF 10100000
        stack = init_memory()
        pm = parse_file('y_register_is_negative.o')
        stack = write_program_to_memory(stack, pm)
        m = Monitor(stack)
        m.execute(0x300)

        self.assertEqual(0x301, m.r.PC)     # 301 because one non-brk instruction was executed
        self.assertEqual(0, m.r.AC)
        self.assertEqual(0, m.r.X)
        self.assertEqual(0xFF, m.r.Y)
        self.assertEqual(0b10110100, m.r.SR)
        self.assertEqual(0xfc, m.r.SP)

    # full example taken from the project hand out
    def test_full_example_1(self):
        stack = init_memory()
        pm = parse_file('full_example_1.o')
        stack = write_program_to_memory(stack, pm)
        m = Monitor(stack)
        m.execute(0x300)

        self.assertEqual(0x30b, m.r.PC)
        self.assertEqual(0xfd, m.r.AC)
        self.assertEqual(0xfd, m.r.X)
        self.assertEqual(128, m.r.Y)
        self.assertEqual(0b10110101, m.r.SR)
        self.assertEqual(0xfc, m.r.SP)

    # full example taken from the project hand out
    def test_full_example_2(self):
        stack = init_memory()
        pm = parse_file('full_example_2.o')
        stack = write_program_to_memory(stack, pm)
        m = Monitor(stack)
        m.execute(0x300)

        self.assertEqual(0x308, m.r.PC)
        self.assertEqual(1, m.r.AC)
        self.assertEqual(2, m.r.X)
        self.assertEqual(1, m.r.Y)
        self.assertEqual(0b00110100, m.r.SR)
        self.assertEqual(0xfc, m.r.SP)