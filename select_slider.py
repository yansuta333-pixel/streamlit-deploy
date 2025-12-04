import numpy as np
from PIL import Image,ImageColor
import streamlit as st

class Color:
    def __init__(self, name):
        self.name = name.lower()
        self.rgb = ImageColor.getrgb(self.name)
        self.image = Image.new('RGB', (50, 50), self.name)
        self.hue = ImageColor.getcolor(self.name, 'HSV')[0]

    def __str__(self):
        return self.name
    
    def __lt__(self, other):
        return self.hue < other.hue
    
    def get_image(self):
        return self.image

    def get_rgb(self):
        return self.rgb
    
    def get_hue(self):
        return self.hue
    

colors = sorted([Color(c) for c in ImageColor.colormap.keys()])

selected = st.select_slider('HTML/CSS色名', colors)
if selected:
    st.image(selected.get_image())
    st.markdown(f'''
        {selected} "{selected.get_rgb()}" Hue={selected.get_hue()}''')