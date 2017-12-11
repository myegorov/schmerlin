" check dependencies
" TODO: check for MLton on path and pip install transmler
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

" main point of entry
function! schmerlin#Register()
  setlocal omnifunc=schmerlin#Complete
  inoremap <buffer> <Tab> <C-R>=schmerlin#CleverTab()<CR>

  if !exists('b:trie')
    Py vim.command("let b:trie = %s" %schmerlin.load_trie())
  endif
endfunction

function! schmerlin#CleverTab()
  " at line start or after a space -> <TAB>
  if strpart(getline('.'), 0, col('.') - 1) =~ '^\s*$'
      return "\<Tab>"
  else
    " omni completion takes priority
    " TODO: check if completion window is open -> cycle through suggestions
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
    let l:line = getline('.')
    let l:start = col('.') - 1
    let s:symbols = '[!%&$#+-/:<=>?@\~`^|*]'
    let l:is_symbolic = (l:line[l:start - 1] =~ s:symbols)
    while l:start > 0
      " Valid identifiers:
      "   [0-9A-Za-z_] or prime or dot
      "   also check if symbolic identifier
      if !l:is_symbolic && (l:line[l:start - 1] =~ '\(\w\|''\|\.\)')
        let l:start -= 1
      elseif l:is_symbolic && (l:line[l:start - 1] =~ s:symbols)
        let l:start -= 1
      else
        break
      endif
    endwhile
    " TODO: return -1 if start unchanged (meaning no completion possible)
    return l:start
  else
    " call #2: return list of candidates
    " TODO: construct & cache the prefix trie on first call (for now assuming will read
    "       from file on first call)
    " workaround to print \\ as \
    let l:complete_res = []
    Py vim.command("let l:complete_res = %s" %
    \   str(schmerlin.complete_prefix(vim.eval("a:base"), vim.eval("b:trie"))).replace("\\\\", "\\"))
    return l:complete_res
  endif
endfunction
