"""
patch_numpy.py
──────────────
Patch de compatibilité NumPy / scikit-learn.

Les fichiers .pkl ont été entraînés sous Google Colab avec :
  - scikit-learn 1.6.1
  - NumPy 2.x

Ce module DOIT être importé en tout premier dans app.py,
avant tout autre import, pour éviter l'erreur :
  "MT19937 is not a known BitGenerator module"
"""

import sys
import numpy
import numpy.random


def apply():
    """Applique tous les patches de compatibilité NumPy."""

    #  Redirige les anciens chemins de modules vers les actuels
    sys.modules["numpy.random._mt19937"]          = numpy.random._mt19937
    sys.modules["numpy.random._common"]           = numpy.random._common
    sys.modules["numpy.random._bounded_integers"] = numpy.random._bounded_integers

    #  Enregistre MT19937 et PCG64 dans le registre BitGenerators
    try:
        from numpy.random import _pickle as np_pickle, MT19937, PCG64
        for name, cls in [("MT19937", MT19937), ("PCG64", PCG64)]:
            if name not in np_pickle.BitGenerators:
                np_pickle.BitGenerators[name] = cls
    except Exception:
        pass  # Versions futures de NumPy : patch inutile, on ignore silencieusement
