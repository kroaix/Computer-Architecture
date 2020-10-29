"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    HLT = 0b00000001
    LDI = 0b10000010
    PRN = 0b01000111
    

    def __init__(self):
        """Construct a new CPU."""
        #pc = program counter
        self.pc = 0
        #ram = memory 256 bytes
        self.ram = [0] * 256
        #register = 8
        self.register = [0] * 8
        #we are going to default running to True
        self.running = True

    #passing an address and returning location in ram from that address
    def ram_read(self, address):
        return self.ram[address]
    #setting a value to location in ram from the address passed
    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if IR == self.HLT:
                self.running = False
                self.pc += 1
            elif IR == self.LDI:
                self.register[reg_a] = reg_b
                self.pc += 3
            elif IR  == self.PRN:
                print(self.register[reg_a])
                self.pc += 2
            else:
                self.pc += 1
