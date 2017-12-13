# Use case (modeled after OCaml's Merlin)

1. [IN PROGRESS] autocomplete tooltip (targeting Vim's `omnifunc`)
  - at a minimum, uses default MLBasis + SML reserved words
  - if editing an `*b` file, `transmile --imports` to infer imported scope
    with `-show-basis-flat`
  - [TBD] in the future, allow for directives at arbitrary point in buffer
      to dump basis at that point
2. [TBD] Jump between def and use with `-show-def-use` (create a single 
    def-use file per project by importing all `*.smlb`, `*.sigb`, `*.funb` 
    files below project level dir)
3. [TBD] Get a list of all uses for name under cursor (CtrlP like interface):
  - jump to any use in list
  - select/rename all occurrences in list, highlight them in buffer etc.
4. [TBD] query type of name under cursor to display in vim commandline
5. [TBD] highlight unused definitions in current buffer
7. [TBD] commands to reload def-use and basis for current buffer (see below).
8. [TBD] alternate between `.sig` and `.sml` files (as in the `a.vim` plugin)

# Target Workflow

- User defines the project root (effectively creating the `MLB_ROOT`
  environmental variable) by placing a
  (potentially empty) per-project `.vimrc` file. `schmerlin` will ascend the
  file tree for the current buffer (triggered by relevant language extension)
  until it discovers the `.vimrc` and
  sets the `MLB_ROOT` for the buffer.
- `schmerlin` will define the `:mkdefuse` command to extract the information
  that can be used via custom commands to jump between
  definitions and uses, select all use cases, query the type information,
  and highlight redundant definitions. Specifically, `:mkdefuse` will
  (a) temporarily bind 
  `makeprg` to the
  `transmile` command, (b) run `transmile` to create the
  `$MLB_ROOT/.ide/project.mlb` that imports all files ending in
  `.sml`, `.sig`, `fun`, `.smlb`, `.sigb`, and `.funb` under `$MLB_ROOT` and
  then (c) run
  `mlton -prefer-abs-paths true -show-def-use $MLB_ROOT/.ide/project.defuse -stop tc`
  to create the project-wide [def-use](http://mlton.org/EmacsDefUseMode)
  file under `$MLB_ROOT/.ide/` and finally (d) rebind `makeprg` to the 
  default `make`. 
- `schmerlin` will additionally define the `:mkbasis` command to extract the
  information that can be used for autocompletion in the current buffer.
  Specifically, `:mkbasis` will
  (a) temporarily bind `makeprg` to the `transmile` command, (b) run
  `transmile` to create the 
  `<current-buffer-dir>/.ide/<current-buffer-filename>.mlb`,
  (c) run
	`mlton -show-basis <current-buffer-dir>/.ide/<current-buffer-file-name>.basis -show-basis-flat true -stop tc <current-buffer-dir>/.ide/<current-buffer-filename>.mlb`
  to write out the names in scope based on the imports of current buffer to
  `<current-buffer-dir>/.ide/<current-buffer-file-name>.basis`, 
  (d) postprocess the `basis` scope to create a prefix trie to be used 
  for autocompletion and write it to
  `<current-buffer-dir>/.ide/<current-buffer-file-name>.pkl`, and finally
  (e) rebind `makeprg` to the default `make`.
- `transmile` and `mlton` can be invoked from vim run via the default 
  `:make` goals to transpile the sources, typecheck (and report errors 
  in the quickfix window) and build the binary.


# Dependencies

- Vim 7+ compiled with Python 3 support (`:echo has('python3') == 1`).
- [MLton](https://github.com/MLton/mlton)
- Transmler (pip install? git submodule?)

# Install

Install this plugin using a plugin manager, or by extracting the
files in your `~/.vim` directory.

If using [Vundle](https://github.com/VundleVim/Vundle.vim), add to your `~/.vimrc`:
```vim
Plugin 'myegorov/schmerlin'
```
and then run `:PluginInstall`

# Custom commands & key bindings

- trigger autocomplete &lt;Tab&gt;
- inspect signature in the preview window

...to be continued
