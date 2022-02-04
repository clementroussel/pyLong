def make_format_z_p(current, other):
    # current and other are axes
    def format_coord(x, y):
        # x, y are data coordinates
        # convert to display coords
        display_coord = current.transData.transform((x,y))
        inv = other.transData.inverted()
        # convert back to data coords with respect to ax
        ax_coord = inv.transform(display_coord)
        coords = [(x, y), ax_coord]
        return ('axe des altitudes : {:<}    axe des pentes : {:<}'
                    .format(*['{:.3f}, {:.3f}'.format(x, y) for x,y in coords]))
    return format_coord

def make_format_z(current):
    def format_coord(x, y):
        display_coord = current.transData.transform((x,y))
        coords = [(x, y)]
        return ('axe des altitudes : {:<}'
                    .format(*['{:.3f}, {:.3f}'.format(x, y) for x,y in coords]))
    return format_coord