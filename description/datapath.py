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
                 ir_data_out:py4hw.Wire,
                 alu_n_in:py4hw.Wire, alu_v_in:py4hw.Wire, alu_z_in:py4hw.Wire, alu_c_in:py4hw.Wire, alu_c_out:py4hw.Wire, 
                 flag_in_sel:py4hw.Wire, 
                 n_enable:py4hw.Wire, v_enable:py4hw.Wire, b_enable:py4hw.Wire, i_enable:py4hw.Wire, z_enable:py4hw.Wire, c_enable:py4hw.Wire):
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
        self.addIn("mm_addr_src",  mm_addr_src)
        self.addIn("flag_in_sel",  flag_in_sel)
        self.addIn("alu_n_in",        alu_n_in)
        self.addIn("alu_v_in",        alu_v_in)
        self.addIn("alu_z_in",        alu_z_in)
        self.addIn("alu_c_in",        alu_c_in)
        self.addIn("n_enable",        n_enable)
        self.addIn("v_enable",        v_enable)
        self.addIn("b_enable",        b_enable)
        self.addIn("i_enable",        i_enable)
        self.addIn("z_enable",        z_enable)
        self.addIn("c_enable",        c_enable)


        self.addOut("output_a",       output_a)
        self.addOut("output_b",       output_b)
        self.addOut("mm_data_out", mm_data_out)
        self.addOut("mm_addr_out", mm_addr_out)
        self.addOut("ir_data_out", ir_data_out)
        self.addOut("alu_c_out",     alu_c_out)


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


        tmp_output = []
        enable     = []
        for i in range(16):
            tmp_output.append(self.wire(f"tmp_output_a_{i}", 8))
            enable.append(self.wire(f"tmp_enable_{i}", 1))
        
        pc = self.wire("pc", 16)
        mar = self.wire("mar", 16)
        one_16 = self.wire("one_16", 16)
        pc_incremented = self.wire("pc_incremented", 16)

        mbr_data =       self.wire("mbr_data", 8)
        pcl_incremented = self.wire("pcl_inc", 8)
        pcl_data =       self.wire("pcl_data", 8)
        pcl_enable =   self.wire("pcl_enable", 1)
        pch_incremented = self.wire("pch_inc", 8)
        pch_data =       self.wire("pch_data", 8)
        pch_enable =   self.wire("pch_enable", 1)
        

        mbr_input = [bus_data,      mm_data_in]
        pcl_input = [bus_data, pcl_incremented] 
        pch_input = [bus_data, pch_incremented]
        mm_addr_input = [pc, mar]
        py4hw.Or2(self, "pcl_or", enable[PCL], pc_inc, pcl_enable)
        py4hw.Or2(self, "pch_or", enable[PCH], pc_inc, pch_enable)



        py4hw.Mux(self, "mbr_input_mux", mbr_src_sel, mbr_input, mbr_data)
        py4hw.Mux(self, "pcl_input_mux", pc_inc, pcl_input, pcl_data)
        py4hw.Mux(self, "pch_input_mux", pc_inc, pch_input, pch_data)

        py4hw.Constant(self, "one_16_const", 1, one_16)
        py4hw.ConcatenateMSBF(self, "pc_concat", [tmp_output[PCH], tmp_output[PCL]], pc)
        py4hw.ConcatenateMSBF(self, "mar_concat", [tmp_output[MARH], tmp_output[MARL]], mar)

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
        py4hw.Reg(self, "MARH", bus_data, tmp_output[MARH], enable[MARH])
        py4hw.Reg(self, "IR",   bus_data, ir_data_out,      enable[IR]  )


        one_1 = self.wire("one_1", 1)
        py4hw.Constant(self, "one_1_const", 1, one_1)


        n_bus = self.wire("n_bus", 1)
        v_bus = self.wire("v_bus", 1)
        b_bus = self.wire("b_bus", 1)
        i_bus = self.wire("i_bus", 1)
        z_bus = self.wire("z_bus", 1)
        c_bus = self.wire("c_bus", 1)

        py4hw.Bit(self, "n_bit_bus", bus_data, 7, n_bus)
        py4hw.Bit(self, "v_bit_bus", bus_data, 6, v_bus)
        py4hw.Bit(self, "b_bit_bus", bus_data, 4, b_bus)
        py4hw.Bit(self, "i_bit_bus", bus_data, 2, i_bus)
        py4hw.Bit(self, "z_bit_bus", bus_data, 1, z_bus)
        py4hw.Bit(self, "c_bit_bus", bus_data, 0, c_bus)
        
        n_input = [alu_n_in, n_bus]
        v_input = [alu_v_in, v_bus]
        z_input = [alu_z_in, z_bus]
        c_input = [alu_c_in, c_bus]


        n_bit = self.wire("n_bit", 1)
        v_bit = self.wire("v_bit", 1)
        z_bit = self.wire("z_bit", 1)
        c_bit = self.wire("c_bit", 1)

        py4hw.Mux(self,"n_mux", flag_in_sel, n_input, n_bit)
        py4hw.Mux(self,"v_mux", flag_in_sel, v_input, v_bit)
        py4hw.Mux(self,"z_mux", flag_in_sel, z_input, z_bit)
        py4hw.Mux(self,"c_mux", flag_in_sel, c_input, c_bit)


        n_out = self.wire("n_out", 1)
        v_out = self.wire("v_out", 1)
        b_out = self.wire("b_out", 1)
        i_out = self.wire("i_out", 1)
        z_out = self.wire("z_out", 1)
        c_out = self.wire("c_out", 1)
        
        py4hw.Reg(self, "N", n_bit, n_out, n_enable)
        py4hw.Reg(self, "V", v_bit, v_out, v_enable)
        py4hw.Reg(self, "B", b_bus, b_out, b_enable)
        py4hw.Reg(self, "I", i_bus, i_out, i_enable)
        py4hw.Reg(self, "Z", z_bit, z_out, z_enable)
        py4hw.Reg(self, "C", c_bit, c_out, c_enable)  

        py4hw.Buf(self, "alu_c_out_buf", c_out, alu_c_out)
        py4hw.ConcatenateMSBF(self, "status_concat", [n_out, v_out, one_1, one_1, b_out, i_out, z_out, c_out], tmp_output[CTL])

        py4hw.Buf(self, "mbr_to_mm", tmp_output[MBR], mm_data_out)
        
        py4hw.Mux(self, "mm_src_mux", mm_addr_src, mm_addr_input, mm_addr_out)

        py4hw.Add(self, "pc_increment", pc, one_16, pc_incremented)
        
        py4hw.Range(self, "pcl_incremented_bits", pc_incremented, 7, 0, pcl_incremented )
        py4hw.Range(self, "pch_incremented_bits", pc_incremented, 15, 8, pch_incremented )

        #py4hw.Reg(self, "CTL", bus_data, tmp_output_a[CTL], enable[CTL])

        # Al tenir doble bus, podem connectar les dues entrades de la ALU alhora 
        py4hw.Mux(self, "sel_mux_a", reg_sel_a, tmp_output, output_a)
        py4hw.Mux(self, "sel_mux_b", reg_sel_b, tmp_output, output_b)
        