
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:01:15 2020

@author: Saad Nafees
"""

from  PyQt5.QtWidgets  import QWidget , QVBoxLayout
from  matplotlib.backends.backend_qt5agg  import  FigureCanvas
from  matplotlib.figure  import  Figure

    
class  dischgwigc ( QWidget ):
    
    def  __init__ ( self ,  parent  =  None ):

        QWidget . __init__ ( self ,  parent )
        
        self . canvas  =  FigureCanvas ( Figure ())
        
        vertical_layout  =  QVBoxLayout () 
        vertical_layout . addWidget ( self . canvas )
        
        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111,position=[0.15, 0.15, 0.75, 0.75] )
        self . setLayout ( vertical_layout )
        
class  dischgwigv ( QWidget ):
    
    def  __init__ ( self ,  parent  =  None ):

        QWidget . __init__ ( self ,  parent )
        
        self . canvas  =  FigureCanvas ( Figure ())
        
        vertical_layout  =  QVBoxLayout () 
        vertical_layout . addWidget ( self . canvas )
        
        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111,position=[0.15, 0.15, 0.75, 0.75] )
        self . setLayout ( vertical_layout )
        
    