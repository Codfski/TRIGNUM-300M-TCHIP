"""
TRIGNUM Core - Subtractive Semantic Geometry for Cold-State AGI
v.300M

The foundational Python implementation of the Trignum framework.
"""

__version__ = "0.300.0"
__author__ = "Trace on Lab"
__license__ = "MIT"

from .pyramid import TrignumPyramid
from .faces import FaceAlpha, FaceBeta, FaceGamma
from .magnetic_field import MagneticField
from .subtractive_filter import SubtractiveFilter
from .tchip_emulator import TCHIP

__all__ = [
    "TrignumPyramid",
    "FaceAlpha",
    "FaceBeta",
    "FaceGamma",
    "MagneticField",
    "SubtractiveFilter",
    "TCHIP",
]
