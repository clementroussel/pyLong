class Layout:
    counter = -1

    def __init__(self):
        Layout.counter += 1

        self.title = ""

        self.dimensions = {'width': 29.7,
                           'height': 21.0}

        self.format = 'png'

        self.dpi = 300

        self.secondaryAxis = False

        self.xAxisProperties = {'min': 0.,
                                'max': 1000.,
                                'label': 'x (m)',
                                'intervals': 10,
                                'label size': 9.,
                                'label color': 'Black',
                                'value size': 9.,
                                'value color': 'Black',
                                'left shift': 5,
                                'right shift': 5}

        self.zAxisProperties = {'min': 0.,
                                'max': 1000.,
                                'label': 'z (m)',
                                'intervals': 10,
                                'label size': 9.,
                                'label color': 'Black',
                                'value size': 9.,
                                'value color': 'Black',
                                'lower shift': 5,
                                'upper shift': 5}

        self.slopesAxisProperties = {'min %': 0.,
                                     'max %': 100.,
                                     'min °': 0,
                                     'max °': 90,
                                     'label': 'slope',
                                     'intervals %': 10,
                                     'intervals °': 9,
                                     'label size': 9.,
                                     'label color': 'Black',
                                     'value size': 9.,
                                     'value color': 'Black',
                                     'lower shift %': 5,
                                     'upper shift %': 5,
                                     'lower shift °': 5,
                                     'upper shift °': 5}

        self.grid = {'active': True,
                     'style': 'dashed',
                     'thickness': 0.8,
                     'opacity': 0.5,
                     'order': 1}

        self.legend = {'active': True,
                       'position': 'upper left',
                       'columns': 6,
                       'size': 9.,
                       'frame': True,
                       'opacity': 1}

        self.subdivisions = 1

        self.hspace = 0.125

        self.subplots = []
        
    def __del__(self) :
        Layout.counter -= 1
