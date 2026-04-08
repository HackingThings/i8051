from __future__ import absolute_import
from binaryninja import Architecture
from .architecture import MCS51
from .binaryview import Family8051View
from .experiments.calling_conventions import SDCCCall, KeilCall, IARCall
from .experiments.calling_conventions import YoloCall
from .devices import surface_ec, coastermelt, inic_3609, vl811

__version__ = '0.0.1'
__all__ = ['MCS51']

MCS51.register()
Family8051View.register()


def _register_calling_conventions(arch):
    """Register architecture/platform calling conventions in a BN 5.x-safe way."""
    platform = arch.standalone_platform
    conventions = {}

    for cc_cls in (SDCCCall, KeilCall, IARCall, YoloCall):
        cc = cc_cls(arch, cc_cls.name)
        arch.register_calling_convention(cc)
        # BN 5.x prefers conventions to be registered with the platform too.
        if hasattr(platform, 'register_calling_convention'):
            platform.register_calling_convention(cc)
        conventions[cc_cls.name] = cc

    yolo_cc = conventions[YoloCall.name]
    platform.default_calling_convention = yolo_cc
    platform.system_calling_convention = yolo_cc


_register_calling_conventions(Architecture['8051'])
