#!/usr/bin/env python
from enigma import *
import pytest

MAX_VALUE = 25

class TestRotor():
    def test_construction(self):
        r = Rotor(1, 1)
        assert r.position == 1
        assert r.ring_position == 1

    def test_construction_defaults(self):
        r = Rotor()
        assert r.position == 0
        assert r.ring_position == 0

    def test_construction_position_too_small(self):
        with pytest.raises(AssertionError):
            r = Rotor(-1)

    def test_construction_position_too_large(self):
        with pytest.raises(AssertionError):
            r = Rotor(26)

    def test_construction_rposition_too_small(self):
        with pytest.raises(AssertionError):
            Rotor(0, -1)

    def test_construction_rposition_too_large(self):
        with pytest.raises(AssertionError):
            Rotor(0, 26)

    def test_rotate(self):
        r = Rotor(1)
        r.rotate()
        assert r.position == 2
        
    def test_rotate_rollover(self):
        r = Rotor(25)
        r.rotate()
        assert r.position == 0

    def test_rotate_ring_match(self):
        r = Rotor(10, 10)
        retval = r.rotate()
        assert retval

    def test_forward_data(self):
        r = Rotor() 
        assert len(r.forward_data) == 26

    def test_backward_data(self):
        r = Rotor() 
        assert len(r.backward_data) == 26
        b = r.forward_data[0]
        assert r.backward_data[b] == 0

    def test_forward_less_than_one(self):
        with pytest.raises(AssertionError):
            r = Rotor()
            r.forward(-1)

    def test_forward_greater_than_25(self):
        with pytest.raises(AssertionError):
            r = Rotor()
            r.forward(26)

    def test_forward_at_0(self):
        r = Rotor()
        assert r.forward(0) == r.forward_data[0]

    def test_backward_less_than_one(self):
        with pytest.raises(AssertionError):
            r = Rotor()
            r.backward(-1)

    def test_backward_greater_than_25(self):
        with pytest.raises(AssertionError):
            r = Rotor()
            r.backward(26)

    def test_backward_at_0(self):
        r = Rotor()
        assert r.backward(0) == r.backward_data[0]