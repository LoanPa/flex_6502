import py4hw
from description import Alu
hw = py4hw.HWSystem()

def sim_bypass(a:int):
    result = {}
    a &= 0xFF

    result["result"] = a
    
    result["zero"] = int(a == 0)

    return result

def sim_suma(a:int, b:int, c:int) -> dict:
    result = {}
    a &= 0xFF
    b &= 0xFF
    c &= 0x01

    sum = a + b + c
    r = sum % 256
    result["result"] = r

    carry_out = (sum >> 8) & 0x01
    result["carry"] = int(carry_out)

    r_sign = (r >> 7) & 1
    result["negative"] = r_sign

    a_sign = (a >> 7) & 1 
    b_sign = (b >> 7) & 1
    overflow = (a_sign == b_sign) and (r_sign != a_sign)
    result["overflow"] = int(overflow)

    result["zero"] = int(r == 0)

    return result

def sim_and(a:int, b:int) -> dict:
    result = {}
    a &= 0xFF
    b &= 0xFF 

    r = a & b
    result["result"] = r

    result["zero"] = int(r == 0)

    return result

def sim_or(a:int, b:int) -> dict:
    result = {}
    a &= 0xFF
    b &= 0xFF 

    r = a | b
    result["result"] = r

    result["zero"] = int(r == 0)

    return result

def sim_xor(a:int, b:int) -> dict:
    result = {}
    a &= 0xFF
    b &= 0xFF 

    r = a ^ b
    result["result"] = r

    result["zero"] = int(r == 0)

    return result

def sim_resta(a:int, b:int, c:int) -> dict:
    result = {}
    a &= 0xFF
    b &= 0xFF
    c &= 0x01
    not_b = ~b & 0xFF
    sub = a + not_b + c
    r = sub % 256
    result["result"] = r

    carry_out = (sub >> 8) & 0x01
    result["carry"] = int(carry_out)

    r_sign = (r >> 7) & 1
    result["negative"] = r_sign

    a_sign = (a >> 7) & 1 
    b_sign = (b >> 7) & 1
    overflow = (a_sign == b_sign) and (r_sign != a_sign)
    result["overflow"] = int(overflow)

    result["zero"] = int(r == 0)

    return result

def sim_shift(a:int, c:int) -> dict:
    result = {}
    a &= 0xFF
    c &= 0x01
    
    r = a >> 1 | ((c << 7) & 0x80)
    result["result"] = r

    carry_out = a & 0x01
    result["carry"] = carry_out

    r_sign = (r >> 7) & 1
    result["negative"] = r_sign


    result["zero"] = int(r == 0)

    return result

def sim_bit(a:int, b:int) -> dict:
    result = {}
    a &= 0xFF
    b &= 0xFF 

    r = a & b

    result["negative"] = (b >> 7) & 0x01

    result["overflow"] = (b >> 6) & 0x01

    result["zero"] = int(r == 0)

    return result

def print_results(results:dict):
    print("R:", f"{results["result"]:08b}", end=' ')
    print("C:", f"{results["carry"]:01b}", end=' ')
    print("N:", f"{results["negative"]:01b}", end=' ')
    print("V:", f"{results["overflow"]:01b}", end=' ')
    print("Z:", f"{results["zero"]:01b}")

#print_results(suma(125,10,1))

a = py4hw.Wire(hw, "a", 8)
b = py4hw.Wire(hw, "b", 8)
sel = py4hw.Wire(hw, "sel", 3)
carry_in = py4hw.Wire(hw, "carry_in", 1)
   
result = py4hw.Wire(hw, "result", 8)
zero = py4hw.Wire(hw, "zero", 1)
negative = py4hw.Wire(hw, "negative", 1)
carry_out = py4hw.Wire(hw, "carry_out", 1)
overflow = py4hw.Wire(hw, "overflow", 1)


ca = py4hw.Constant(hw, "a", 7, a)
cb = py4hw.Constant(hw, "b", 3, b)
csel = py4hw.Constant(hw, "sel", 1, sel)
cc = py4hw.Constant(hw, "carry_in", 1, carry_in)

alu = Alu(hw, "alu", a, b, sel, carry_in, result, zero, negative, carry_out, overflow)

BYP = 0
ADD = 1
AND = 2
OR  = 3
XOR = 4
SUB = 5
SHR = 6
BIT = 7  


vsel = SUB
    
csel.value = vsel
va = 0
vb = 1
vc = 0
ca.value = va
cb.value = vb
cc.value = vc

hw.getSimulator().clk(1)

print("Starting test")
for i in range(256):
    print(i)
    for j in range(256):
        for k in range(2):
            
            va = i
            vb = j
            vc = k
            ca.value = va
            cb.value = vb
            cc.value = vc

            hw.getSimulator().clk(1)
            results = sim_resta(va, vb, vc)

            #print(va, vb, vc,'|', result.get(), negative.get(), results["negative"])
            #print(zero.get(), negative.get(), overflow.get(), carry_out.get())
            #print("va:", va, "vb:", vb, "vc:", vc,"|  ",overflow.get(), "|", results["overflow"])
            #print("va:", va, "vb:", vb, "vc:", vc,"|  ",carry_out.get(), "|", results["carry"])
            #print("va:", va, "vb:", vb, "|  ",zero.get(), "|", results["zero"])
            
            assert(result.get() == results["result"])
            assert(zero.get() == results["zero"])
            assert(negative.get() == results["negative"])
            assert(overflow.get() == results["overflow"])
            assert(carry_out.get() == results["carry"])


print("Verification test passed!")
#def testAlu(sel, a, b, carry):


