module bit_fifo
  #(
    parameter FIFO_IF_W = 48,
    parameter FIFO_DEPTH = 4,
    parameter FIFO_W = FIFO_IF_W * FIFO_DEPTH,
    parameter ADD_W = 
    (FIFO_W>127) ? 8 :
    (FIFO_W>63)  ? 7 :
    (FIFO_W>31)  ? 6 :
    (FIFO_W>15)  ? 5 :
    (FIFO_W>7)   ? 4 :
    (FIFO_W>3)   ? 3 :
    (FIFO_W>1)   ? 2 : 1,
    parameter IF_ADD_W = 
    (FIFO_IF_W>31)  ? 6 :
    (FIFO_IF_W>15)  ? 5 :
    (FIFO_IF_W>7)   ? 4 :
    (FIFO_IF_W>3)   ? 3 :
    (FIFO_IF_W>1)   ? 2 : 1    
    ) 
   (
    input                   clk,
    input                   rst_n,
    // Init                 
    input                   data_fifo_init_en,
    input [FIFO_W-1:0]      data_fifo_init_val,
    output [FIFO_W-1:0]     data_fifo,
    input                   num_bits_init_en,
    input [ADD_W-1:0]       num_bits_init_val,
    output [ADD_W-1:0]      num_bits,
    // General IN/OUT       
    input [FIFO_IF_W-1:0]   data_in,
    input [IF_ADD_W-1:0]    data_in_num_bits,
    input                   data_in_wr,
    input [IF_ADD_W-1:0]    data_out_num_bits,
    input                   data_out_rd,
    output [FIFO_IF_W-1:0]  data_out,
    output                  wr_error,
    output                  rd_error
    );

   //----------------------------------

   wire [FIFO_W-1:0]        data_fifo_shr;
   reg [FIFO_W-1:0]         data_fifo_in;
   wire [FIFO_W-1:0]        data_shl;
   wire [IF_ADD_W-1:0]      rd_num_bits;
   wire [IF_ADD_W-1:0]      wr_num_bits;
   reg [ADD_W-1:0]          num_bits_in;
   wire [ADD_W-1:0]         din_shl;
   wire [(2*FIFO_IF_W)-1:0] data_inout_mask;
   wire [(2*FIFO_IF_W)-1:0] data_out_mask_pre;
   wire [FIFO_IF_W-1:0]     data_out_mask;
   wire [(2*FIFO_IF_W)-1:0] data_in_mask_pre;
   wire [FIFO_IF_W-1:0]     data_in_mask;

   wire                    data_wr_legal;
   wire                    data_rd_legal;
   //--------------------------
   //---     NUM_BITS     -----
   //--------------------------

   assign din_shl = (num_bits - rd_num_bits); 

   always @(*)
     if (num_bits_init_en) num_bits_in = num_bits_init_val;
     else num_bits_in = din_shl + wr_num_bits;

   m_enffr #(.w(ADD_W), .init_val(0)) i_num_bits
     (
      .clk(clk),
      .reset_n(rst_n),
      .in(num_bits_in),
      .en(data_wr_legal | data_rd_legal | num_bits_init_en),
      .out(num_bits));
   
   //-------------------------------
   //---     Data Out Mask     -----
   //-------------------------------

   assign data_inout_mask   = {{FIFO_IF_W{1'b0}},{FIFO_IF_W{1'b1}}};
   assign data_out_mask_pre = data_inout_mask << rd_num_bits;
   assign data_out_mask     = data_out_mask_pre[(2*FIFO_IF_W)-1:FIFO_IF_W];
   
   //---------------------------
   //---     DATA_FIFO     -----
   //---------------------------

   assign data_wr_legal = data_in_wr & ((num_bits+data_in_num_bits)<=FIFO_W);
   assign wr_error      = data_in_wr & (~data_wr_legal);
   assign data_rd_legal = ((num_bits>=data_out_num_bits) & data_out_rd);
   assign rd_error      = data_out_rd & (~data_rd_legal);

   always @(*)
     if (data_fifo_init_en) data_fifo_in = data_fifo_init_val;
     else data_fifo_in = (data_fifo_shr | data_shl); //data_wr_legal | data_rd_legal 

   m_enffr #(.w(FIFO_W), .init_val(0)) i_data_fifo
     (
      .clk(clk),
      .reset_n(rst_n),
      .in(data_fifo_in),
      .en(data_wr_legal | data_rd_legal | data_fifo_init_en),
      .out(data_fifo));

   //--------------------------
   //---     DATA_OUT     -----
   //--------------------------

   assign data_out = data_fifo[FIFO_IF_W-1:0] & data_out_mask;

   //--------------------------
   //--- Mask rd_num_bits -----
   //--------------------------

   assign rd_num_bits = data_out_num_bits & {IF_ADD_W{data_rd_legal}};

   //--------------------------
   //--- Mask wr_num_bits -----
   //--------------------------

   assign wr_num_bits = data_in_num_bits & {IF_ADD_W{data_wr_legal}};   

   //----------------------------------
   //---     Shift FIFO Right     -----
   //----------------------------------

   assign data_fifo_shr = data_fifo >> rd_num_bits;

   //------------------------------------
   //---     Shift Data In Left     -----
   //------------------------------------

   assign data_in_mask_pre = data_inout_mask << wr_num_bits;
   assign data_in_mask     = data_in_mask_pre[(2*FIFO_IF_W)-1:FIFO_IF_W];   
   assign data_shl     = {{(FIFO_W-FIFO_IF_W){1'b0}}, (data_in_mask&data_in)} << din_shl;


endmodule // bit_fifo

