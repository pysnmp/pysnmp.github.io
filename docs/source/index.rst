pysnmp
======

.. rst-class:: lead

   Pure-Python SNMP, from the wire up: an SNMP engine, the MIB compiler that
   feeds it, the ASN.1 codec underneath both, and the MIB archive they read
   from. No C extensions and no Net-SNMP bindings -- Python all the way down.

.. list-table::
   :header-rows: 1
   :widths: 12 26 20 42
   :class: project-table

   * - Project
     - Install
     - Documentation
     - What it is
   * - :repo:`pysnmp`
     - ``pip install --pre pysnmplib``
     - :docs:`pysnmp`
     - SNMP v1/v2c/v3 engine -- manager, agent and proxy, asyncio throughout.
   * - :repo:`pysmi`
     - ``pip install pysnmp-pysmi``
     - :docs:`pysmi`
     - MIB compiler: ASN.1 SMIv1/SMIv2 sources into pysnmp modules or JSON.
   * - :repo:`pyasn1`
     - ``pip install pysnmp-pyasn1``
     - :docs:`pyasn1`
     - ASN.1 types and BER/CER/DER codecs -- what the other two are built on.
   * - :repo:`mibs`
     - --
     - :doc:`the archive <mibs>`
     - The MIB modules pysmi and pysnmp fetch when one is not on disk.

Start here
----------

.. code-block:: console

   $ pip install --pre pysnmplib

.. note::

   ``--pre`` is not decoration. pysnmp 6.0 is in release candidate and is the
   line being maintained: it is what the code below runs on and what the rest
   of this site describes. A plain ``pip install pysnmplib`` resolves 5.0.24,
   whose ``pysnmp-pyasn1`` requirement predates the current releases of that
   package and which fails to import against the one it pulls in. Drop the
   flag once 6.0 is generally available.

.. code-block:: python

   import asyncio

   from pysnmp.hlapi.asyncio import *


   async def run():
       snmpEngine = SnmpEngine()
       errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
           snmpEngine,
           CommunityData("public", mpModel=0),
           UdpTransportTarget(("localhost", 161)),
           ContextData(),
           ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
       )

       for varBind in varBinds:
           print(" = ".join(x.prettyPrint() for x in varBind))

       snmpEngine.transportDispatcher.closeDispatcher()


   asyncio.run(run())

That is the high-level API, which is where almost everyone should start. Under
it sits the v3 architecture -- message processing, security models, access
control -- addressable directly when you need to build something the
high-level API does not cover, such as a proxy or a command responder.

Runnable versions of this and a few hundred others live in the
`examples directory <https://github.com/pysnmp/pysnmp/tree/main/examples>`_ of
the pysnmp repository, and are rendered into the
:docs:`pysnmp`.

How the pieces fit
------------------

An SNMP engine speaks a binary protocol about objects named in MIB modules, so
there are three layers, and they are three repositories:

**pyasn1** encodes and decodes. BER on the wire; CER and DER where a
representation has to be reproducible byte for byte.

**pysmi** reads ASN.1 MIB sources -- SMIv1, SMIv2, and the dialects real
vendors actually ship -- and renders them as pysnmp modules or as JSON. It is
what turns ``IF-MIB::ifInOctets`` from a string into an object identifier and
a type.

**pysnmp** is the engine above both: message processing for v1, v2c and v3,
USM authentication and privacy, VACM access control, the transport dispatcher,
and the high-level API.

**mibs** is the archive the other two fall back to when a module is not on
disk. See :doc:`mibs`.

pysnmp ships the standard MIB modules its engine resolves at start-up, so an
engine starts with neither pysmi nor the archive present. Compiling vendor
MIBs while the engine is running is the extra:
``pip install --pre 'pysnmplib[compile]'``.

.. toctree::
   :maxdepth: 2
   :caption: This site

   projects
   mibs
   community
   history
