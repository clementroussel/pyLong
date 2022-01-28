from matplotlib.text import Text as mpl_Text
from matplotlib.lines import Line2D

import numpy as np

from pyLong.dictionaries import lineStyles, colors
from pyLong.annotation import Annotation


class Interval(Annotation):
    counter = 0
    
    def __init__(self):
        Interval.counter += 1
        
        Annotation.__init__(self)
        
        self.title = ""
    
        self.label = ""
        
        self.limits = {'x start': 100,
                       'x end': 900,
                       'z start': 500,
                       'z end': 500,
                       'z low': 0}
        
        self.labelProperties = {'z coordinate': 0.,
                                'size': 9.,
                                'color': 'Black'}
        
        self.limitsProperties = {'style': 'solid',
                                 'color': 'Black',
                                 'thickness': 0.8}
        
        self.frame = {'style': 'solid',
                      'color': 'Black',
                      'thickness': 0.8}
        
        self.clear()

    def clear(self):
        self.text = mpl_Text(0,
                             0,
                             "",
                             horizontalalignment='center',
                             verticalalignment='center',
                             bbox=dict(facecolor='w')
                             )

        self.startLine = Line2D([], [])

        self.endLine = Line2D([], [])
                                         
    def update(self):
        self.text.set_text(self.label)
        self.text.set_x(np.mean([self.limits['x start'], self.limits['x end']]))
        self.text.set_y(self.labelProperties['z coordinate'])
        self.text.set_fontsize(self.labelProperties['size'])
        self.text.set_color(colors[self.labelProperties['color']])
        self.text.set_alpha(self.opacity)
        self.text.set_zorder(self.order)
        self.text.set_bbox(dict(linestyle=lineStyles[self.frame['style']],
                                edgecolor=colors[self.frame['color']],
                                linewidth=self.frame['thickness'],
                                facecolor='White',
                                alpha=self.opacity,
                                zorder=self.order))
        
        self.text.set_visible(self.active)
        
        self.startLine.set_data([self.limits['x start'], self.limits['x start']],
                                [self.limits['z low'], self.limits['z start']])
        self.startLine.set_linestyle(lineStyles[self.limitsProperties['style']])
        self.startLine.set_color(colors[self.limitsProperties['color']])
        self.startLine.set_linewidth(self.limitsProperties['thickness'])
        self.startLine.set_alpha(self.opacity)
        self.startLine.set_zorder(self.order)
        self.startLine.set_visible(self.active)
        
        self.endLine.set_data([self.limits['x end'], self.limits['x end']],
                              [self.limits['z low'], self.limits['z end']])
        self.endLine.set_linestyle(lineStyles[self.limitsProperties['style']])
        self.endLine.set_color(colors[self.limitsProperties['color']])
        self.endLine.set_linewidth(self.limitsProperties['thickness'])
        self.endLine.set_alpha(self.opacity)
        self.endLine.set_zorder(self.order)
        self.endLine.set_visible(self.active)
        
    def __del__(self):
        Interval.counter -= 1

    def imitate(self, annotation):
        if isinstance(annotation, Interval):
            self.labelProperties['z coordinate'] = annotation.labelProperties['z coordinate']
            self.labelProperties['size'] = annotation.labelProperties['size']
            self.labelProperties['color'] = annotation.labelProperties['color']
            self.limitsProperties['style'] = annotation.limitsProperties['style']
            self.limitsProperties['color'] = annotation.limitsProperties['color']
            self.limitsProperties['thickness'] = annotation.limitsProperties['thickness']
            self.frame['style'] = annotation.frame['style']
            self.frame['thickness'] = annotation.frame['thickness']
            self.frame['color'] = annotation.frame['color']
            self.opacite = annotation.opacite
            self.ordre = annotation.ordre

            self.update()

    def duplicate(self):
        annotation = Interval()
        annotation.imitate(self)

        annotation.label = self.label
        annotation.limits['x start'] = self.limits['x start']
        annotation.limits['x end'] = self.limits['x end']
        annotation.limits['z start'] = self.limits['z start']
        annotation.limits['z end'] = self.limits['z end']
        annotation.limits['z low'] = self.limits['z low']

        annotation.update()

        return annotation

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["text"] = mpl_Text(0,
                                      0,
                                      "",
                                      horizontalalignment='center',
                                      verticalalignment='center',
                                      bbox=dict(facecolor='w')
                                      )

        attributes["startLine"] = Line2D([], [])

        attributes["endLine"] = Line2D([], [])

        return attributes
