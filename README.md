# vim-svtb

Vim plugin to work easier with Verilog and systemVerilog. For the moment,
the plugin only add instance of a module.

To use it, go to a module to instanciate and copy the lines specifying the
module name, the parameters and the input/output. Then call `InsertSVInstance`
command. The instance will be inserted after current line.
