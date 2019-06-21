from __future__ import annotations

from typing import Union, Collection, Dict, Any, Callable
from numbers import Number

from mcts import Mcts
from nodes import IntNode, FloatNode

number_or_callable = Union[Callable[[Any], Number], Number]

class ControlledParam:
    """
    Controlled parameter automatically searches for and takes values resulting in better outcomes.
    """
    ctrl_values: Dict[Any, Collection[ControlledParam]] = {}

    @staticmethod
    def init(unit, cps: Collection[ControlledParam]):
        ControlledParam.ctrl_values[unit] = cps
        for cp in cps:
            cp._init(unit)

    @staticmethod
    def step(unit, result):
        cps = ControlledParam.ctrl_values[unit]
        for cp in cps:
            cp._step(unit, result)

    def __init__(self, param_name: str, min: number_or_callable, max: number_or_callable,
                 exponential = False, integer = False):
        prefix = self.__class__.__name__
        self.min = min
        self.max = max
        self.integer = integer
        self.exponential = exponential

        self.mcts_storage_name = f"{prefix}_mcts_{param_name}"
        self.curval_storage_name = f"{prefix}_curval_{param_name}"

    def _decide(self, unit):
        mc: Mcts = getattr(unit, self.mcts_storage_name)
        action = mc.decide()
        if self.exponential:
            action = 10 ** action
        setattr(unit, self.curval_storage_name, action)

    def _step(self, unit, result):
        mc: Mcts = getattr(unit, self.mcts_storage_name)
        mc.register(result)
        self._decide(unit)

    def _init(self, unit):

        try:
            min = self.min(unit)
        except TypeError:
            min = self.min

        try:
            max = self.max(unit)
        except TypeError:
            max = self.max


        if self.integer:
            interval = IntNode(min, max)
        else:
            interval = FloatNode(min, max)

        mc = Mcts(interval)
        setattr(unit, self.mcts_storage_name, mc)
        self._decide(unit)

    def __get__(self, unit, _):
        return getattr(unit, self.curval_storage_name)

    def __set__(self, unit, value):
        raise Exception("Can't set value of controlled parameter")

