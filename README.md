# Use case (modeled after OCaml's Merlin)

1. autocomplete tooltip (targeting Vim's `omnifunc`)
  - at a minimum, use default MLBasis
  - if editing an *b file, `transmile --imports` to infer imported scope
    with `-show-basis-flat`
  - in the future, allow for directives at arbitrary point in buffer
      to dump basis at that point
2. Jump between def and use with `-show-def-use`
3. Get a list of all uses for name under cursor (CtrlP like interface):
  - jump to any use in list
  - select/rename all occurrences in list etc.
4. query type of name under cursor to display in vim commandline
5. highlight unused definitions in current buffer
6. report type errors
7. async autoreload def-use and basis for current buffer & run typechecker in the background
8. alternate between .sig and .sml files (as in a.vim)


# Roadmap

- skeleton for a Vim plugin (for now only for autocompletion);
- parser for -show-basis-flat, dump to prefix trie representation
  (see `:help complete-items` for `omnifunc` requirements)
- add other features
