# Features

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
6. [TBD] commands to reload def-use and basis for current buffer (see below).
7. [TBD] alternate between `.sig` and `.sml` files (as in the `a.vim` plugin)
8. [TBD] update `transmler` for the requirements of `schmerlin`
9. [TBD] provide interface to custom plugin commands & option to disable
    default keybindings
10. [TBD] add support for plain .sml files (look for `<basename>.mlb` or
    `sources.mlb` or prompt user for path to mlb).


# Target workflow

The steps below refer to a sample project tree:

    project-root
    ├── dist                    <~~ created by transmler invoked from ../Makefile
    │   ├── f.sig
    │   ├── f.sig.mlb
    │   ├── f.sml
    │   ├── f.sml.mlb
    │   ├── g.sml
    │   └── g.sml.mlb
    ├── .ide                    <~~ generated via :mkdefuse
    │   ├── project.defuse
    │   └── project.mlb
    ├── Makefile
    ├── src                     <~~ working directory
    │   ├── f.sigb
    │   ├── f.smlb
    │   ├── g.smlb
    │   └── .ide                <~~ generated via :mkbasis
    │       ├── f.sig.mlb
    │       ├── f.smlb.basis
    │       ├── f.smlb.pkl
    │       ├── f.sml.mlb
    │       ├── g.smlb.basis
    │       ├── g.smlb.pkl
    │       └── g.sml.mlb
    └── .vimlocal               <~~ let b:mlb_root=expand("%:p:h")

- The user defines the project root (effectively creating the `mlb_root`
  buffer-scoped variable) by placing a
  (potentially empty) per-project `.vimlocal` file at the project's top level
  directory.
  `schmerlin`(this plugin) will ascend the
  file tree for the current buffer (triggered by relevant language extension)
  until it discovers the `.vimlocal`. It will then `:source .vimlocal` and
  set the `mlb_root` for the buffer.
- The user writes Standard ML in what we call the _smlb_ format
  (effectively combining `mlb` and `sml` in one module), and uses the
  [transmler](https://github.com/myegorov/transmler) preprocessor to
  transpile to the standard source representation that can be compiled by
  [MLton](https://github.com/MLton/mlton).
- `schmerlin` will define the `:mkdefuse` command to extract the information
  that can be used via custom commands to jump between
  definitions and uses, select all use cases, query the type information,
  and highlight redundant definitions. Specifically, `:mkdefuse` will
  (a) temporarily bind 
  `makeprg` to the
  `transmile` command, (b) run `transmile` to create the
  `$mlb_root/.ide/project.mlb` that imports all files ending in
  `.sml`, `.sig`, `fun`, `.smlb`, `.sigb`, and `.funb` nested under `$mlb_root`
  and then (c) run
  `mlton -prefer-abs-paths true -show-def-use $mlb_root/.ide/project.defuse -stop tc`
  to create the project-wide [def-use](http://mlton.org/EmacsDefUseMode)
  file under `$mlb_root/.ide/` and finally (d) rebind `makeprg` to its 
  original setting (or default `make`).
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
  (e) rebind `makeprg` to the original setting (or default `make`).
- Outside the scope of this plugin, `transmile` and `mlton` can be invoked
  from vim via `:make` goals to transpile the sources,
  typecheck (and report errors
  in the quickfix window) and build the binary, e.g. with the help of a
  `Makefile`.


# Dependencies

- Vim 8+ compiled with Python 3 support (`:echo has('python3') == 1`).
    (or Vim 7+ if not relying on async?)
- [MLton](https://github.com/MLton/mlton)
- [transmler](https://github.com/myegorov/transmler)


# Install

Install this plugin using a plugin manager, or by extracting the
files in your `~/.vim` directory.

For example, if using [Vundle](https://github.com/VundleVim/Vundle.vim), add to your `~/.vimrc`:
```vim
Plugin 'myegorov/schmerlin'
```
and then run `:PluginInstall`


# Custom commands & key bindings

- trigger autocomplete with <kbd>Tab</kbd> in insert mode
- cycle forward through popup autosuggestions with <kbd>Tab</kbd>, or 
  <kbd>Ctrl</kbd>+<kbd>n</kbd>,
  and backward with <kbd>Ctrl</kbd>+<kbd>p</kbd>
- toggle between main and preview windows as usual in the normal mode 
  with <kbd>Ctrl</kbd>+<kbd>w</kbd> followed by <kbd>w</kbd>; close
  the preview window with `:pc`

[...to be continued]

# Inspiration

- [MLton's emacs mode](http://mlton.org/Emacs)
- [OCaml's merlin](https://github.com/ocaml/merlin)
- [Matthew Fluet](https://github.com/matthewfluet) provided
  direction and encouragement
