from abc import ABC

import pytest
from .cnc_machine_base import Machine, JsonMachineWorker, TxtMachineWorker, XmlMachineWorker


def test_machine_is_abs_class():
    assert issubclass(Machine, ABC)

@pytest.mark.parametrize(
    'classe',
    [
        Machine,
        JsonMachineWorker,
        TxtMachineWorker,
        XmlMachineWorker,
    ]
)
def test_machine_class_attr_valids(classe):
    assert hasattr(classe, '_core_generator')
    assert hasattr(classe, '_work_report')
    assert hasattr(classe, 'make_part')
    assert hasattr(classe, 'type')
