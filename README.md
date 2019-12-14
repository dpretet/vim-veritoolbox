# vim-svtb

Vim plugin to work easier with Verilog and systemVerilog. For the moment,
the plugin only add instance of a module.

To use it, go to a module to instanciate and copy the lines specifying the
module name, the parameters and the input/output. Then call `InsertSVInstance`
command. The instance will be inserted after current line.

# Installation

Use [Vim-Plug](https://github.com/junegunn/vim-plug) or any other plugin manager to install it.

```vim
Plug 'damofthemoon/vim-svtb'
```

vim-svtb is written in python. Please be sure to use Vim/NVim with python support.


# License

This plugin is under MIT license. Do whatever you want with it, and don't hesitate to fork it and
contribute!
