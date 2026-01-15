import py4hw

# Registres
A    = 0
X    = 1
Y    = 2
SP   = 3
MBR  = 4
PCL  = 5
PCH  = 6
MARL = 7
MARH = 8
IR   = 9
CTL  = 10

# Operacions ALU
BYP = 0
ADD = 1
AND = 2
OR  = 3
XOR = 4
SUB = 5
SHR = 6
BIT = 7 

# Estats
FETCH_T0 = 0
FETCH_T1 = 1
DECODE = 2
EXECUTE_ALU = 3
ZP_FETCH = 4
TRANSFER_MBR_TO_A = 5

class UC(py4hw.Logic):
    def __init__(self, parent, name, 
                 # Entrades     
                 reset:py4hw.Wire,
                 ir_data:py4hw.Wire,
                 

                 # sortides
                 
                 pc_inc:py4hw.Wire,
                 mbr_enable:py4hw.Wire,

                 enable_sel:py4hw.Wire, write:py4hw.Wire,
                 reg_sel_a:py4hw.Wire,
                 reg_sel_b:py4hw.Wire,
                 
                 mbr_src_sel:py4hw.Wire,  # 0=Bus, 1=Memòria 
                 mm_addr_src:py4hw.Wire,  # 0=PC, 1=MAR
                 clear_marh:py4hw.Wire,
                 
                 # Control  ALU [...]
                 alu_op:py4hw.Wire,
                 flag_in_sel:py4hw.Wire,
                 n_enable:py4hw.Wire, v_enable:py4hw.Wire,
                 b_enable:py4hw.Wire, i_enable:py4hw.Wire,
                 z_enable:py4hw.Wire, c_enable:py4hw.Wire
                 ):
        super().__init__(parent, name)

        self.reset = self.addIn("reset",  reset)
        self.ir_data = self.addIn("ir_data",  ir_data)
        
        self.pc_inc = self.addOut("pc_inc", pc_inc)
        self.mbr_enable = self.addOut("mbr_enable", mbr_enable)
        
        self.enable_sel = self.addOut("enable_sel", enable_sel)
        self.write = self.addOut("write", write)

        self.reg_sel_a = self.addOut("reg_sel_a", reg_sel_a)
        self.reg_sel_b = self.addOut("reg_sel_b", reg_sel_b)

        self.mbr_src_sel = self.addOut("mbr_src_sel",  mbr_src_sel)
        self.mm_addr_src = self.addOut("mm_addr_src",  mm_addr_src)
        self.clear_marh = self.addOut("clear_marh", clear_marh)
        
        self.alu_op = self.addOut("alu_op", alu_op)
        self.flag_in_sel = self.addOut("flag_in_sel", flag_in_sel)
        self.n_enable = self.addOut("n_enable", n_enable)
        self.v_enable = self.addOut("v_enable", v_enable)
        self.b_enable = self.addOut("b_enable", b_enable)
        self.i_enable = self.addOut("i_enable", i_enable)
        self.z_enable = self.addOut("z_enable", z_enable)
        self.c_enable = self.addOut("c_enable", c_enable)


        self.state = 0


    def default_values(self):
        """for i in self.outPorts:
            i.wire.put(0)"""
        self.pc_inc.put(0)
        self.enable_sel.put(0)
        self.write.put(0)

        self.reg_sel_a.put(0)
        self.reg_sel_b.put(0)

        self.mbr_src_sel.put(0)
        self.mm_addr_src.put(0)

        self.alu_op.put(0)
# Helpers per facilitar la lectura del codi 
    def _fetch_pc_to_mbr(self):
        self.mm_addr_src.prepare(0)   # Agafem adreça de PC
        self.mbr_src_sel.prepare(1)   # mbr agafa la dada de memòria
        self.write.prepare(1)         # Habilitem l'escriptura
        self.pc_inc.prepare(1)        # Actualitzem PC
    def _fetch_mar_to_mbr(self):
        self.mm_addr_src.prepare(1)  # Accedim a l'adreça de memòria continguda al mar
        self.mbr_src_sel.prepare(1)   # mbr agafa la dada de memòria
        self.mbr_enable.prepare(1)
        self.write.prepare(1)
    def transfer_pc_to_mar(self):
        self.reg
        self.write.prepare(1)
        pass

    def _implicit_addressing(self, aaa, cc):
        pass
    def _accumulator_addressing(self, aaa, cc):
        pass

    def _immediate_addressing(self, aaa, cc):
        # Dada a PC, llegim memòria i la carreguem al registre corresponent
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                self._fetch_pc_to_mbr()
                self.state = EXECUTE_ALU
            elif (aaa == 1):  # AND
                self._fetch_pc_to_mbr()
                self.state = EXECUTE_ALU
            elif (aaa == 2):  # EOR
                self._fetch_pc_to_mbr()
                self.state = EXECUTE_ALU
            elif (aaa == 3):  # ADC
                self._fetch_pc_to_mbr()
                self.state = EXECUTE_ALU
            elif (aaa == 4):  # STA
                pass # Operació no documentada
            elif (aaa == 5):  # LDA
                self._fetch_pc_to_mbr()
                self.state = TRANSFER_MBR_TO_A
            elif (aaa == 6):  # CMP
                self._fetch_pc_to_mbr()
                self.state = EXECUTE_ALU
            elif (aaa == 7):  # SBC
                self._fetch_pc_to_mbr()
                self.state = EXECUTE_ALU

    def _zero_page_addressing(self, aaa, cc):
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                self.clear_marh.prepare(1)  # MARH = 0
                self._fetch_mar_to_mbr()
                self.state = ZP_FETCH

            elif (aaa == 1):  # AND
                pass
            elif (aaa == 2):  # EOR
                pass
            elif (aaa == 3):  # ADC
                pass
            elif (aaa == 4):  # STA
                pass
            elif (aaa == 5):  # LDA
                pass
            elif (aaa == 6):  # CMP
                pass
            elif (aaa == 7):  # SBC
                pass
    def _zero_page_x_addressing(self, aaa, cc):
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                pass
            elif (aaa == 1):  # AND
                pass
            elif (aaa == 2):  # EOR
                pass
            elif (aaa == 3):  # ADC
                pass
            elif (aaa == 4):  # STA
                pass
            elif (aaa == 5):  # LDA
                self._fetch_pc_mem_to_reg(A)
            elif (aaa == 6):  # CMP
                pass
            elif (aaa == 7):  # SBC
                pass
    def _zero_page_y_addressing(self, aaa, cc):
        pass
    def _relative_addressing(self, aaa, cc):
        pass
    def _absolute_addressing(self, aaa, cc):
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                pass
            elif (aaa == 1):  # AND
                pass
            elif (aaa == 2):  # EOR
                pass
            elif (aaa == 3):  # ADC
                pass
            elif (aaa == 4):  # STA
                pass
            elif (aaa == 5):  # LDA
                self._fetch_pc_mem_to_reg(A)
            elif (aaa == 6):  # CMP
                pass
            elif (aaa == 7):  # SBC
                pass
    def _absolute_x_addressing(self, aaa, cc):
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                pass
            elif (aaa == 1):  # AND
                pass
            elif (aaa == 2):  # EOR
                pass
            elif (aaa == 3):  # ADC
                pass
            elif (aaa == 4):  # STA
                pass
            elif (aaa == 5):  # LDA
                self._fetch_pc_mem_to_reg(A)
            elif (aaa == 6):  # CMP
                pass
            elif (aaa == 7):  # SBC
                pass
    def _absolute_y_addressing(self, aaa, cc):
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                pass
            elif (aaa == 1):  # AND
                pass
            elif (aaa == 2):  # EOR
                pass
            elif (aaa == 3):  # ADC
                pass
            elif (aaa == 4):  # STA
                pass
            elif (aaa == 5):  # LDA
                self._fetch_pc_mem_to_reg(A)
            elif (aaa == 6):  # CMP
                pass
            elif (aaa == 7):  # SBC
                pass
    def _indirect_addressing(self, aaa, cc):
        pass
    def _indexed_indirect_addressing(self, aaa, cc):
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                pass
            elif (aaa == 1):  # AND
                pass
            elif (aaa == 2):  # EOR
                pass
            elif (aaa == 3):  # ADC
                pass
            elif (aaa == 4):  # STA
                pass
            elif (aaa == 5):  # LDA
                self._fetch_pc_mem_to_reg(A)
            elif (aaa == 6):  # CMP
                pass
            elif (aaa == 7):  # SBC
                pass
    def _indirect_indexed_addressing(self, aaa, cc):
        if cc == 0x01:  # Grup 1, Aritmètic
            if (aaa == 0):  # ORA
                pass
            elif (aaa == 1):  # AND
                pass
            elif (aaa == 2):  # EOR
                pass
            elif (aaa == 3):  # ADC
                pass
            elif (aaa == 4):  # STA
                pass
            elif (aaa == 5):  # LDA
                self._fetch_pc_mem_to_reg(A)
            elif (aaa == 6):  # CMP
                pass
            elif (aaa == 7):  # SBC
                pass

    def clock(self):

        if(self.reset.get() == 1):
            self.default_values()
            self.state = FETCH_T0
            return
        
        # Borrem sortides
        self.default_values()

        # Decodificació de la instrucció
        ir_val = self.ir_data.get()

        cc  = (ir_val >> 0) & 0x03 # grup
        bbb = (ir_val >> 2) & 0x07 # mode adreçament
        aaa = (ir_val >> 5) & 0x07 # operació


        if(self.state == FETCH_T0):
            self.mm_addr_src.prepare(0)

            self.state = FETCH_T1

        elif(self.state == FETCH_T1):

            self.pc_inc.prepare(1)       # PC <-[PC] + 1
            self.enable_sel.prepare(IR)  
            self.write.prepare(1)

            self.state = DECODE

        elif(self.state == DECODE):

            # cc=01: Grup 1, Aritmètic
            if(cc == 0x01):
                if(bbb == 0x00):  # (zp,x)
                    pass
                elif(bbb == 0x01): # zp
                    pass
                elif(bbb == 0x02): # #immediat
                    self._immediate_addressing(aaa, cc)
                elif(bbb == 0x03): # absolut
                    pass
                elif(bbb == 0x04): # (zp),Y
                    pass
                elif(bbb == 0x05): # zp,X
                    pass
                elif(bbb == 0x06): # absolut,Y
                    pass
                elif(bbb == 0x07): # absolut,X
                    pass

            # cc=02: Grup 2, memòria i rotacions
            elif(cc == 0x02): 
                pass

            # cc=03: Grup 3, control i flags
            elif(cc == 0x03):
                pass

            self.state = FETCH_T0  # Tornar a l'estat inicial després d'executar la instrucció
        
        elif(self.state == EXECUTE_ALU):
            
            if cc == 0x01:  # Grup 1, Aritmètic
                self.reg_sel_a.prepare(A)
                self.reg_sel_b.prepare(MBR)
                if (aaa == 0):  # ORA
                    self.alu_op.prepare(OR)
                    self.n_enable.prepare(1)
                    self.z_enable.prepare(1)
                    
                    self.enable_sel.prepare(A)
                    self.write.prepare(1)

                elif (aaa == 1):  # AND
                    self.alu_op.prepare(AND)
                    self.n_enable.prepare(1)
                    self.z_enable.prepare(1)

                    self.enable_sel.prepare(A)
                    self.write.prepare(1)

                elif (aaa == 2):  # EOR
                    self.alu_op.prepare(XOR)
                    self.n_enable.prepare(1)
                    self.z_enable.prepare(1)

                    self.enable_sel.prepare(A)
                    self.write.prepare(1)

                elif (aaa == 3):  # ADC
                    self.alu_op.prepare(ADD)
                    self.n_enable.prepare(1)
                    self.v_enable.prepare(1)
                    self.z_enable.prepare(1)
                    self.c_enable.prepare(1)

                    self.enable_sel.prepare(A)
                    self.write.prepare(1)

                elif (aaa == 6):  # CMP
                    self.alu_op.prepare(SUB)
                    self.n_enable.prepare(1)
                    self.z_enable.prepare(1)
                    #Aquí no guardem el resultat, només actualitzem els flags

                elif (aaa == 7):  # SBC
                    self.alu_op.prepare(SUB)
                    self.n_enable.prepare(1)
                    self.v_enable.prepare(1)
                    self.z_enable.prepare(1)
                    self.c_enable.prepare(1)

                    self.enable_sel.prepare(A)
                    self.write.prepare(1)

            self.state = FETCH_T0

        elif(self.state == TRANSFER_MBR_TO_A):
            self.reg_sel_a.prepare(MBR)   # Llegim de MBR
            self.enable_sel.prepare(A)    # Escrivim a A
            self.write.prepare(1)         # Permetem l'escriptura
            self.state = FETCH_T0         # Tornem a T0, TODO: potser es podira anar directament a T1 i estalviar-se un cicle

        elif(self.state == ZP_FETCH):
            if cc == 0x01:  # Grup 1, Aritmètic
                if(aaa == 0):
                    self.mm_addr_src.prepare(1)  # Accedim a l'adreça de memòria continguda al mar
                    self.mbr_enable.prepare(1) # I l'escrivim a MBR
                    self.write.prepare(1)
                    self.state = EXECUTE_ALU
      

                elif (aaa == 1):  # AND
                    pass
                elif (aaa == 2):  # EOR
                    pass
                elif (aaa == 3):  # ADC
                    pass
                elif (aaa == 4):  # STA
                    pass
                elif (aaa == 5):  # LDA
                    pass
                elif (aaa == 6):  # CMP
                    pass
                elif (aaa == 7):  # SBC
                    pass