The MIB distribution
====================

SNMP names things in MIB modules. Without the module that defines it, an agent
answering ``1.3.6.1.2.1.2.2.1.8.1`` tells you the value is ``2``; with it, the
same answer reads ``IF-MIB::ifOperStatus.1 = down``. :repo:`mibs` is where this
organization publishes those modules.

It is a distribution rather than a package: nothing to ``pip install``, several
ways to get at the same content.

- **Over HTTPS**, one module per request, which is what pysmi fetches from by
  default. No index -- the tree is generated, and a listing of several thousand
  files would not help anyone. Browse :repo:`mibs` to see what is there.
- **As an archive**, for build systems and air-gapped sites that would rather
  fetch once than reach out per module.
- **As OCI images**, to mount alongside a container that needs the modules
  without giving it egress.

The examples below use the HTTPS channel because it needs no setup.

Resolving a name
----------------

This is the everyday reason to care. ``IF-MIB`` is not one of the modules
pysnmp ships, so naming an object in it needs pysmi and a source to read
from:

.. code-block:: python

   from pysnmp.smi import builder, compiler, rfc1902, view

   mibBuilder = builder.MibBuilder()
   compiler.addMibCompiler(
       mibBuilder, sources=["https://pysnmp.github.io/mibs/asn1/@mib@"]
   )
   mibView = view.MibViewController(mibBuilder)

   identity = rfc1902.ObjectIdentity("IF-MIB", "ifInOctets", 1)
   identity.resolveWithMib(mibView)

   print(identity.getOid())

.. code-block:: text

   1.3.6.1.2.1.2.2.1.10.1

The ``@mib@`` in the source is a placeholder pysmi substitutes with the module
name it wants. The first resolution compiles ``IF-MIB``; later ones read the
compiled copy. Hand the same ``ObjectIdentity`` to ``getCmd`` or ``nextCmd``
and you are polling by name.

Translating a trap
------------------

A notification arrives as bare numbers. Turning it into something a human or a
log pipeline can read is the same machinery in reverse, with one wrinkle worth
knowing: **an OID carries no hint of which module defines it**, so the modules
you care about have to be loaded before the lookup can succeed. Resolving
against an empty builder raises ``SmiError: ... (MIB not loaded?)``.

.. code-block:: python

   from pysnmp.smi import builder, compiler, rfc1902, view

   mibBuilder = builder.MibBuilder()
   compiler.addMibCompiler(
       mibBuilder, sources=["https://pysnmp.github.io/mibs/asn1/@mib@"]
   )
   # Load what this receiver expects to see. Without this the reverse lookup
   # has nothing to search.
   mibBuilder.loadModules("SNMPv2-MIB", "IF-MIB")
   mibView = view.MibViewController(mibBuilder)

   # What a linkDown trap actually carries on the wire.
   varBinds = [
       ("1.3.6.1.6.3.1.1.4.1.0", "1.3.6.1.6.3.1.1.5.3"),
       ("1.3.6.1.2.1.2.2.1.1.1", 1),
       ("1.3.6.1.2.1.2.2.1.8.1", 2),
   ]

   for oid, value in varBinds:
       varBind = rfc1902.ObjectType(rfc1902.ObjectIdentity(oid), value)
       varBind.resolveWithMib(mibView)
       print(varBind.prettyPrint())

.. code-block:: text

   SNMPv2-MIB::snmpTrapOID.0 = IF-MIB::linkDown
   IF-MIB::ifIndex.1 = 1
   IF-MIB::ifOperStatus.1 = down

Note the last line. ``2`` became ``down`` because the textual convention in
``IF-MIB`` says so -- the distribution gives you the enumeration labels, not
just the names.

Pointing pysmi somewhere else
-----------------------------

The source is a list, and the first hit wins, so a local directory in front of
the published tree is how you override a module or work offline:

.. code-block:: python

   compiler.addMibCompiler(
       mibBuilder,
       sources=[
           "/usr/share/snmp/mibs",
           "https://pysnmp.github.io/mibs/asn1/@mib@",
       ],
   )

The same list is what ``mibdump`` takes on the command line. Most vendor MIBs
are not public, so this is the normal arrangement rather than the exception.

What is and is not here
-----------------------

The standard modules and the widely published vendor ones. Not every MIB ever
written, and where a device ships its own, that copy is authoritative -- the
distribution's is a snapshot.

An engine does not need any of it to start. The modules pysnmp resolves during
start-up are compiled into the package, which is why ``pip install pysnmplib``
works on a machine with no network. The distribution matters the moment you
want to name something outside that set.

.. warning::

   A MIB module compiled by pysmi becomes Python that pysnmp imports. Treat an
   ASN.1 MIB source the way you would treat any other code you are about to
   run, and compile from somewhere you trust.

Contributing a module
---------------------

Missing modules and corrections go to :repo:`mibs` as pull requests. Say where
the module came from, so the next person can tell a vendor's own publication
from a transcription.
