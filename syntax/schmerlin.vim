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
set filetype=sml

syntax keyword TransmlerInclude import export from
highlight link TransmlerInclude Include

syntax keyword TransmlerDelimiter %%
highlight link TransmlerDelimiter Delimiter

syntax keyword TransmlerTodo TODO FIXME contained
highlight link TransmlerTodo Todo

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
