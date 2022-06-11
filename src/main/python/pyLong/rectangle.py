from matplotlib.patches import Rectangle as mpl_Rectangle

from pyLong.dictionaries import lineStyles, colors
from pyLong.annotation import Annotation


class Rectangle(Annotation):
    counter = 0
    
    def __init__(self):
        Rectangle.counter += 1
        
        Annotation.__init__(self)
        
        self.title = "Rectangle n°{}".format(Rectangle.counter)
    
        self.label = ""

        self.position = {'x coordinate' : 500,
                         'z coordinate' : 500}

        self.dimensions = {'width' : 100,
                           'height' : 100}
        
        self.outline = {'line style': "solid",
                        'color': 'Black',
                        'thickness': 0.8}
        
        self.filling = {'color': 'White',
                        'hatch style': '/',
                        'density': 1}
        
        self.clear()

    def clear(self):
        self.rectangle = mpl_Rectangle((0,0), 0, 0)
        
    def update(self):
        self.rectangle.set_xy((self.position['x coordinate'], self.position['z coordinate']))
        self.rectangle.set_width(self.dimensions['width'])
        self.rectangle.set_height(self.dimensions['height'])
        if self.active:
            self.rectangle.set_label(self.label)
        else:
            self.rectangle.set_label("")
        self.rectangle.set_linestyle(lineStyles[self.outline['line style']])
        self.rectangle.set_linewidth(self.outline['thickness'])
        self.rectangle.set_edgecolor(colors[self.outline['color']])
        self.rectangle.set_facecolor(colors[self.filling['color']])
        self.rectangle.set_hatch(self.filling['density'] * self.filling['hatch style'])
        self.rectangle.set_alpha(self.opacity)
        self.rectangle.set_zorder(self.order)
        self.rectangle.set_visible(self.active)
        
    def __del__(self):
        Rectangle.counter -= 1

    def imitate(self, annotation):
        if isinstance(annotation, Rectangle):
            self.outline['line style'] = annotation.contour['line style']
            self.outline['color'] = annotation.contour['color']
            self.outline['thickness'] = annotation.contour['thickness']
            self.filling['color'] = annotation.filling['color']
            self.filling['hatch style'] = annotation.filling['hatch style']
            self.filling['density'] = annotation.filling['density']
            self.opacity = annotation.opacity
            self.order = annotation.order

            self.update()

    def duplicate(self):
        annotation = Rectangle()
        annotation.imitate(self)

        annotation.label = self.label
        annotation.position['x coordinate'] = self.position['x coordinate']
        annotation.position['z coordinate'] = self.position['z coordinate']
        annotation.dimensions['width'] = self.dimensions['width']
        annotation.dimensions['height'] = self.dimensions['height']

        annotation.update()

        return annotation

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["rectangle"] = mpl_Rectangle((0,0), 0, 0)

        return attributes
