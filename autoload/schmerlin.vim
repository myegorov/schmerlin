"------------------------
" Global settings
"------------------------
let s:curdir=expand("<sfile>:p:h")

function! s:WarnMsg(msg)
  echohl WarningMsg | echomsg "WARNING => " . a:msg | echohl None
endfunction

function! s:ErrorMsg(msg)
  echohl ErrorMsg | echoerr "ERROR => " . a:msg | echohl None
endfunction

function! schmerlin#CheckDependencies()
  " Python3
  if has('python3')
    command! -nargs=1 Py python3 <args>
    Py import sys, vim
    Py if not vim.eval("s:curdir") in sys.path:
    \   sys.path.append(vim.eval("s:curdir"))
    Py import schmerlin
    Py from util import find_mlton as fm
    Py from util import find_transmler as ft
  else
    call s:ErrorMsg('vim must be compiled with +python3')
  endif

  " Vim version
  if !(v:version >= 800 || has('patch-7.4.1829'))
    call s:ErrorMsg('require vim >= 7.4.1829')
  endif

  " skywind3000/asyncrun.vim plugin
  if !exists(':AsyncRun')
    call s:ErrorMsg('require skywind3000/asyncrun.vim plugin')
  endif

  " MLton
  Py vim.command("let s:mlton_ok = %d" %fm.test_mlton())
  if (s:mlton_ok != 1)
    call s:ErrorMsg('require MLton >= MLton 20171229.*')
  endif

  " transmler
  Py vim.command("let s:transmler_ok = %d" %ft.test_transmler())
  if (s:transmler_ok != 1)
    call s:ErrorMsg('require transmler >= 0.3.3')
  endif
endfunction


" main point of entry
function! schmerlin#Register() abort
  call schmerlin#CheckDependencies()
  setlocal omnifunc=schmerlin#Complete
  setlocal completeopt=longest,menuone,preview

  " remap <Tab> for invoking autocomplete & cycling
  inoremap <buffer> <Tab> <C-R>=schmerlin#CleverTab()<CR>

  " use <ENTER> to select
  inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"

  " " autoclose preview window once autocompleted
  " autocmd CompleteDone * pclose

  " remove line numbers in preview window
  autocmd WinEnter * call schmerlin#Preview()

  " TODO monitor async command status
  " https://github.com/skywind3000/asyncrun.vim/wiki/Display-Progress-in-Status-Line-or-Airline

  " TODO: run async, signal when done
  Py schmerlin.get_trie(vim.eval("expand('%:p')"))
endfunction

function! schmerlin#Preview()
  if &previewwindow
    setlocal nonumber
  endif
endfunction

function! schmerlin#CleverTab()
  " at line start or after a space -> <TAB>
  if strpart(getline('.'), 0, col('.') - 1) =~ '^\s*$'
      return "\<Tab>"
  else
    " omni completion takes priority
    if &omnifunc != ''
      " cycle through menu
      if pumvisible()
        return "\<C-N>"
      else
        return "\<C-X>\<C-O>"
      endif
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
    let s:symbols = '[!%&$#:<=>?@\~`^\|*\+\-\/\\]'
    " FIXME: bug, e.g. Compare.>=.whatever is a valid identifier
    "         do this regex thingy in Python instead
    let l:is_symbolic = ((l:line[l:start - 1] =~ s:symbols))
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
    return l:start
  else
    " call #2: return list of candidates
    let l:complete_res = []
    Py vim.command("let l:complete_res = %s" %
    \   schmerlin.complete_prefix(vim.eval("a:base"), vim.eval("expand('%:p')")))
    return l:complete_res
  endif
endfunction
