The MIB archive
===============

SNMP names things in MIB modules, and a program that wants to say
``IF-MIB::ifInOctets`` instead of ``1.3.6.1.2.1.2.2.1.10`` needs the module
that defines it. :repo:`mibs` is where this organization publishes those
modules, and it is what pysmi and pysnmp fetch from when one is not on disk.

Fetching a module
-----------------

Modules are served over HTTPS, one file per module, named after the module
with no extension:

.. code-block:: console

   $ curl -O https://pysnmp.github.io/mibs/asn1/IF-MIB
   $ head -1 IF-MIB
   IF-MIB DEFINITIONS ::= BEGIN

There is no directory index -- the tree is generated, and a listing of several
thousand files would not be much use anyway. To see what is there, browse the
:repo:`mibs` repository.

How the libraries use it
------------------------

Both libraries take a list of *sources*, each written as a URL template with
``@mib@`` standing in for the module name. The archive is the default last
entry, after whatever is on the local filesystem:

.. code-block:: console

   $ mibdump --generate-mib-texts --destination-format json IF-MIB
   Source MIB repositories: file:///usr/share/snmp/mibs, https://pysnmp.github.io/mibs/asn1/@mib@

So a module already in ``/usr/share/snmp/mibs`` is read from there, and only a
module that is missing locally is fetched. The same template can be given to
pysmi's API directly:

.. code-block:: python

   from pysmi.reader import HttpReader

   mibCompiler.add_sources(HttpReader("https://pysnmp.github.io/mibs/asn1/@mib@"))

Point it somewhere else -- a directory, a ZIP archive, an internal HTTP
server -- when your MIBs are not public ones. Most vendor MIBs are not.

What is and is not in here
--------------------------

The archive carries the standard modules and the widely-published vendor ones.
It is not a complete index of every MIB ever written, and a module that a
device's own documentation ships is best taken from there: the archive's copy
of a vendor MIB is a snapshot, and the vendor's is authoritative.

pysnmp does not depend on the archive to start. The modules its engine
resolves during start-up are compiled into the package already, which is why
an engine starts on a machine with no network access. The archive matters when
you are compiling a module you do not have, which is what
``pip install --pre 'pysnmplib[compile]'`` and pysmi are for.

.. warning::

   A MIB module compiled by pysmi becomes Python that pysnmp imports. Treat an
   ASN.1 MIB source the way you would treat any other code you are about to
   run, and compile from somewhere you trust.

Contributing a module
---------------------

Missing modules and corrections go to the :repo:`mibs` repository as pull
requests. Include where the module came from, so the next person can tell a
vendor's own publication from a transcription.
