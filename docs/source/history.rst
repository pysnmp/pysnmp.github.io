History and naming
==================

PySNMP was written by `Ilya Etingof <https://github.com/etingof>`_, starting in
1999, and the project was sponsored early on by a
`Python Software Foundation <https://www.python.org/psf/>`_ grant. pysmi and
pyasn1 came out of the same work: a SNMP engine needs an ASN.1 codec and a way
to read MIB modules, and neither existed in Python.

Ilya `died on 10 August 2022
<https://lists.openstack.org/pipermail/openstack-discuss/2022-August/030062.html>`_.
His code was, and is, in wide use. More than one group picked up maintenance
afterwards, independently, which is the reason for the section below.

Everything here remains under the 2-clause BSD license it has always carried.

Which package am I looking at?
------------------------------

Several packages on PyPI descend from Ilya's code. They are not the same
software and they do not share a version number, so the name you install
decides which one you get.

This organization -- `github.com/pysnmp <https://github.com/pysnmp>`_ --
maintains and publishes:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40
   :class: project-table

   * - PyPI package
     - Repository
     - Imported as
   * - `pysnmplib <https://pypi.org/project/pysnmplib/>`_
     - :repo:`pysnmp`
     - ``pysnmp``
   * - `pysnmp-pysmi <https://pypi.org/project/pysnmp-pysmi/>`_
     - :repo:`pysmi`
     - ``pysmi``
   * - `pysnmp-pyasn1 <https://pypi.org/project/pysnmp-pyasn1/>`_
     - :repo:`pyasn1`
     - ``pyasn1``

The import names are unchanged from Ilya's originals, which is deliberate --
existing code keeps working -- and it is also why the distribution names had to
differ from the ones already on PyPI.

Other forks exist. The ``pysnmp``, ``pysmi`` and ``pyasn1`` names on PyPI are
published by other maintainers, and `pysnmp.com <https://www.pysnmp.com/>`_ and
`docs.lextudio.com <https://docs.lextudio.com/snmp/>`_ are theirs. If you
installed one of those, their documentation is the one that describes what you
have; issues about it are best raised with them, and issues about the packages
listed above are best raised here.

This site, and everything under
`pysnmp.github.io <https://pysnmp.github.io/>`_, documents the packages in the
table.
