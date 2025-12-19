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

class UC(py4hw.Logic):
    def __init__(self, parent, name, 
                 # Entrades     
                 reset:py4hw.Wire,
                 ir_data:py4hw.Wire,
                 

                 # sortides
                 
                 pc_inc:py4hw.Wire, ld_pc2mar:py4hw.Wire,

                 enable_sel:py4hw.Wire, write:py4hw.Wire,
                 
                 
                 reg_sel_a:py4hw.Wire,
                 reg_sel_b:py4hw.Wire,
                 
                 mbr_src_sel:py4hw.Wire,  # 0=Bus, 1=Memòria 
                 mm_addr_src:py4hw.Wire,  # 0=PC, 1=MAR
                 
                 # Control  ALU [...]
                 alu_op:py4hw.Wire, 
                 flags_enable:py4hw.Wire
                 ):
        super().__init__(parent, name)

        self.reset =       self.addIn("reset",  reset)
        
        self.pc_inc =      self.addOut("pc_inc", pc_inc)
        self.ld_pc2mar =   self.addOut("ld_pc2mar", ld_pc2mar)
        self.enable_sel =  self.addOut("enable_sel", enable_sel)
        self.write =       self.addOut("write", write)
        self.mbr_src_sel = self.addOut("mbr_src_sel",  mbr_src_sel)
        self.mm_addr_src = self.addOut("mm_addr_src",  mm_addr_src)


        
        self.state = 0
    def default_values(self):
        for i in self.outPorts:
            i.wire.put(0)

    def clock(self):

        if(self.state == 0 or self.reset.get() == 1):
            self.default_values()
            #self.ld_pc2mar.prepare(1)    # MAR <-[PC]
            self.mm_addr_src.prepare(0)

            self.state = 1

        elif(self.state == 1 and self.reset.get() == 0):
            self.default_values()
            """         
            self.pc_inc.prepare(1)       # PC <-[PC] + 1
            self.mbr_src_sel.prepare(1)  # MBR <-[PC]
            self.enable_sel.prepare(MBR)
            """
            self.pc_inc.prepare(1)       # PC <-[PC] + 1
            self.enable_sel.prepare(IR)  
            self.write.prepare(1)

            self.state = 2