" check dependencies
if has('python3')
  command! -nargs=1 Py python3 <args>
  let s:curdir=expand("<sfile>:p:h")
  Py import sys, vim
  Py if not vim.eval("s:curdir") in sys.path:
  \   sys.path.append(vim.eval("s:curdir"))
else
  echo "Error: vim must be compiled with +python3"
  finish
endif

function! schmerlin#Register()
  setlocal omnifunc=schmerlin#Complete
  inoremap <buffer> <Tab> <C-R>=schmerlin#CleverTab()<CR>
endfunction

function! schmerlin#CleverTab()
  " at line start or after a space -> <TAB>
  if strpart(getline('.'), 0, col('.') - 1) =~ '^\s*$'
      return "\<Tab>"
  else
    " omni completion takes priority
    " TODO: use dictionary completion for reserved keywords
    " TODO: check if completion window open and cycle through suggestions
    if &omnifunc != ''
      return "\<C-X>\<C-O>"
    else
      " known-word completion
      return "\<C-N>"
    endif
  endif
endfunction

function! schmerlin#Complete(findstart,base)
  if a:findstart
    " call #1: return col number
    return 0
  else
    " call #2: return list of candidates
    return ["something", "or", "other"]
  endif
endfunction
