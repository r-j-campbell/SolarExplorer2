import numpy as np

class Spectropolarimetric:
    def __init__(self):
        self.Attributes = {
            'S': 4, #num Stokes pts
            'y': 100, #num y pts
            'x': 100, #num x pts
            'wl': 100, #number of wl points
            't':0, #num frames
            'x_sampling': 1, #arcsec/pixel or Mm/pixel
            'y_sampling': 1,
            'x_increment': 1,
            'y_increment': 1,
            'xy_unit': "Arcseconds",
            'wl_dispersion': 1,
            'wl_offset': 0,
            'wl_increment': 1,
            'wl_unit': "Angstroms",
        }
        self.data = np.empty([int(self.Attributes['S']), int(self.Attributes['wl']), int(self.Attributes['y']), int(self.Attributes['x'])])
        self.binary = np.ones((int(self.Attributes['y']), int(self.Attributes['x'])))
        self.current_wl_index = 0
        self.current_frame_index = 0
        self.current_x = 0
        self.current_y = 0
        self.wl_min = 0
        self.wl_max = 100
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.wl_scale_ticks = None
        self.wl_scale_tick_labels = None
        self.x_scale_ticks = None
        self.x_scale_tick_labels = None
        self.y_scale_ticks = None
        self.y_scale_tick_labels = None
    def update_data(self,data):
        self.data=data
    def update_binary(self,binary):
        self.binary=binary

