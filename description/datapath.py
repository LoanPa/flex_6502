import py4hw

class Datapath(py4hw.Logic):
    def __init__(self, parent, name,
                 bus_data:py4hw.Wire,
                 pc_inc:py4hw.Wire,
                 enable_sel:py4hw.Wire, write:py4hw.Wire,
                 reg_sel_a:py4hw.Wire, reg_sel_b:py4hw.Wire,
                 output_a:py4hw.Wire, output_b:py4hw.Wire,
                 mbr_src_sel:py4hw.Wire,
                 mm_data_in:py4hw.Wire, mm_data_out:py4hw.Wire,
                 mm_addr_src:py4hw.Wire, mm_addr_out:py4hw.Wire,
                 marh_enable:py4hw.Wire):
        super().__init__(parent, name)
        # Només hi ha una entrada al bus, ja que no hi ha massa oportunitats per a fer-ne servir dues alhora.
        self.addIn("bus_data",        bus_data)
        self.addIn("pc_inc",            pc_inc)
        self.addIn("enable_sel",    enable_sel)
        self.addIn("write",              write)
        self.addIn("reg_sel_a",      reg_sel_a)
        self.addIn("reg_sel_b",      reg_sel_b)
        self.addIn("mbr_src_sel",  mbr_src_sel)
        self.addIn("mm_data_in",    mm_data_in)
        self.addIn("marh_enable",  marh_enable)
        self.addIn("mm_addr_src", mm_addr_src)

        self.addOut("output_a",       output_a)
        self.addOut("output_b",       output_b)
        self.addOut("mm_data_out", mm_data_out)
        self.addOut("mm_addr_out", mm_addr_out)

        # Registres
        A    = 0
        X    = 1
        Y    = 2
        SP   = 3
        MBR  = 4
        PCL  = 5
        PCH  = 6
        MARL = 7

        tmp_output = []
        enable     = []
        for i in range(8):
            tmp_output.append(self.wire(f"tmp_output_a_{i}", 8))
            enable.append(self.wire(f"tmp_enable_{i}", 1))
        
        pc = self.wire("pc", 16)
        mar = self.wire("mar", 16)
        one = self.wire("one", 16)
        pc_incremented = self.wire("pc_incremented", 16)

        mbr_data =       self.wire("mbr_data", 8)
        pcl_incremented = self.wire("pcl_inc", 8)
        pcl_data =       self.wire("pcl_data", 8)
        pcl_enable =   self.wire("pcl_enable", 1)
        pch_incremented = self.wire("pch_inc", 8)
        pch_data =       self.wire("pch_data", 8)
        pch_enable =   self.wire("pch_enable", 1)
        marh_data =    self.wire("marh_data",  8)
        

        mbr_input = [bus_data,      mm_data_in]
        pcl_input = [bus_data, pcl_incremented] 
        pch_input = [bus_data, pch_incremented] 
        pch_input = [bus_data, pch_incremented] 
        mm_addr_input = [pc, mar]
        py4hw.Or2(self, "pcl_or", enable[PCL], pc_inc, pcl_enable)
        py4hw.Or2(self, "pch_or", enable[PCH], pc_inc, pch_enable)



        py4hw.Mux(self, "mbr_input_mux", mbr_src_sel, mbr_input, mbr_data)
        py4hw.Mux(self, "pcl_input_mux", pc_inc, pcl_input, pcl_data)
        py4hw.Mux(self, "pch_input_mux", pc_inc, pch_input, pch_data)

        py4hw.Constant(self, "one_const", 1, one)
        py4hw.ConcatenateMSBF(self, "pc_concat", [tmp_output[PCH], tmp_output[PCL]], pc)
        py4hw.ConcatenateMSBF(self, "mar_concat", [tmp_output[MARL], marh_data], mar)

        py4hw.Demux(self, "enable_demux", write, enable_sel, enable)
        #assert bus_data.getWidth() == 8
        py4hw.Reg(self, "A",    bus_data, tmp_output[A],    enable[A]   )
        py4hw.Reg(self, "X",    bus_data, tmp_output[X],    enable[X]   )
        py4hw.Reg(self, "Y",    bus_data, tmp_output[Y],    enable[Y]   )
        py4hw.Reg(self, "SP",   bus_data, tmp_output[SP],   enable[SP]  )
        py4hw.Reg(self, "MBR",  mbr_data, tmp_output[MBR],  enable[MBR] )
        py4hw.Reg(self, "PCL",  pcl_data, tmp_output[PCL],  pcl_enable  ) 
        py4hw.Reg(self, "PCH",  pch_data, tmp_output[PCH],  pch_enable  )
        py4hw.Reg(self, "MARL", bus_data, tmp_output[MARL], enable[MARL])
        py4hw.Reg(self, "MARH", bus_data, marh_data,        marh_enable )
        
        py4hw.Buf(self, "mbr_to_mm", tmp_output[MBR], mm_data_out)
        
        py4hw.Mux(self, "mm_src_mux", mm_addr_src, mm_addr_input, mm_addr_out )

        py4hw.Add(self, "pc_increment", pc, one, pc_incremented)
        
        py4hw.Range(self, "pcl_incremented_bits", pc_incremented, 7, 0, pcl_incremented )
        py4hw.Range(self, "pch_incremented_bits", pc_incremented, 15, 8, pch_incremented )

        #py4hw.Reg(self, "CTL", bus_data, tmp_output_a[CTL], enable[CTL])

        # Al tenir doble bus, podem connectar les dues entrades de la ALU alhora 
        py4hw.Mux(self, "sel_mux_a", reg_sel_a, tmp_output, output_a)
        py4hw.Mux(self, "sel_mux_b", reg_sel_b, tmp_output, output_b)
        