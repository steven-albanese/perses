"""
Samplers for perses automated molecular design.

TODO: Refactor tests into a test class so that AlanineDipeptideSAMS test system only needs to be constructed once for a battery of tests.

"""

__author__ = 'John D. Chodera'

################################################################################
# IMPORTS
################################################################################

from simtk import openmm, unit
from simtk.openmm import app
import os, os.path
import sys, math
import numpy as np
import logging
from functools import partial

import perses.tests.testsystems

import perses.rjmc.topology_proposal as topology_proposal
import perses.bias.bias_engine as bias_engine
import perses.rjmc.geometry as geometry
import perses.annihilation.ncmc_switching as ncmc_switching

################################################################################
# TEST MCMCSAMPLER
################################################################################

def test_alanine_dipeptide_samplers():
    """
    Test samplers on alanine dipeptide test system.
    """
    # Retrieve the test system.
    from perses.tests.testsystems import AlanineDipeptideTestSystem
    testsystem = AlanineDipeptideTestSystem()
    # Test MCMCSampler samplers.
    for environment in testsystem.environments:
        mcmc_sampler = testsystem.mcmc_samplers[environment]
        f = partial(mcmc_sampler.run)
        f.description = "Testing MCMC sampler with alanine dipeptide '%s'" % environment
        yield f
    # Test ExpandedEnsembleSampler samplers.
    for environment in testsystem.environments:
        exen_sampler = testsystem.exen_samplers[environment]
        f = partial(exen_sampler.run)
        f.description = "Testing expanded ensemble sampler with alanine dipeptide '%s'" % environment
        yield f
    # Test SAMSSampler samplers.
    for environment in testsystem.environments:
        sams_sampler = testsystem.sams_samplers[environment]
        f = partial(exen_sampler.run)
        f.description = "Testing SAMS sampler with alanine dipeptide '%s'" % environment
        yield f
    # Test MultiTargetDesign sampler for implicit hydration free energy
    from perses.samplers.samplers import MultiTargetDesign
    # Construct a target function for identifying mutants that maximize the peptide implicit solvent hydration free energy
    for environment in testsystem.environments:
        target_samplers = { testsystem.sams_samplers[environment] : 1.0, testsystem.sams_samplers['vacuum'] : -1.0 }
        designer = MultiTargetDesign(target_samplers)
        f = partial(designer.run)
        f.description = "Testing MultiTargetDesign sampler with alanine dipeptide mutation transfer free energy from vacuum -> %s" % environment
        yield f

def test_alkanes_samplers():
    """
    Test samplers on alkanes test system.
    """
    # Retrieve the test system.
    from perses.tests.testsystems import AlanineDipeptideTestSystem
    testsystem = AlanineDipeptideTestSystem()
    # Test MCMCSampler samplers.
    for environment in testsystem.environments:
        mcmc_sampler = testsystem.mcmc_samplers[environment]
        f = partial(mcmc_sampler.run)
        f.description = "Testing MCMC sampler with alkanes '%s'" % environment
        yield f
    # Test ExpandedEnsembleSampler samplers.
    for environment in testsystem.environments:
        exen_sampler = testsystem.exen_samplers[environment]
        f = partial(exen_sampler.run)
        f.description = "Testing expanded ensemble sampler with alkanes '%s'" % environment
        yield f
    # Test SAMSSampler samplers.
    for environment in testsystem.environments:
        sams_sampler = testsystem.sams_samplers[environment]
        f = partial(exen_sampler.run)
        f.description = "Testing SAMS sampler with alkanes '%s'" % environment
        yield f
    # Test MultiTargetDesign sampler for implicit hydration free energy
    from perses.samplers.samplers import MultiTargetDesign
    # Construct a target function for identifying mutants that maximize the peptide implicit solvent hydration free energy
    for environment in testsystem.environments:
        target_samplers = { testsystem.sams_samplers[environment] : 1.0, testsystem.sams_samplers['vacuum'] : -1.0 }
        designer = MultiTargetDesign(target_samplers)
        f = partial(designer.run)
        f.description = "Testing MultiTargetDesign sampler with alkanes mutation transfer free energy from vacuum -> %s" % environment
        yield f
