# WaferViz

`WaferViz` is a small GUI tool which wraps  `wfmap` to create fancy Wafer Map/Trend Plots.
![WaferViz](img/waferviz.jpg)

## Installation

Launch the application from command line as below:
```bash
git clone https://github.com/xlhaw/wfmap.git
cd wfmap/gui
pip install -r requirements.txt
python main.py
```

Since the package size by `Pyinstaller` is huge, the pre-compiled binary is not uploaded. Plan to rewrite with other approaches, eg **Tauri/Pyodide/Quarto** to package & distribute it in the future. 

## Configuration

Default settings are saved in the `config.yml` file, open with any text editor if need modification.
![](img/Config.jpg)

## Basic Usage

![](img/Basic.jpg)
![](img/Basic2.jpg)

## Data Download
![](img/Data.jpg)

## WaferMap
![](img/WaferMap.jpg)

## DefectMap
![](img/DefectMap.jpg)

## IncomingMap
![](img/IncomingMap.jpg)

## WIF Trend
![](img/WIF_Trend.jpg)

## WIF Trends
![](img/WIF_Trends.jpg)

## TwinY Trends
![](img/TwinTrends.jpg)