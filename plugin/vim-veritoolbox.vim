"--------------------------------------------------------
"
" Plugin:      https://github.com/dpretet/vim-veritoolbox
" Description: A plugin to work with Verilog & SystemVerilog
" Maintainer:  Damien Pretet https://github.com/dpretet

" Created with the help of Tim's Exploration Journal
" http://candidtim.github.io/vim/2017/08/11/write-vim-plugin-in-python.html
"
"--------------------------------------------------------


"--------------------------------------------------------
" Launch the plugin
"--------------------------------------------------------

" Require Python3
if !has("python3")
    echo "vim has to be compiled with +python3 to run Vim-Veritoolbox plugin"
    finish
endif

" Avoid to load several times the plugin load
if exists('g:veritoolbox_plugin_loaded')
    finish
endif

let g:veritoolbox_plugin_loaded = 1


"--------------------------------------------------------
" Load here the python part of the plugin
"--------------------------------------------------------

" Get current plugin directory
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import veritoolbox
EOF


"--------------------------------------------------------
" Bind the python function to call them from command mode
"--------------------------------------------------------

function! InsertSVInstance()
    let buf = @"
    python3 veritoolbox.insert_sv_instance()
endfunction

command! -nargs=0 InsertSVInstance call InsertSVInstance()

