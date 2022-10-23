import os
import yaml
from gooey import Gooey, GooeyParser
from wfmap import *
import numpy as np
from .wfdata import Wafer, merge_wfmap
from .wfutils import get_wflist, read_excel

# default args
with open(f'{os.path.dirname(__file__)}/config.yml') as f:
    default = yaml.load(f, Loader=yaml.Loader)

menu = [{
    'name': 'Help',
    'items': [{
            'type': 'AboutDialog',
        'menuTitle': 'About',
        'name': 'WaferViz',
                'description': 'A Toolbox for Wafer Data Visualization',
                'version': '1.0.0',
                'copyright': '2017~2022',
                'website': 'https://github.com/xlhaw/wfmap',
                'developer': 'Leon Xiao <i@xlhaw.com>',
                'license': 'MIT'
    }, {
        'type': 'Link',
        'menuTitle': 'Visit Source',
        'url': 'https://github.com/xlhaw/wfmap'
    }, {
        'type': 'Link',
        'menuTitle': 'Docs Online',
        'url': 'https://www.wfmap.ml'
    }]
}]


@Gooey(
    program_name="WaferViz",
    program_description="Create Fancy Wafer Map/Trend with ease",
    # image_dir='./assets',
    image_dir=f'{os.path.dirname(__file__)}/assets',
    menu=menu,
    richtext_controls=True,
    default_size=(600, 520),
    navigation="TABBED",
    optional_cols=3,
    required_cols=1,
    progress_regex=r"^Progress (\d+)$",
)
def main():
    parser = GooeyParser()

    programs = {'wafer_map': ['WaferMap'],
                'defect_map': ['DefectMap'],
                'inc_map': ["IncomingMap"],
                "wif_trend": ["WIF Trend"],
                "wif_trends": ["WIF Trends"],
                'twin_trends': ["TwinY Trends"],
                }
    subs = parser.add_subparsers(help="commands", dest="command")

    for k, v in programs.items():
        programs[k].append(subs.add_parser(
            k, prog=v[0]).add_argument_group(''))

    for tab in ['wafer_map', 'wif_trend', 'wif_trends', 'twin_trends']:
        prog = programs[tab][1]
        prog.add_argument(
            "-input_file",
            metavar=' ',
            help='Select the Rawdata',
            widget="FileChooser",
            gooey_options=dict(
                wildcard="Excel/Csv files (*.xlsx, *.csv,*xls)|*.xlsx;*.csv;*.xls")
        )
        prog.add_argument(
            "-wafer_format",
            default='UP2/UF2',
            metavar=' ',
            type=str,
            help="Confirm the Wafer Format",
            choices=['UP/UF', 'UP2/UF2', 'UP3/UF3', 'UP2E/UF2E', 'UP3E/UF3E']
        )
        prog.add_argument('-OCR', nargs='?', type=str,
                          default='SLIDER_OCR_NO',
                          metavar=' ',
                          help="Specify the OCR Column"
                          )
        prog.add_argument(
            '-value', nargs='?', type=str,
            default='CLO1A_RLGH_AFT',
            metavar=' ',
            help="Input the Column Name to Plot"
        )
        prog.add_argument(
            '-yrange',
            type=float,
            metavar=' ',
            default=None,
            # widget='DecimalField',
            help="Y-axis Range"
        )
    programs['defect_map'][1].add_argument(
        'server',
        type=str,
        metavar='Server Path',
        # default=r'\\dn2prod11\FSPDC\INCOMING\HDWY',
        default=default['Path']['Server'],
        help="Specify the location of Incoming *.LZH files")
    programs['defect_map'][1].add_argument(
        '-wafer',
        type=str,
        default='H1ABCD',
        metavar='Wafer',
        help="Input the Wafer No.")
    programs['inc_map'][1].add_argument(
        "-wflist",
        metavar='Wafer List',
        help="Open the Wafer List",
        default=default['Path']['Wf_List'],
        widget="FileChooser",
        gooey_options=dict(wildcard="Text files (*.txt)|*.txt")
    )

    programs['inc_map'][1].add_argument('-items', metavar='Select Items', help="Pick items to Plot",
                                        default=['ELG_RES', 'WELG_RES',
                                                 'MR', 'HDI', 'OSR'],
                                        widget="Listbox", nargs='+', choices=default['IncMap'].keys())

    for tab in ['wif_trends', 'twin_trends']:
        prog = programs[tab][1]
        prog.add_argument('-value2', nargs='?', type=str,
                          default='CLO1A_WRLGH_AFT',
                          metavar=' ',
                          help="2nd Column Name to Plot"
                          )

    for tab in ['twin_trends']:
        prog.add_argument(
            '-keep_rng',
            required=False,
            action="store_true",
            default=False,
            metavar=' ',
            help="Keep twinY-range same as Y-range"
        )
        prog.add_argument(
            '-tyrange',
            type=float,
            required=False,
            metavar=' ',
            default=None,
            # widget='DecimalField',
            help="2nd Y-axis Range"
        )

    for tab in programs:
        prog = programs[tab][1]
        prog.add_argument(
            "-output_dir",
            help="Select Output Directory",
            metavar=' ',
            widget="DirChooser",
            default=default['Path']['Output'],
        )

    args = parser.parse_args()
    handler(args)


def handler(args):
    #print(vars(args), default)
    os.chdir(args.output_dir)
    if args.command == 'defect_map':
        defectmap(Wafer(args.wafer).clean_inc(), 'DEFECT', ok_codes=default['UAI_CODE'], title=f'{args.wafer[1:]} Incoming DefectMap').savefig(
            f'{args.wafer[1:]} DefectMap.jpg')
    elif args.command == "inc_map":
        vsigmas = {'ELG_RES': 0.2, 'WELG_RES': 0.2, 'MR': 10,
                   'MR2': 10, 'PCM': 5,  'HDI': 0.75, 'OSR': 1}
        _ = [vsigmas.pop(item) for item in vsigmas if item not in args.items]
        for wf in get_wflist(args.wflist):
            print(f'Processing {wf} ---------------')
            df = Wafer(wf).clean_inc()
            df['ELG_RES'][df['ELG_STATUS'] != 'R2'] = np.nan
            df['WELG_RES'][df['WELG_STATUS'] != 'W2'] = np.nan
            create_incmap(df, title=f'{wf} Incoming Map').savefig(
                f'{args.wafer} IncomingMap.jpg')
    elif args.command in ['wafer_map', 'wif_trend', 'wif_trends', 'twin_trends']:
        wftype = args.wafer_format.split('/')[0]
        data = read_excel(args.input_file)
        data = merge_wfmap(data, ocr_col=args.OCR, mode=wftype,
                           map_path=f'{os.path.dirname(__file__)}/layout')
        for wf, df in data.groupby('Wafer'):
            print(f'Processing {wf} ---------------')
            if args.command == "wafer_map":
                wafermap(df, args.value, title=f'{wf} {args.value}', wftype=wftype).savefig(
                    f'{wf} {args.value}.jpg')
            elif args.command == "wif_trend":
                wif_trend(df, args.value, yrange=args.yrange, title=f'{wf} {args.value}').savefig(
                    f'{wf} {args.value} Trend.jpg')
            elif args.command == "wif_trends":
                wif_trends(df, [args.value, args.value2], yrange=args.yrange, title=f'{wf} {args.value}&{args.value2}').savefig(
                    f'{wf} {args.value}&{args.value2} Trend.jpg')
            elif args.command == "twin_trends":
                twin_trends(df, args.value, args.value2, yrange=args.yrange, tyrange=args.tyrange, keep_rng=args.keep_rng,
                            title=f'{wf} {args.value}&{args.value2}').savefig(f'{wf} {args.value}&{args.value2} TwinY Trend.jpg')


if __name__ == '__main__':
    main()
