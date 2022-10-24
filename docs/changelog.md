# Changelogs

All notable changes to the `wfmap` package will be documented in this file.

## [1.0.3]

### Bug Fixes

- Fix matplotlib warning
- Thanks to [@benfroelich](https://github.com/benfroelich), fix bug where wafermap fn wasn't passing on non-default coord col names [#6](https://github.com/xlhaw/wfmap/pull/6)
- Fix legend display issue in `wif_trends` and add limitation on max items to plot

### Features

- Add new param `majority` in `wif_trend` for  control
- Add `wif_corrplot` for correlation plot
- Documentation Site https://www.wfmap.ml

## [1.0.2]

### Bug Fixes

- Unify the behaviors of grid lines when different matplotlib styles were applied
- Fix default title of `create_incmap` to None

## [1.0.0]

### Features

- Add more customized wafer heatmap and trend charts, such as DefectMap, IncomingMap, Trend Charts by Flash Field/Shot
- Add demo GUI program built with Gooey
- Add demo data and examples

### Changed

- Refactor original `wafermap` function to `num_heatmap` & `cat_heatmap` by numerical & categorical variables respectively
- Improve the documentation and tutorials  :vulcan_salute:

## [0.0.7]

### Added

- Add color histogram subplot for Wafer heatmap
- Add pie chart inset and yield annotation for categorical variables

## [0.0.1]

- First release. 🎉🎉🎉