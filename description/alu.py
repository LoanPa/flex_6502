import py4hw

class Alu(py4hw.Logic):

    def __init__(self, parent, name, a, b, op_sel, carry_in, result, zero_flag, negative_flag, carry_out, overflow_flag):
        super().__init__(parent, name)
        
        self.addIn("a", a)
        self.addIn("b", b)
        self.addIn("op_sel", op_sel)
        self.addIn("carry_in", carry_in)

        self.addOut("result", result)
        self.addOut("zero", zero_flag)
        self.addOut("negative", negative_flag)
        self.addOut("carry_out", carry_out)
        self.addOut("overflow", overflow_flag)

        BYP = 0
        ADD = 1
        AND = 2
        OR  = 3
        XOR = 4
        SUB = 5
        SHR = 6
        BIT = 7        

        tmp_result = []
        for i in range(8):
            tmp_result.append(self.wire(f"tmp_result_{i}", 8))

        # ADD és 001 i SHR 110, utilitzem el primer bit per a diferenciar-les
        sel_bit_0 = self.wire("sel_bit_0")
        py4hw.Bit(self, "bit0", op_sel, 0, sel_bit_0)

        # Amb el tercer bit diferenciem ADD i SUB (001 i 101)
        sel_bit_2 = self.wire("sel_bit_2")
        py4hw.Bit(self, "bit2", op_sel, 2, sel_bit_2)

        # Aquí es declaren els cables per a gestionar el flag negatiu, si es BIT el resultat és diferent
        result_sign = self.wire("result_sign")
        bit_negative = self.wire("bit_negative")
        is_bit_selected = self.wire("is_bit_selected")

        tmp_negative = [result_sign, bit_negative]

        sum_carry = self.wire("sum_carry")
        shift_right_carry = self.wire("shift_right_carry")
        tmp_sum_carry = self.wire("tmp_sum_carry")
        tmp_carry = [shift_right_carry, sum_carry]


        sum_overflow = self.wire("tmp_overflow")
        bit_overflow = self.wire("bit_overflow")
        tmp_overflow = [sum_overflow, bit_overflow]

        # Bypass
        py4hw.Buf(self, "bypass", a, tmp_result[BYP])
        # Add
        py4hw.Add(self, "add", a, b, tmp_result[ADD], carry_in, tmp_sum_carry)
        # And
        py4hw.And2(self, "and", a, b, tmp_result[AND])
        # Or
        py4hw.Or2(self, "or", a, b, tmp_result[OR])
        # Xor
        py4hw.Xor2(self, "xor", a, b, tmp_result[XOR])
        # Sub
        py4hw.Buf(self, "add_to_sub_buffer", tmp_result[ADD], tmp_result[SUB])
        # Shr
        a_bits = self.wires("a_bits", 8, 1)
        py4hw.BitsLSBF(self, "bits_shr", a, a_bits)      
        rotate_bits = a_bits[1:]
        rotate_bits.append(carry_in)
        py4hw.ConcatenateLSBF(self, "concat_rotate", rotate_bits, tmp_result[SHR])
        # Bit
        py4hw.Buf(self, "bit_logic_connection", tmp_result[AND], tmp_result[BIT])

        # Resultat
        py4hw.Mux(self, "mux", op_sel, tmp_result, result)

        # Zero
        result_bits = self.wires("bits_result", 8, 1)
        py4hw.BitsLSBF(self, "result_bits", result, result_bits)
        py4hw.Nor(self, "zero_nor", result_bits, zero_flag)

        # Negative
        py4hw.Bit(self, "result_sign", result, 7, result_sign)
        py4hw.Bit(self, "bit_sign", b, 7, bit_negative)
        op_sel_bits = self.wires("op_sel_bits", 3, 1)
        py4hw.BitsLSBF(self, "bits_op_sel", op_sel, op_sel_bits)
        py4hw.And(self, "bit_detector", op_sel_bits, is_bit_selected)
        py4hw.Mux(self, "negative_mux", is_bit_selected, tmp_negative, negative_flag)

        # Carry
        py4hw.Bit(self, "SHR_carry", a, 0, shift_right_carry)
        py4hw.Xor2(self, "carry_xor", sel_bit_2, tmp_sum_carry, sum_carry)
        py4hw.Mux(self, "carry_mux", sel_bit_0, tmp_carry, carry_out)
        
        # Overflow
        py4hw.Bit(self, "BIT_overflow", b, 6, bit_overflow)
        
        # Això es podria simplificar molt agafant el carry intern més significatiu del sumador, queda pendent
        a_sign = self.wire("a_sign")
        b_sign = self.wire("b_sign")
        not_a_sign = self.wire("not_a_sign")
        not_b_sign = self.wire("not_b_sign")
        not_result_sign = self.wire("not_result_sign")

        sign_and_1 = self.wire("sign_and_1")
        sign_and_2 = self.wire("sign_and_2")
        sign_and_3 = self.wire("sign_and_3")
        sign_and_4 = self.wire("sign_and_4")

        py4hw.Bit(self, "a_sign", a, 7, a_sign)
        py4hw.Bit(self, "b_sign", b, 7, b_sign)
        py4hw.Not(self, "not_a_sign", a_sign, not_a_sign)
        py4hw.Not(self, "not_b_sign", b_sign, not_b_sign)
        py4hw.Not(self, "not_result_sign", result_sign, not_result_sign)
        
        # A & B = S1
        py4hw.And2(self, "sign_and_a_b", a_sign, b_sign, sign_and_1)
        # (S1) & !R = S2
        py4hw.And2(self, "sign_and_a_b_not_r", sign_and_1, not_result_sign, sign_and_2)
        # !A & !B = S3
        py4hw.And2(self, "sign_and_not_a_not_b", not_a_sign, not_b_sign, sign_and_3)
        # S3 & R = S4 
        py4hw.And2(self, "sign_and_not_a__not_b_r", sign_and_3, result_sign, sign_and_4)
        # S2 | S4 = sum_overflow
        py4hw.Or2(self, "overflow_xor", sign_and_2, sign_and_4, sum_overflow)

        py4hw.Mux(self, "overflow_mux", is_bit_selected, tmp_overflow, overflow_flag)
