import re

class Analysis:
    def __init__(self):
        self.template_fn = ''
        self.method = 'one at a time'
        self.base_params = {}
        self.output_fn = ''
        self.command = ''
        
        self.template_extension = '.template'
        
        self.variation_size = 1e-2
        
    def start(self, verbose=True):
        
