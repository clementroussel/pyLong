from matplotlib.text import Annotation as mpl_Annotation

from pyLong.dictionaries import lineStyles, colors
from pyLong.annotation import Annotation


class VerticalAnnotation(Annotation):
    counter = 0
    
    def __init__(self):
        VerticalAnnotation.counter += 1
        
        Annotation.__init__(self)
        
        self.title = "Vertical annotation n°{}".format(VerticalAnnotation.counter)
    
        self.label = ""

        self.position = {'x coordinate' : 500.,
                         'z coordinate' : 500.}
        
        self.labelProperties = {'size': 9.,
                                'color': 'Black'}
        
        self.arrowProperties = {'length': 100,
                                'vertical shift': 0,
                                'arrow style': '-|>',
                                'line style': 'solid',
                                'color': 'Black',
                                'thickness': 1}
        
        self.clear()

    def clear(self):
        self.annotation = mpl_Annotation("",
                                         xy=(0, 0),
                                         xytext=(0, 0),
                                         xycoords='data',
                                         rotation=90,
                                         horizontalalignment='center',
                                         verticalalignment='bottom',
                                         arrowprops=dict(arrowstyle='->'))
                                         
    def update(self):
        self.annotation.arrow_patch.set_arrowstyle(self.arrowProperties['arrow style'])
        self.annotation.arrow_patch.set_linestyle(lineStyles[self.arrowProperties['line style']])
        self.annotation.arrow_patch.set_linewidth(self.arrowProperties['thickness'])
        self.annotation.arrow_patch.set_color(colors[self.arrowProperties['color']])
        self.annotation.arrow_patch.set_alpha(self.opacity)
        self.annotation.arrow_patch.set_zorder(self.order)        
        
        self.annotation.set_text(self.label)
        self.annotation.xy = (self.position['x coordinate'], self.position['z coordinate'] + self.arrowProperties['vertical shift'])
        self.annotation.set_x(self.position['x coordinate'])
        self.annotation.set_y(self.position['z coordinate'] + self.arrowProperties['length'] + self.arrowProperties['vertical shift'])
        self.annotation.set_color(colors[self.labelProperties['color']])
        self.annotation.set_fontsize(self.labelProperties['size'])
        self.annotation.set_alpha(self.opacity)
        self.annotation.set_zorder(self.order)
        
        self.annotation.set_visible(self.active)
        
    def __del__(self):
        VerticalAnnotation.counter -= 1

    def imitate(self, annotation):
        if isinstance(annotation, VerticalAnnotation):
            self.labelProperties['size'] = annotation.labelProperties['size']
            self.labelProperties['color'] = annotation.labelProperties['color']
            self.arrowProperties['length'] = annotation.arrowProperties['length']
            self.arrowProperties['vertical shift'] = annotation.arrowProperties['vertical shift']
            self.arrowProperties['arrow style'] = annotation.arrowProperties['arrow style']
            self.arrowProperties['line style'] = annotation.arrowProperties['line style']
            self.arrowProperties['color'] = annotation.arrowProperties['color']
            self.arrowProperties['thickness'] = annotation.arrowProperties['thickness']
            self.opacity = annotation.opacity
            self.order = annotation.order

            self.update()

    def duplicate(self):
        annotation = VerticalAnnotation()
        annotation.imitate(self)

        annotation.label = self.label
        annotation.position['x coordinate'] = self.position['x coordinate']
        annotation.position['z coordinate'] = self.position['z coordinate']

        annotation.update()

        return annotation

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["annotation"] = mpl_Annotation("",
                                                  xy=(0, 0),
                                                  xytext=(0, 0),
                                                  xycoords='data',
                                                  rotation=90,
                                                  horizontalalignment='center',
                                                  verticalalignment='bottom',
                                                  arrowprops=dict(arrowstyle='->'))

        return attributes
