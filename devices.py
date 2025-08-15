from collections.abc import Callable
from enum import StrEnum, auto

import svg

import supernote_nomad
import supernote_manta
import remarkable_2


class Device(StrEnum):
    Nomad = auto()
    Manta = auto()
    Remarkable2 = auto()

    @property
    def mm(self) -> float:
        match self:
            case Device.Nomad:
                return supernote_nomad.MM
            case Device.Manta:
                return supernote_manta.MM
            case Device.Remarkable2:
                return remarkable_2.MM

    @property
    def border(self) -> Callable[[], svg.Element]:
        match self:
            case Device.Nomad:
                return supernote_nomad.border
            case Device.Manta:
                return supernote_manta.border
            case Device.Remarkable2:
                return remarkable_2.border

    @property
    def screen_width(self) -> float:
        match self:
            case Device.Nomad:
                return supernote_nomad.SCREEN_WIDTH
            case Device.Manta:
                return supernote_manta.SCREEN_WIDTH
            case Device.Remarkable2:
                return remarkable_2.SCREEN_WIDTH

    @property
    def screen_height(self) -> float:
        match self:
            case Device.Nomad:
                return supernote_nomad.SCREEN_HEIGHT
            case Device.Manta:
                return supernote_manta.SCREEN_HEIGHT
            case Device.Remarkable2:
                return remarkable_2.SCREEN_HEIGHT
