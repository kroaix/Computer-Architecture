"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    HLT = 0b00000001
    LDI = 0b10000010
    PRN = 0b01000111
    MUL = 0b10100010
    

    def __init__(self):
        """Construct a new CPU."""
        #pc = program counter
        self.pc = 0
        #ram = memory 256 bytes
        self.ram = [0] * 256
        #register = 8
        self.reg = [0] * 8
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

        if len(sys.argv) != 2:
            print("Wrong number of arguments")
            sys.exit(1)
        with open(sys.argv[1]) as f:
            for line in f:
                line_split = line.split('#')
                command = line_split[0].strip()
                if command == '':
                    continue
                else:
                    self.ram[address] = int(command[:8], 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.HLT:
            self.running = False
            self.pc += 1
        elif op == self.LDI:
            self.reg[reg_a] = reg_b
            self.pc += 3
        elif op == self.PRN:
            print(self.reg[reg_a])
            self.pc += 2
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]
            
            self.alu(IR, reg_a, reg_b)