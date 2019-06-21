from __future__ import annotations
from typing import Union, Collection, Dict, Any
from mcts import Mcts, Node
import copy



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

    def __init__(self, param_name: str, interval: Node):
        prefix = self.__class__.__name__
        self.interval = interval
        self.mcts_storage_name = f"{prefix}_mcts_{param_name}"
        self.curval_storage_name = f"{prefix}_curval_{param_name}"

    def _decide(self, unit):
        mc: Mcts = getattr(unit, self.mcts_storage_name)
        action = mc.decide()
        setattr(unit, self.curval_storage_name, action)

    def _step(self, unit, result):
        mc: Mcts = getattr(unit, self.mcts_storage_name)
        mc.register(result)
        self._decide(unit)

    def _init(self, unit):
        mc = Mcts(copy.deepcopy(self.interval))
        setattr(unit, self.mcts_storage_name, mc)
        self._decide(unit)

    def __get__(self, unit, _) -> Union[float, None]:
        return getattr(unit, self.curval_storage_name)

    def __set__(self, unit, value):
        raise Exception("Can't set value of controlled parameter")

