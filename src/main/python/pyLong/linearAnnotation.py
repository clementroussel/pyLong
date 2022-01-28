from matplotlib.text import Annotation as mpl_Annotation
from matplotlib.text import Text as mpl_Text

import numpy as np

from pyLong.dictionaries import *
from pyLong.annotation import Annotation


class LinearAnnotation(Annotation):
    counter = 0
    
    def __init__(self):
        LinearAnnotation.counter += 1
        
        Annotation.__init__(self)
        
        self.title = ""
    
        self.label = ""
        
        self.labelProperties = {'vertical shift': 0,
                                'size': 9.,
                                'color': 'Black'}
        
        self.arrowProperties = {'x start': 0.,
                                'x end': 1000.,
                                'z coordinate': 500.,
                                'arrow style': '<->',
                                'line style': 'solide',
                                'color': 'Black',
                                'thickness': 0.8}
        
        self.clear()

    def clear(self):
        self.annotation = mpl_Annotation("",
                                         xy=(0, 0),
                                         xytext=(0, 0),
                                         xycoords='data',
                                         arrowprops=dict(arrowstyle='->'))

        self.text = mpl_Text(0,
                             0,
                             "",
                             horizontalalignment='center',
                             verticalalignment='bottom')
                                         
    def update(self):
        self.annotation.arrow_patch.set_arrowstyle(self.arrowProperties['arrow style'])
        self.annotation.arrow_patch.set_linestyle(lineStyles[self.arrowProperties['line style']])
        self.annotation.arrow_patch.set_linewidth(self.arrowProperties['thickness'])
        self.annotation.arrow_patch.set_color(colors[self.arrowProperties['color']])
        self.annotation.arrow_patch.set_alpha(self.opacity)
        self.annotation.arrow_patch.set_zorder(self.order)        
        self.annotation.xy = (self.arrowProperties['x start'], self.arrowProperties['z coordinate'])
        self.annotation.set_x(self.arrowProperties['x end'])
        self.annotation.set_y(self.arrowProperties['z coordinate'])
        self.annotation.set_visible(self.active)
        
        self.text.set_text(self.label)
        self.text.set_x(np.mean([self.arrowProperties['x start'], self.arrowProperties['x end']]))
        self.text.set_y(self.arrowProperties['z coordinate'] + self.labelProperties['vertical shift'])
        self.text.set_fontsize(self.labelProperties['size'])
        self.text.set_color(colors[self.labelProperties['color']])
        self.text.set_alpha(self.opacity)
        self.text.set_zorder(self.order)
        self.text.set_visible(self.active)
        
    def __del__(self):
        LinearAnnotation.counter -= 1

    def imitate(self, annotation):
        if isinstance(annotation, LinearAnnotation):
            self.labelProperties['vertical shift'] = annotation.labelProperties['vertical shift']
            self.labelProperties['size'] = annotation.labelProperties['size']
            self.labelProperties['color'] = annotation.labelProperties['color']
            self.arrowProperties['arrow style'] = annotation.arrowProperties['arrow style']
            self.arrowProperties['line style'] = annotation.arrowProperties['line style']
            self.arrowProperties['color'] = annotation.arrowProperties['color']
            self.arrowProperties['thickness'] = annotation.arrowProperties['thickness']
            self.opacity = annotation.opacity
            self.order = annotation.order

            self.update()

    def duplicate(self):
        annotation = LinearAnnotation()
        annotation.imitate(self)

        annotation.label = self.label
        annotation.arrowProperties['x start'] = self.arrowProperties['x start']
        annotation.arrowProperties['x end'] = self.arrowProperties['x end']
        annotation.arrowProperties['z coordinate'] = self.arrowProperties['z coordinate']

        annotation.update()

        return annotation

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["annotation"] = mpl_Annotation("",
                                                  xy=(0, 0),
                                                  xytext=(0, 0),
                                                  xycoords='data',
                                                  arrowprops=dict(arrowstyle='->'))

        attributes["text"] = mpl_Text(0,
                                      0,
                                      "",
                                      horizontalalignment='center',
                                      verticalalignment='bottom')

        return attributes
