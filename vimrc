set ru nu cindent smartindent autoindent ts=4 sts=4 sw=4 hls ar bs=2 mouse=a

syntax on

nmap <C-A> ggVG
vmap <C-C> "+y

filetype plugin indent on

map <F9> :!g++ % -o %< -g -Wall -Wextra -Wconversion -std=c++11 && size %< <CR>
map <C-F9> :!g++ % -o %< -g -O2 -std=c++11 && size %< <CR>
map <F8> :!time ./%< < %<.in <CR>
map <F5> :!time ./%< <CR>
map <F3> :vnew %<.in <CR>
map <F4> :!gedit % <CR>
map <F10> :!sudo python % <CR>
