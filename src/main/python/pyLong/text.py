from matplotlib.text import Text as mpl_Text

from pyLong.dictionaries import lineStyles, colors
from pyLong.annotation import Annotation

class Text(Annotation):
    counter = 0
    
    def __init__(self):
        Text.counter += 1
        
        Annotation.__init__(self)
        
        self.title = ""
    
        self.label = ""

        self.position = {'x coordinate': 500,
                         'z coordinate': 500}
        
        self.labelProperties = {'size': 9.,
                                'color': 'Black',
                                'style': 'normal',
                                'thickness': 'normal',
                                'rotation': 0}
        
        self.clear()

    def clear(self):
        self.text = mpl_Text(0,
                             0,
                             "",
                             rotation = 0,
                             rotation_mode = 'anchor',
                             horizontalalignment ='left',
                             verticalalignment ='baseline')
                                         
    def update(self):
        self.text.set_text(self.label)
        self.text.set_x(self.position['x coordinate'])
        self.text.set_y(self.position['z coordinate'])
        self.text.set_fontsize(self.labelProperties['taille'])
        self.text.set_fontstyle(self.labelProperties['style'])
        self.text.set_color(colors[self.labelProperties['color']])
        self.text.set_fontweight(self.labelProperties['thickness'])
        self.text.set_rotation(self.labelProperties['rotation'])
        self.text.set_alpha(self.opacity)
        self.text.set_zorder(self.order)
        self.text.set_visible(self.active)
        
    def __del__(self):
        Text.counter -= 1

    def imitate(self, annotation):
        if isinstance(annotation, Text):
            self.labelProperties['size'] = annotation.labelProperties['size']
            self.labelProperties['color'] = annotation.labelProperties['color']
            self.labelProperties['style'] = annotation.labelProperties['style']
            self.labelProperties['thickness'] = annotation.labelProperties['thickness']
            self.labelProperties['rotation'] = annotation.labelProperties['rotation']
            self.opacity = annotation.opacity
            self.order = annotation.order

            self.update()

    def duplicate(self):
        annotation = Text()
        annotation.imitate(self)

        annotation.label = self.label
        annotation.position['x coordinate'] = self.position['x coordinate']
        annotation.position['z coordinate'] = self.position['z coordinate']

        annotation.update()

        return annotation

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["text"] = mpl_Text(0,
                                      0,
                                      "",
                                      rotation=0,
                                      rotation_mode='anchor',
                                      horizontalalignment='left',
                                      verticalalignment='baseline')

        return attributes
