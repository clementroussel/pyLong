class Subplot:
    def __init__(self):
        self.id = ""

        self.subdivisions = 1

        self.yAxisProperties = {'min': -100.,
                                'max': 100.,
                                'label': '',
                                'intervals': 5,
                                'label color': 'Black',
                                'value color': 'Black',
                                'lower shift': 0,
                                'upper shift': 0}
        
        self.legend = {'active': True,
                       'position': 'upper left',
                       'columns': 6}
