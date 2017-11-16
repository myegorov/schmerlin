# Use case (modeled after OCaml's Merlin)

1. Jump between def and use with `-show-def-use`
2. Get a list of all uses for name under cursor (CtrlP like interface):
  - jump to any use in list
  - select/rename all occurrences in list etc.
3. autocomplete tooltip (probably plugin for Valloric/YouCompleteMe)
  - at a minimum, use default MLBasis
  - if editing an *b file, `transmile --imports` to infer imported scope
    with `-show-basis-verbose`
  - in the future, allow for directives at arbitrary point in buffer
      to dump basis at that point
4. query type of name under cursor to display in vim commandline
5. highlight unused definitions in current buffer
6. report type errors
7. autoreload def-use and basis for current buffer & run typechecker in the background
