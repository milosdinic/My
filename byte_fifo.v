module byte_fifo
  #(parameter DATA_OUT_BYTE_W = 16,
    parameter DATA_IN_BYTES_W = 16,
    parameter FIFO_BYTE_W = 32,    
    parameter NUM_BYTES_IN_W = 
    (DATA_IN_BYTES_W>511) ? 10 :
    (DATA_IN_BYTES_W>255) ? 9 :
    (DATA_IN_BYTES_W>127) ? 8 :
    (DATA_IN_BYTES_W>63)  ? 7 :
    (DATA_IN_BYTES_W>31)  ? 6 :
    (DATA_IN_BYTES_W>15)  ? 5 :
    (DATA_IN_BYTES_W>7)   ? 4 :
    (DATA_IN_BYTES_W>3)   ? 3 :
    (DATA_IN_BYTES_W>1)   ? 2 : 1,
    parameter NUM_BYTES_TAKEN_W =
    (DATA_OUT_BYTE_W>511) ? 10 :
    (DATA_OUT_BYTE_W>255) ? 9 :
    (DATA_OUT_BYTE_W>127) ? 8 :
    (DATA_OUT_BYTE_W>63)  ? 7 :
    (DATA_OUT_BYTE_W>31)  ? 6 :
    (DATA_OUT_BYTE_W>15)  ? 5 :
    (DATA_OUT_BYTE_W>7)   ? 4 :
    (DATA_OUT_BYTE_W>3)   ? 3 :
    (DATA_OUT_BYTE_W>1)   ? 2 : 1,
    parameter ADD_W = 
    (FIFO_BYTE_W>511) ? 10 :
    (FIFO_BYTE_W>255) ? 9 :
    (FIFO_BYTE_W>127) ? 8 :
    (FIFO_BYTE_W>63)  ? 7 :
    (FIFO_BYTE_W>31)  ? 6 :
    (FIFO_BYTE_W>15)  ? 5 :
    (FIFO_BYTE_W>7)   ? 4 :
    (FIFO_BYTE_W>3)   ? 3 :
    (FIFO_BYTE_W>1)   ? 2 : 1
    ) 
   (
    input                     clk,
    input                     rst_n,
    input                     sync_rst,
    // Init
    // General IN/OUT
    input                            input_data_valid,
    input [NUM_BYTES_TAKEN_W-1:0]    num_bytes_taken_from_fifo,
    input [(DATA_IN_BYTES_W*8)-1:0]  input_data,
    input [NUM_BYTES_IN_W-1:0]       num_bytes_in,
    output                           data_valid,
    output reg [ADD_W-1:0]           num_bytes,
    output [(DATA_OUT_BYTE_W*8)-1:0] data
    );

   //----------------------------------

   reg [(FIFO_BYTE_W*8)-1:0]      data_fifo;   
   wire [ADD_W-1:0]               din_shl;
   reg [ADD_W-1:0]                num_bytes_i;
   wire [(FIFO_BYTE_W*8)-1:0]     data_shl;
   wire [(DATA_IN_BYTES_W*8)-1:0] input_data_mask;
   reg [(FIFO_BYTE_W*8)-1:0]      data_fifo_in;
   wire [(FIFO_BYTE_W*8)-1:0]     data_fifo_shr;
   
   //--------------------------
   //     NUM_BYTES     
   //--------------------------

   always @(*)
     if (sync_rst) 
       num_bytes_i = {ADD_W{1'b0}};
     else 
       num_bytes_i = (num_bytes_in & {NUM_BYTES_IN_W{input_data_valid}}) - (num_bytes_taken_from_fifo & {NUM_BYTES_TAKEN_W{data_valid}}) + num_bytes; 
   
   always @(posedge clk or negedge rst_n)
     if (~rst_n)
       num_bytes <= 'b0;
     else if (input_data_valid | data_valid | sync_rst)            
       num_bytes <= #(0.1) num_bytes_i ;
   
   
   //----------------------------------
   //     Shift Data In Left     
   //----------------------------------
   
   assign din_shl         = (num_bytes - ({1'b0,num_bytes_taken_from_fifo} & {NUM_BYTES_TAKEN_W{data_valid}}));
   assign input_data_mask = input_data_valid ? {(DATA_IN_BYTES_W*8){1'b1}} >> ((DATA_IN_BYTES_W-num_bytes_in)*8) : {FIFO_BYTE_W*8{1'b0}};
   assign data_shl        = (input_data & input_data_mask) << (din_shl*8);

   //--------------------------
   //     DATA_FIFO     
   //--------------------------

   always @(*)
    if (sync_rst) 
      data_fifo_in = {(FIFO_BYTE_W*8){1'b0}};
    else 
      data_fifo_in = (data_fifo_shr | data_shl); //input_data_valid | data_valid


   always @(posedge clk or negedge rst_n)
     if (~rst_n)
       data_fifo <= 'b0;
     else if (input_data_valid | data_valid | sync_rst)            
       data_fifo <= #(0.1) data_fifo_in ;


   //--------------------------
   //     DATA_OUT     
   //--------------------------

   assign data = data_fifo[(DATA_OUT_BYTE_W*8)-1:0];

   assign data_valid = (num_bytes_taken_from_fifo=={NUM_BYTES_TAKEN_W{1'b0}}) ? 1'b0: (num_bytes>=num_bytes_taken_from_fifo & num_bytes!={ADD_W{1'b0}});

   //--------------------------
   //     Shift FIFO Right     
   //--------------------------
   
   assign data_fifo_shr =   ~data_valid ? data_fifo : data_fifo >> (num_bytes_taken_from_fifo*8);
   
endmodule
