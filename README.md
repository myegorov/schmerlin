# Use case (modeled after OCaml's Merlin)

1. [IN PROGRESS] autocomplete tooltip (targeting Vim's `omnifunc`)
  - at a minimum, use default MLBasis
  - if editing an *b file, `transmile --imports` to infer imported scope
    with `-show-basis-flat`
  - [TBD] in the future, allow for directives at arbitrary point in buffer
      to dump basis at that point
2. [TBD] Jump between def and use with `-show-def-use`
3. [TBD] Get a list of all uses for name under cursor (CtrlP like interface):
  - jump to any use in list
  - select/rename all occurrences in list etc.
4. [TBD] query type of name under cursor to display in vim commandline
5. [TBD] highlight unused definitions in current buffer
6. [TBD] report type errors
7. [TBD] async autoreload def-use and basis for current buffer & run typechecker in the background
8. [TBD] alternate between .sig and .sml files (as in a.vim)

# Dependencies

Vim 7+ compiled with Python 3 support (`:echo has('python3') == 1`).

# Install

Install this plugin using a plugin manager, or by extracting the
files in your `~/.vim` directory.

If using [Vundle](https://github.com/VundleVim/Vundle.vim), add to your `~/.vimrc`:
```vim
Plugin 'myegorov/schmerlin'
```
and then run `:PluginInstall`

# Features

- autocomplete identifiers with <Tab>
