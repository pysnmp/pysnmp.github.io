Projects
========

Four repositories, one toolchain. Each publishes its own versioned
documentation; this page says what each one is for and when you would reach
for it directly.

pysnmp
------

:Repository: :repo:`pysnmp`
:PyPI: `pysnmplib <https://pypi.org/project/pysnmplib/>`_
:Documentation: :docs:`pysnmp`

The SNMP engine. It implements SNMPv1, SNMPv2c and SNMPv3 as a manager, as an
agent, as a proxy, and as a notification originator or receiver -- the same
engine in every role, configured differently.

What is inside it, roughly in the order a message passes through:

- **Transport dispatcher.** UDP over IPv4 and IPv6, on asyncio.
- **Message processing.** One module per SNMP version, following
  :rfc:`3412`'s split between message processing and security.
- **Security models.** Community-based for v1 and v2c; USM for v3, with
  authentication (MD5, SHA-1, SHA-2) and privacy (DES, 3DES, AES) as
  pluggable protocols.
- **Access control.** VACM, :rfc:`3415`, which is what makes an agent's view
  of its own MIB configurable rather than all-or-nothing.
- **SMI layer.** MIB modules loaded and instantiated, with the managed-object
  machinery an agent implements its instrumentation against.
- **High-level API.** ``pysnmp.hlapi.asyncio``: one call per SNMP operation,
  which is what most programs need.

Reach past the high-level API when you are building something that is not a
single request -- a command responder, a proxy between SNMP versions, a
notification receiver that has to survive its own authorization failures.

pysmi
-----

:Repository: :repo:`pysmi`
:PyPI: `pysnmp-pysmi <https://pypi.org/project/pysnmp-pysmi/>`_
:Documentation: :docs:`pysmi`

The MIB compiler. It parses ASN.1 MIB sources -- SMIv1, SMIv2 and the de-facto
dialects that vendors ship -- and writes them out as pysnmp modules or as JSON.

It ships the ``mibdump`` and ``mibcopy`` command-line tools, and it can pull
sources from a directory, a ZIP archive, or over HTTP, which is how the
:doc:`MIB archive <mibs>` gets used.

You need pysmi when you have a vendor MIB and want to refer to its objects by
name. You do not need it to run pysnmp: the standard modules an engine
resolves at start-up are compiled already and shipped inside pysnmp, so pysmi
is an optional extra (``pip install 'pysnmplib[compile]'``) rather than a
dependency.

pyasn1
------

:Repository: :repo:`pyasn1`
:PyPI: `pysnmp-pyasn1 <https://pypi.org/project/pysnmp-pyasn1/>`_
:Documentation: :docs:`pyasn1`

ASN.1 types and codecs: X.208 types, and BER, CER and DER encoders and
decoders that can work over a stream rather than a complete buffer.

It is maintained here because SNMP depends on it, but it is not SNMP-specific
and never was -- LDAP, X.509, Kerberos and a long tail of other protocols are
ASN.1 too, and this is a general implementation of the standard.

mibs
----

:Repository: :repo:`mibs`
:Served at: ``https://pysnmp.github.io/mibs/asn1/<MODULE>``

The MIB archive. Not a package -- a website. See :doc:`mibs`.

How they are maintained
-----------------------

The three libraries share a toolchain deliberately, so that a change in one is
a change you already know how to make in the others:

- `uv <https://docs.astral.sh/uv/>`_ with a committed lockfile;
  ``uv sync --locked`` reproduces exactly what CI runs.
- `ruff <https://docs.astral.sh/ruff/>`_ for lint and formatting, against a
  shared rule set, with mypy on top.
- `Conventional Commits <https://www.conventionalcommits.org/>`_, checked on
  every pull request, because semantic-release computes the version number and
  the release notes from the commit history.
- ``main`` carries the released line, ``next`` is where work integrates. A
  release candidate is cut from ``next``, a general release from ``main``, and
  no push releases anything on its own.

Full detail is in
`CONTRIBUTING.md <https://github.com/pysnmp/.github/blob/main/CONTRIBUTING.md>`_,
which applies to every repository in the organization.
