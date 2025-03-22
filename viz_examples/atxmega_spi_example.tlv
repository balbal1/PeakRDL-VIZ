\m4_TLV_version 1d: tl-x.org
\SV

`include "sp_default.vh" //_\SV

// -----------------
// registers package
// -----------------
package atxmega_spi_pkg;

    localparam ATXMEGA_SPI_DATA_WIDTH = 8;
    localparam ATXMEGA_SPI_MIN_ADDR_WIDTH = 1;

    typedef struct {
        logic next;
        logic we;
    } atxmega_spi__CTRL__MASTER__in_t;

    typedef struct {
        atxmega_spi__CTRL__MASTER__in_t MASTER;
    } atxmega_spi__CTRL__in_t;

    typedef struct {
        atxmega_spi__CTRL__in_t CTRL;
    } atxmega_spi__in_t;

    typedef struct {
        logic [1:0] value;
    } atxmega_spi__CTRL__PRESCALER__out_t;

    typedef struct {
        logic [1:0] value;
    } atxmega_spi__CTRL__MODE__out_t;

    typedef struct {
        logic value;
    } atxmega_spi__CTRL__MASTER__out_t;

    typedef struct {
        logic value;
    } atxmega_spi__CTRL__DORD__out_t;

    typedef struct {
        logic value;
    } atxmega_spi__CTRL__ENABLE__out_t;

    typedef struct {
        logic value;
    } atxmega_spi__CTRL__CLK2X__out_t;

    typedef struct {
        atxmega_spi__CTRL__PRESCALER__out_t PRESCALER;
        atxmega_spi__CTRL__MODE__out_t MODE;
        atxmega_spi__CTRL__MASTER__out_t MASTER;
        atxmega_spi__CTRL__DORD__out_t DORD;
        atxmega_spi__CTRL__ENABLE__out_t ENABLE;
        atxmega_spi__CTRL__CLK2X__out_t CLK2X;
    } atxmega_spi__CTRL__out_t;

    typedef struct {
        atxmega_spi__CTRL__out_t CTRL;
    } atxmega_spi__out_t;
endpackage

// ---
// VIZ
// ---
\TLV ff(/_ff, _register, _field, #_index, #_x)
   /_ff
      \viz_js
         box: {width: 50, height: 40, strokeWidth: 1},
         init() {
            let ret = {}
            ret.bit = new fabric.Text("", {
               left: 18, top: 7,
               fontSize: 22, fontFamily: "Courier New",
            })
            ret.label = new fabric.Text("", {
               left: 0, top: -15,
               fontSize: 6, fontFamily: "Courier New",
            })
            return ret
         },
         render() {
            let objs = this.getObjects()
            let field = this.sigVal(`atxmega_spi.field_storage.${_register}.${_field}.value`)
            objs.bit.set({text: field.getValue()[#_index]})
            objs.label.set({text: `${_field}[${#_index}]`})
            return []
         },
         where: {left: #_x * 50, top: 0}

// ---
// Top
// ---
\SV
   m4_makerchip_module
   atxmega_spi_pkg::atxmega_spi__in_t hwif_in;
   atxmega_spi_pkg::atxmega_spi__out_t hwif_out;

\TLV
   
   $clk = *clk;
   $reset = *reset;
   
   atxmega_spi atxmega_spi($clk, $reset, $s_apb_psel, $s_apb_penable, $s_apb_pwrite, $s_apb_paddr, $s_apb_pwdata, $s_apb_pready, $s_apb_prdata, $s_apb_pslverr, *hwif_in, *hwif_out);
   
   m4+ff(/prescaler0, "CTRL", "PRESCALER", 0, 0)
   m4+ff(/prescaler1, "CTRL", "PRESCALER", 1, 1)
   m4+ff(/mode0, "CTRL", "MODE", 0, 2)
   m4+ff(/mode1, "CTRL", "MODE", 1, 3)
   m4+ff(/master, "CTRL", "MASTER", 0, 4)
   m4+ff(/dord, "CTRL", "DORD", 0, 5)
   m4+ff(/enable, "CTRL", "ENABLE", 0, 6)
   m4+ff(/clkx2, "CTRL", "CLK2X", 0, 7)

   
   *passed = *cyc_cnt > 20;
   *failed = 1'b0;

\SV
endmodule

// ------
// Design
// ------
module atxmega_spi (
        input wire clk,
        input wire rst,

        input wire s_apb_psel,
        input wire s_apb_penable,
        input wire s_apb_pwrite,
        input wire [0:0] s_apb_paddr,
        input wire [7:0] s_apb_pwdata,
        output logic s_apb_pready,
        output logic [7:0] s_apb_prdata,
        output logic s_apb_pslverr,

        input atxmega_spi_pkg::atxmega_spi__in_t hwif_in,
        output atxmega_spi_pkg::atxmega_spi__out_t hwif_out
    );

    //--------------------------------------------------------------------------
    // CPU Bus interface logic
    //--------------------------------------------------------------------------
    logic cpuif_req;
    logic cpuif_req_is_wr;
    logic [0:0] cpuif_addr;
    logic [7:0] cpuif_wr_data;
    logic [7:0] cpuif_wr_biten;
    logic cpuif_req_stall_wr;
    logic cpuif_req_stall_rd;

    logic cpuif_rd_ack;
    logic cpuif_rd_err;
    logic [7:0] cpuif_rd_data;

    logic cpuif_wr_ack;
    logic cpuif_wr_err;

    // Request
    logic is_active;
    always_ff @(posedge clk) begin
        if(rst) begin
            is_active <= '0;
            cpuif_req <= '0;
            cpuif_req_is_wr <= '0;
            cpuif_addr <= '0;
            cpuif_wr_data <= '0;
        end else begin
            if(~is_active) begin
                if(s_apb_psel) begin
                    is_active <= '1;
                    cpuif_req <= '1;
                    cpuif_req_is_wr <= s_apb_pwrite;
                    cpuif_addr <= s_apb_paddr[0:0];
                    cpuif_wr_data <= s_apb_pwdata;
                end
            end else begin
                cpuif_req <= '0;
                if(cpuif_rd_ack || cpuif_wr_ack) begin
                    is_active <= '0;
                end
            end
        end
    end
    assign cpuif_wr_biten = '1;

    // Response
    assign s_apb_pready = cpuif_rd_ack | cpuif_wr_ack;
    assign s_apb_prdata = cpuif_rd_data;
    assign s_apb_pslverr = cpuif_rd_err | cpuif_wr_err;

    logic cpuif_req_masked;

    // Read & write latencies are balanced. Stalls not required
    assign cpuif_req_stall_rd = '0;
    assign cpuif_req_stall_wr = '0;
    assign cpuif_req_masked = cpuif_req
                            & !(!cpuif_req_is_wr & cpuif_req_stall_rd)
                            & !(cpuif_req_is_wr & cpuif_req_stall_wr);

    //--------------------------------------------------------------------------
    // Address Decode
    //--------------------------------------------------------------------------
    typedef struct {
        logic CTRL;
    } decoded_reg_strb_t;
    decoded_reg_strb_t decoded_reg_strb;
    logic decoded_req;
    logic decoded_req_is_wr;
    logic [7:0] decoded_wr_data;
    logic [7:0] decoded_wr_biten;

    always_comb begin
        decoded_reg_strb.CTRL = cpuif_req_masked & (cpuif_addr == 1'h0);
    end

    // Pass down signals to next stage
    assign decoded_req = cpuif_req_masked;
    assign decoded_req_is_wr = cpuif_req_is_wr;
    assign decoded_wr_data = cpuif_wr_data;
    assign decoded_wr_biten = cpuif_wr_biten;

    //--------------------------------------------------------------------------
    // Field logic
    //--------------------------------------------------------------------------
    typedef struct {
        struct {
            struct {
                logic [1:0] next;
                logic load_next;
            } PRESCALER;
            struct {
                logic [1:0] next;
                logic load_next;
            } MODE;
            struct {
                logic next;
                logic load_next;
            } MASTER;
            struct {
                logic next;
                logic load_next;
            } DORD;
            struct {
                logic next;
                logic load_next;
            } ENABLE;
            struct {
                logic next;
                logic load_next;
            } CLK2X;
        } CTRL;
    } field_combo_t;
    field_combo_t field_combo;

    typedef struct {
        struct {
            struct {
                logic [1:0] value;
            } PRESCALER;
            struct {
                logic [1:0] value;
            } MODE;
            struct {
                logic value;
            } MASTER;
            struct {
                logic value;
            } DORD;
            struct {
                logic value;
            } ENABLE;
            struct {
                logic value;
            } CLK2X;
        } CTRL;
    } field_storage_t;
    field_storage_t field_storage;

    // Field: atxmega_spi.CTRL.PRESCALER
    always_comb begin
        automatic logic [1:0] next_c;
        automatic logic load_next_c;
        next_c = field_storage.CTRL.PRESCALER.value;
        load_next_c = '0;
        if(decoded_reg_strb.CTRL && decoded_req_is_wr) begin // SW write
            next_c = (field_storage.CTRL.PRESCALER.value & ~decoded_wr_biten[1:0]) | (decoded_wr_data[1:0] & decoded_wr_biten[1:0]);
            load_next_c = '1;
        end
        field_combo.CTRL.PRESCALER.next = next_c;
        field_combo.CTRL.PRESCALER.load_next = load_next_c;
    end
    always_ff @(posedge clk) begin
        if(rst) begin
            field_storage.CTRL.PRESCALER.value <= 2'h0;
        end else begin
            if(field_combo.CTRL.PRESCALER.load_next) begin
                field_storage.CTRL.PRESCALER.value <= field_combo.CTRL.PRESCALER.next;
            end
        end
    end
    assign hwif_out.CTRL.PRESCALER.value = field_storage.CTRL.PRESCALER.value;
    // Field: atxmega_spi.CTRL.MODE
    always_comb begin
        automatic logic [1:0] next_c;
        automatic logic load_next_c;
        next_c = field_storage.CTRL.MODE.value;
        load_next_c = '0;
        if(decoded_reg_strb.CTRL && decoded_req_is_wr) begin // SW write
            next_c = (field_storage.CTRL.MODE.value & ~decoded_wr_biten[3:2]) | (decoded_wr_data[3:2] & decoded_wr_biten[3:2]);
            load_next_c = '1;
        end
        field_combo.CTRL.MODE.next = next_c;
        field_combo.CTRL.MODE.load_next = load_next_c;
    end
    always_ff @(posedge clk) begin
        if(rst) begin
            field_storage.CTRL.MODE.value <= 2'h0;
        end else begin
            if(field_combo.CTRL.MODE.load_next) begin
                field_storage.CTRL.MODE.value <= field_combo.CTRL.MODE.next;
            end
        end
    end
    assign hwif_out.CTRL.MODE.value = field_storage.CTRL.MODE.value;
    // Field: atxmega_spi.CTRL.MASTER
    always_comb begin
        automatic logic [0:0] next_c;
        automatic logic load_next_c;
        next_c = field_storage.CTRL.MASTER.value;
        load_next_c = '0;
        if(decoded_reg_strb.CTRL && decoded_req_is_wr) begin // SW write
            next_c = (field_storage.CTRL.MASTER.value & ~decoded_wr_biten[4:4]) | (decoded_wr_data[4:4] & decoded_wr_biten[4:4]);
            load_next_c = '1;
        end else if(hwif_in.CTRL.MASTER.we) begin // HW Write - we
            next_c = hwif_in.CTRL.MASTER.next;
            load_next_c = '1;
        end
        field_combo.CTRL.MASTER.next = next_c;
        field_combo.CTRL.MASTER.load_next = load_next_c;
    end
    always_ff @(posedge clk) begin
        if(rst) begin
            field_storage.CTRL.MASTER.value <= 1'h0;
        end else begin
            if(field_combo.CTRL.MASTER.load_next) begin
                field_storage.CTRL.MASTER.value <= field_combo.CTRL.MASTER.next;
            end
        end
    end
    assign hwif_out.CTRL.MASTER.value = field_storage.CTRL.MASTER.value;
    // Field: atxmega_spi.CTRL.DORD
    always_comb begin
        automatic logic [0:0] next_c;
        automatic logic load_next_c;
        next_c = field_storage.CTRL.DORD.value;
        load_next_c = '0;
        if(decoded_reg_strb.CTRL && decoded_req_is_wr) begin // SW write
            next_c = (field_storage.CTRL.DORD.value & ~decoded_wr_biten[5:5]) | (decoded_wr_data[5:5] & decoded_wr_biten[5:5]);
            load_next_c = '1;
        end
        field_combo.CTRL.DORD.next = next_c;
        field_combo.CTRL.DORD.load_next = load_next_c;
    end
    always_ff @(posedge clk) begin
        if(rst) begin
            field_storage.CTRL.DORD.value <= 1'h0;
        end else begin
            if(field_combo.CTRL.DORD.load_next) begin
                field_storage.CTRL.DORD.value <= field_combo.CTRL.DORD.next;
            end
        end
    end
    assign hwif_out.CTRL.DORD.value = field_storage.CTRL.DORD.value;
    // Field: atxmega_spi.CTRL.ENABLE
    always_comb begin
        automatic logic [0:0] next_c;
        automatic logic load_next_c;
        next_c = field_storage.CTRL.ENABLE.value;
        load_next_c = '0;
        if(decoded_reg_strb.CTRL && decoded_req_is_wr) begin // SW write
            next_c = (field_storage.CTRL.ENABLE.value & ~decoded_wr_biten[6:6]) | (decoded_wr_data[6:6] & decoded_wr_biten[6:6]);
            load_next_c = '1;
        end
        field_combo.CTRL.ENABLE.next = next_c;
        field_combo.CTRL.ENABLE.load_next = load_next_c;
    end
    always_ff @(posedge clk) begin
        if(rst) begin
            field_storage.CTRL.ENABLE.value <= 1'h0;
        end else begin
            if(field_combo.CTRL.ENABLE.load_next) begin
                field_storage.CTRL.ENABLE.value <= field_combo.CTRL.ENABLE.next;
            end
        end
    end
    assign hwif_out.CTRL.ENABLE.value = field_storage.CTRL.ENABLE.value;
    // Field: atxmega_spi.CTRL.CLK2X
    always_comb begin
        automatic logic [0:0] next_c;
        automatic logic load_next_c;
        next_c = field_storage.CTRL.CLK2X.value;
        load_next_c = '0;
        if(decoded_reg_strb.CTRL && decoded_req_is_wr) begin // SW write
            next_c = (field_storage.CTRL.CLK2X.value & ~decoded_wr_biten[7:7]) | (decoded_wr_data[7:7] & decoded_wr_biten[7:7]);
            load_next_c = '1;
        end
        field_combo.CTRL.CLK2X.next = next_c;
        field_combo.CTRL.CLK2X.load_next = load_next_c;
    end
    always_ff @(posedge clk) begin
        if(rst) begin
            field_storage.CTRL.CLK2X.value <= 1'h0;
        end else begin
            if(field_combo.CTRL.CLK2X.load_next) begin
                field_storage.CTRL.CLK2X.value <= field_combo.CTRL.CLK2X.next;
            end
        end
    end
    assign hwif_out.CTRL.CLK2X.value = field_storage.CTRL.CLK2X.value;

    //--------------------------------------------------------------------------
    // Write response
    //--------------------------------------------------------------------------
    assign cpuif_wr_ack = decoded_req & decoded_req_is_wr;
    // Writes are always granted with no error response
    assign cpuif_wr_err = '0;

    //--------------------------------------------------------------------------
    // Readback
    //--------------------------------------------------------------------------

    logic readback_err;
    logic readback_done;
    logic [7:0] readback_data;

    // Assign readback values to a flattened array
    logic [7:0] readback_array[1];
    assign readback_array[0][1:0] = (decoded_reg_strb.CTRL && !decoded_req_is_wr) ? field_storage.CTRL.PRESCALER.value : '0;
    assign readback_array[0][3:2] = (decoded_reg_strb.CTRL && !decoded_req_is_wr) ? field_storage.CTRL.MODE.value : '0;
    assign readback_array[0][4:4] = (decoded_reg_strb.CTRL && !decoded_req_is_wr) ? field_storage.CTRL.MASTER.value : '0;
    assign readback_array[0][5:5] = (decoded_reg_strb.CTRL && !decoded_req_is_wr) ? field_storage.CTRL.DORD.value : '0;
    assign readback_array[0][6:6] = (decoded_reg_strb.CTRL && !decoded_req_is_wr) ? field_storage.CTRL.ENABLE.value : '0;
    assign readback_array[0][7:7] = (decoded_reg_strb.CTRL && !decoded_req_is_wr) ? field_storage.CTRL.CLK2X.value : '0;

    // Reduce the array
    always_comb begin
        automatic logic [7:0] readback_data_var;
        readback_done = decoded_req & ~decoded_req_is_wr;
        readback_err = '0;
        readback_data_var = '0;
        for(int i=0; i<1; i++) readback_data_var |= readback_array[i];
        readback_data = readback_data_var;
    end

    assign cpuif_rd_ack = readback_done;
    assign cpuif_rd_data = readback_data;
    assign cpuif_rd_err = readback_err;
endmodule
