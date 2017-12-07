" Vim syntax file
" Language:	SML extensions
" Maintainer:	Maksim Yegorov <findmaksim@gmail.com>
" URL: https://github.com/myegorov/schmerlin
" Last Change: 2017-12-06 Wed 07:14 PM

if exists("b:current_syntax")
  finish
endif

" fall back on standard syntax highlighting for SML
runtime! syntax/sml.vim syntax/sml/*.vim

syntax keyword TransmlerKeyword import export from
highlight link TransmlerKeyword PreProc

syntax keyword TransmlerDelimiter %%
highlight link TransmlerDelimiter Delimiter

" MLton basis
syntax match MLtonBasis /\v(^\s*import\s+)@<=\$\(SML_LIB\)\S*/
highlight link MLtonBasis String

" simple path
syntax match PathToBasis /\v(^\s*import\s+)@<=".+[^"]"/
highlight link PathToBasis String

" from path
syntax match FromPath /\v(^\s*import.+from\s+)@<=".+[^"]"/
highlight link FromPath String

let b:current_syntax = "sml"
