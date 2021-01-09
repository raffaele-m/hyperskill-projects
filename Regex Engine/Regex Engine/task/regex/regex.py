# write your code here
import sys
sys.setrecursionlimit(10000)


class RegEngine:

    def __init__(self):
        self.reg, self.inp, self.fixed = None, None, None

    def compare(self, reg, inp):
        if reg:
            if reg[0] == '^':
                return self.strict_compare(reg[1:], inp)
            elif reg[-1] == '$':
                return self.strict_compare(reg[0:len(reg)-1], inp[-len(reg)+1:])
            elif self.strict_compare(reg, inp):
                return True
            else:
                return reg in inp
        else:
            return True

    def strict_compare(self, reg, inp):
        if len(reg) == 1 and reg[0] == '$' and not inp:
            return True
        if (len(reg) == 1 and reg[0] == '.') or not reg:
            return True
        elif inp == '':
            return False
        elif len(reg) > 1:
            if reg[0] == '\\':
                return self.compare(reg[1:], inp)
            if reg[1] == '?':
                return self.strict_compare(reg[2:], inp[1:]) if reg[0] == inp[0] else self.strict_compare(reg[2:], inp[0:])
            elif reg[1] == '*':
                return self.strict_compare(reg[2:], inp.strip(inp[0])) if reg[0] == inp[0] else self.strict_compare(reg[2:], inp[0:])
            elif reg[1] == '+':
                return self.strict_compare(reg[2:], inp.strip(inp[0])) if reg[0] == inp[0] or reg[0] == '.' else False
            elif reg[0] == inp[0] or reg[0] == '.':
                return self.strict_compare(reg[1:], inp[1:])
            else:
                return False
        else:
            return reg[0] == inp[0]


regex, in_var = input().split('|')
print(RegEngine().compare(regex, in_var))

