from utils.version import get_git_version
import os

MODULE_DIR = os.path.dirname(__file__)

__version__ = get_git_version(MODULE_DIR)
__author__ = "Paul Golder"
__author_github__ = "https://github.com/Hysnap"
__description__ = "Visualisations for the project."
__all__ = [
    'plot_bar_line.plot_bar_line_by_year',
    'plot_bar_chart.plot_bar_chart',
    'plot_regresionplot.plot_regresionplot',
    'plot_pie_chart.plot_pie_chart',
    'plot_scatter_chart.',
    # 'plot_line_chart',
    # 'plot_heatmap',
    # 'plot_histogram',
    # 'plot_box_plot',
    # 'plot_violin_plot',
    # 'plot_strip_plot',
    # 'plot_funnel_plot',
    # 'plot_density_contour',
    # 'plot_density_heatmap',
    # 'plot_imshow',
    # 'plot_treemap',
    # 'plot_sunburst',
]