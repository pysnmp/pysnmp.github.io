pysnmp
======

.. rst-class:: lead

   Pure-Python SNMP. An engine that speaks v1, v2c and v3, and a MIB
   distribution that lets it talk about managed objects by name instead of by
   number. No C extensions and no Net-SNMP bindings.

Two of the four repositories here are what you install and use directly:

.. list-table::
   :header-rows: 1
   :widths: 12 30 16 42
   :class: project-table

   * - Project
     - Install
     - Documentation
     - What it is
   * - :repo:`pysnmp`
     - ``pip install 'pysnmplib[compile]'``
     - :docs:`pysnmp`
     - The engine. SNMP v1, v2c and v3 as manager, agent or proxy, on asyncio.
   * - :repo:`mibs`
     - served, not installed
     - :doc:`the distribution <mibs>`
     - The MIB distribution: thousands of modules over HTTPS, as an archive,
       and as OCI images.

The other two sit underneath and most people never import them. pysnmp pulls
in what it needs:

.. list-table::
   :header-rows: 1
   :widths: 12 30 16 42
   :class: project-table

   * - Project
     - Install
     - Documentation
     - What it is
   * - :repo:`pysmi`
     - with ``pysnmplib[compile]``
     - :docs:`pysmi`
     - The MIB compiler. Turns ASN.1 MIB sources into pysnmp modules or JSON.
   * - :repo:`pyasn1`
     - with ``pysnmplib``
     - :docs:`pyasn1`
     - The codec. ASN.1 types with BER, CER and DER.

Reach for them directly when you are compiling MIBs outside an engine, or
using ASN.1 for something that is not SNMP at all.

Start here
----------

.. code-block:: console

   $ pip install 'pysnmplib[compile]'

The ``compile`` extra pulls in pysmi. Without it pysnmp still speaks SNMP --
it ships the standard modules an engine resolves at start-up -- but it cannot
read a MIB it does not already have, and reading those is most of what makes
SNMP legible. Install it plain (``pip install pysnmplib``) only if you know
you will never name an object outside the standard set.

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

An SNMP engine speaks a binary protocol about objects named in MIB modules,
so there are three layers. You use the top one:

**pysnmp** is the engine: message processing for v1, v2c and v3, USM
authentication and privacy, VACM access control, the transport dispatcher,
and the high-level API above all of it.

**pysmi** reads ASN.1 MIB sources -- SMIv1, SMIv2 and the dialects vendors
actually ship -- and renders them as pysnmp modules or JSON. It is what turns
``IF-MIB::ifInOctets`` from a string into an object identifier and a type.
pysnmp drives it for you; you call it directly only to compile MIBs outside
an engine, with ``mibdump``.

**pyasn1** encodes and decodes: BER on the wire, CER and DER where a
representation has to be reproducible byte for byte. Nothing in normal use
reaches this layer by hand.

And underneath all three, **mibs** supplies the module definitions themselves.
An engine works without it, on the standard modules pysnmp ships; it is what
you add when you want to name a vendor's objects rather than count OID arcs.
See :doc:`mibs`.

.. toctree::
   :maxdepth: 2
   :caption: This site

   projects
   mibs
   community
   history
