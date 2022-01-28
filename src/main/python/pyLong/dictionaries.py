""" --> styles de ligne <-- """
lineStyles = {'solide' : '-',
              'tiretée' : '--',
              'tiretée et pointillée' : '-.',
              'pointillée' : ':'}

""" --> styles de marqueur <-- """
styles2marqueur = {'point' : '.',
                   'plus' : '+',
                   'pixel': ',',
                   'croix': 'x',
                   'cercle': 'o',
                   'losange': 'D',
                   'losange étroit': 'd',
                   'octogone': '8',
                   'carré': 's',
                   'pentagone': 'p',
                   'étoile': '*',
                   'ligne verticale': '|',
                   'ligne horizontale': '_',
                   'hexagone 1': 'h',
                   'hexagone 2': 'H',
                   'triangle gauche': '<',
                   'triangle droite': '>',
                   'triangle haut': '^',
                   'triangle bas': 'v',
                   'tri-marqueur gauche': '3',
                   'tri-marqueur droite': '4',
                   'tri-marqueur haut': '2',
                   'tri-marqueur bas': '1',
                   'aucun': 'None'}

""" --> placement de la légende <-- """
placementsLegende = {'haut droite': ('upper right', (1,1)),
                     'haut gauche': ('upper left', (0,1)),
                     'bas gauche': ('lower left', (0,0)),
                     'bas droite': ('lower right', (1,0)),
                     'centre droite': ('center right', (1,0.5)),
                     'centre gauche': ('center left', (0,0.5)),
                     'centre bas': ('lower center', (0.5,0)),
                     'centre haut': ('upper center', (0.5,1)),
                     'centre': ('center', (0.5,0.5))}

""" --> délimiteurs <-- """
delimiteurs = {'espace' : ' ',
               'tabulation' : '\t',
               'virgule' : ',',
               'point virgule' : ';'}

""" --> séparateurs décimal <-- """
separateurs = {'point' : '.',
               'virgule' : ','}

""" --> extensions <-- """
extensions = {'pdf' : 'Portable Document Format',
              'png' : 'Portable Network Graphics',
              'eps' : 'Encapsulated PostScript',
              'svg' : 'Scalable Vector Graphics'}

""" --> couleurs HTML <-- """
colors = {'Pink' : '#FFC0CB',
          'Deep Pink' : '#FF1493',
          'Violet' : '#EE82EE',
          'Dark Violet' : '#9400D3',
          'Rebecca Purple' : '#663399',
          'Magenta' : '#FF00FF',
          'Dark Magenta' : '#8B008B',
          'Purple' : '#800080',
          'Indigo' : '#4B0082',
          'Indian Red' : '#CD5C5C',
          'Red' : '#FF0000',
          'Crimson' : '#DC143C',
          'Dark Red' : '#8B0000',
          'Orange' : '#FFA500',
          'Dark Orange' : '#FF8C00',
          'Orange Red' : '#FF4500',
          'Yellow' : '#FFFF00',
          'Gold' : '#FFD700',
          'Khaki': '#F0E68C',
          'Dark Khaki' : '#BDB76B',
          'Green' : '#008000',
          'Dark Green' : '#006400',
          'Lime Green' : '#32CD32',
          'Chartreuse' : '#7FFF00',
          'Forest Green' : '#228B22',
          'Olive' : '#808000',
          'Cyan' : '#00FFFF',
          'Dark Cyan' : '#008B8B',
          'Turquoise' : '#40E0D0',
          'Dark Turquoise' : '#00CED1',
          'Blue' : '#0000FF',
          'Dark Blue' : '#00008B',
          'Cadet Blue' : '#5F9EA0',
          'Steel Blue' : '#4682B4',
          'Deep Sky Blue' : '#00BFFF',
          'Brown' : '#A52A2A',
          'Sandy Brown' : '#F4A460',
          'Chocolate' : '#D2691E',
          'Peru' : '#CD853F',
          'Maroon' : '#800000',
          'Gray' : '#808080',
          'Silver' : '#C0C0C0',
          'Black' : '#000000',
          'White' : '#FFFFFF'}

""" --> trio couleurs HTML <-- """
triosCouleur = {'Green,Orange,Red' : ['#008000','#FFA500','#FF0000'],
                'Dark Green,Dark Orange,Dark Red' : ['#006400','#FF8C00','#8B0000'],
                'Forest Green,Orange Red,Crimson' : ['#228B22','#FF4500','#DC143C'],
               }