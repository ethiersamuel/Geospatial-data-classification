# -*- coding: utf-8 -*-
"""Tests for classify"""
import subprocess
import pytest


def test_run():
    """test that the program runs with the expected args"""
    run_classify = subprocess.check_call(
        ['python', 'classify.py'], stdout=subprocess.DEVNULL
    )
    assert run_classify == 0


def test_valid_landcover():
    """test that the program runs with the expected landcover optional arg"""
    run_classify = subprocess.check_call(
        ['python', 'classify.py', '--landcover', 'water'], stdout=subprocess.DEVNULL
    )
    assert run_classify == 0


def test_no_landcover():
    """test that landcover with no value raises error"""
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(
            ['python', 'classify.py', '--landcover'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )


def test_water():
    """test water landcover (returns 0)"""
    output = subprocess.check_output(['python', 'classify.py', '--landcover', 'water'])
    assert 'water' in output.decode('utf-8').lower()
    assert '0' in output.decode('utf-8')


def test_woody_savannas():
    """test specific landcover"""
    output = subprocess.check_output(['python', 'classify.py', '--landcover', 'woody savannas'])
    assert 'woody savannas' in output.decode('utf-8').lower()
    # this test will pass if greater precision is used
    assert '130' in output.decode('utf-8')
    assert '58.40' not in output.decode('utf-8')


def test_woody_savannas_with_stddev():
    """test specific landcover with stddev optional arg"""
    output = subprocess.check_output(
        ['python', 'classify.py', '--landcover', 'woody savannas', '--stddev']
    )
    assert 'woody savannas' in output.decode('utf-8').lower()
    assert '130' in output.decode('utf-8')
    assert '58.40' in output.decode('utf-8')
