# Tabler icons (vendored subset)

- Source: npm package `@tabler/icons`, **version 3.48.0** (https://tabler.io/icons,
  https://github.com/tabler/tabler-icons), outline style, unchanged SVG files.
- Licence: MIT, see `LICENSE` (copied from the package).
- Only the icons the repository uses are kept here (`outline/`, 50 files, about 25 KB of
  SVG) instead of the full set (5000+ icons, 21 MB): renders stay offline and reproducible,
  and the repository stays small. Add more of the same version with
  `python -m explainer.icons add <name> ...` (downloads from cdn.jsdelivr.net) and commit them.
- Loaded by `explainer.icons.icon()`, which writes the colour in place of `currentColor`.
