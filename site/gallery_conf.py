from mkdocs_gallery.gen_gallery import DefaultResetArgv
import os
import sys

min_reported_time = 0
if 'SOURCE_DATE_EPOCH' in os.environ:
    min_reported_time = sys.maxint if sys.version_info[0] == 2 else sys.maxsize

sphinx_gallery_conf = {
    'image_scrapers': ('matplotlib'),
    'matplotlib_animations': True,
}


conf = {
    'reset_argv': DefaultResetArgv(),
    'min_reported_time': min_reported_time,
}
