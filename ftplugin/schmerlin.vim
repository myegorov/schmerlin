if exists("g:loaded_schmerlin")
  finish
endif
let g:loaded_schmerlin = 1

" Activate schmerlin on current buffer
try
  call schmerlin#Register()
catch /.*/
  echohl ErrorMsg | echomsg v:exception | echohl None
  finish
finally
  unlet g:loaded_schmerlin
endtry
