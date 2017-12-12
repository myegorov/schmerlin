if exists("g:loaded_schmerlin")
  finish
endif
let g:loaded_schmerlin = 1

" Activate schmerlin on current buffer
call schmerlin#Register()
