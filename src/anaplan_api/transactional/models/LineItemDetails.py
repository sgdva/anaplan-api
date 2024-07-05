from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class LineItemsDetails:
    _moduleId: str
    _moduleName: str
    _id: str
    _name: str
    _isSummary: bool
    _startOfSection: bool
    _broughtForward: bool
    _useSwitchover: bool
    _breakback: bool
    _cellCount: int
    _version: dict
    _appliesTo: List[dict]
    _dataTags: List[dict]
    _referencedBy: List[dict]
    _parent: dict
    _readAccessDriver: dict
    _writeAccessDriver: dict
    _formula: str
    _format: str
    _formatMetadata: dict
    _summary: str
    _timeScale: str
    _timeRange: str
    _formulaScope: str
    _style: str
    _code: str
    _notes: str

    @property
    def module_id(self):
        return self._moduleId

    @property
    def module_name(self):
        return self._moduleName

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def is_summary(self):
        return self._isSummary

    @property
    def start_of_section(self):
        return self._startOfSection

    @property
    def brought_forward(self):
        return self._broughtForward

    @property
    def use_switchover(self):
        return self._useSwitchover

    @property
    def breakback(self):
        return self._breakback

    @property
    def cell_count(self):
        return self._cellCount

    @property
    def version(self):
        return self._version

    @property
    def applies_to(self):
        return self._appliesTo

    @property
    def data_tags(self):
        return self._dataTags

    @property
    def referenced_by(self):
        return self._referencedBy

    @property
    def parent(self):
        return self._parent

    @property
    def read_access_driver(self):
        return self._readAccessDriver

    @property
    def write_access_driver(self):
        return self._writeAccessDriver

    @property
    def formula(self):
        return self._formula

    @property
    def format(self):
        return self._format

    @property
    def format_metadata(self):
        return self._formatMetadata

    @property
    def summary(self):
        return self._summary

    @property
    def time_scale(self):
        return self._timeScale

    @property
    def time_range(self):
        return self._timeRange

    @property
    def formula_scope(self):
        return self._formulaScope

    @property
    def style(self):
        return self._style

    @property
    def code(self):
        return self._code

    @property
    def notes(self):
        return self._notes
