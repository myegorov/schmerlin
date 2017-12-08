" check dependencies
if has('python3')
  command! -nargs=1 Py python3 <args>
  let s:curdir=expand("<sfile>:p:h")
  Py import sys, vim
  Py if not vim.eval("s:curdir") in sys.path:
  \   sys.path.append(vim.eval("s:curdir"))
  Py import schmerlin
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
    " call #1: return col number @ start of prefix
    let line = getline('.')
    let start = col('.') - 1
    " let symbols = '[!%\&\$#+-/:<=>?@\\\~`\^|\*]'
    " let is_symbolic = (line[start] =~ symbols)
    while start > 0
      " [0-9A-Za-z_] or prime or dot
      "" also check if symbolic identifier
      " if !is_symbolic && line[start - 1] =~ '\(\w\|''\|\.\)'
      if line[start - 1] =~ '\(\w\|''\|\.\)'
        let start -= 1
      " elseif is_symbolic && line[start - 1] =~ symbols
      "   let start -= 1
      else
        break
      endif
    endwhile
    return start
  else
    " call #2: return list of candidates
    let l:complete_res = []
    Py vim.command("let l:complete_res = %s" %
    \   schmerlin.complete_prefix(vim.eval("a:base")))
    return l:complete_res
  endif
endfunction
