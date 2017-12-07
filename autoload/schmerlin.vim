function! schmerlin#Register()
  setlocal omnifunc=schmerlin#Complete
  inoremap <buffer> <Tab> <C-R>=schmerlin#CleverTab()<CR>
endfunction

function! schmerlin#CleverTab()
    if strpart(getline('.'), 0, col('.') - 1) =~ '^\s*$'
        return "\<Tab>"
    else
        if &omnifunc != ''
            return "\<C-x>\<C-o>"
        elseif &dictionary != ''
            return "\<C-K>"
        else
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
