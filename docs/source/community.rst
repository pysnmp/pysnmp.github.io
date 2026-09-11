Community
=========

The organization's community files live in :repo:`.github` and apply to every
repository here. A repository that ships its own copy of one of them overrides
it, so check the repository you are working in first.

Reporting a bug
---------------

Open an issue on the repository the bug is in, using the **Bug report** form.
The form asks for the things that decide whether a report can be acted on: the
smallest script that reproduces it, the full traceback rather than the last
line, and the versions you are running.

For anything involving a real device, say which device. "A Cisco switch" and
"net-snmp 5.9 with this ``snmpd.conf``" lead to different first questions, and
a packet capture settles most of them faster than either.

Asking a question
-----------------

Use the **Question** form on the repository, after the
:docs:`documentation <pysnmp>` and the repository's ``examples/`` directory --
most usage questions are answered by a script already in the tree.
`SUPPORT.md <https://github.com/pysnmp/.github/blob/main/SUPPORT.md>`_ says
what is in scope and what is not.

Contributing
------------

`CONTRIBUTING.md <https://github.com/pysnmp/.github/blob/main/CONTRIBUTING.md>`_
is the full version. In brief:

.. code-block:: console

   $ git clone https://github.com/pysnmp/<repository>.git
   $ cd <repository>
   $ uv sync --locked
   $ uv run --locked --group dev pytest
   $ pre-commit install

Then: open the pull request against ``next``, write the title as a
`conventional commit <https://www.conventionalcommits.org/>`_ because it
becomes one, and bring a test that fails without your change.

These are protocol libraries, so a test that asserts against encoded bytes or
a decoded structure is worth more than one that asserts against a ``repr``,
and a test that cites the RFC it is checking is still reviewable in five
years.

Reporting a vulnerability
-------------------------

Privately, through GitHub's private vulnerability reporting on the affected
repository -- never as a public issue.
`SECURITY.md <https://github.com/pysnmp/.github/blob/main/SECURITY.md>`_ has
the links and says what to expect.

It also says what is not a vulnerability, which is worth reading before you
write one up. SNMPv1 and SNMPv2c have no security by design; the community
string is a cleartext password and there is no integrity protection. SNMPv3
specifies MD5, SHA-1 and DES, and pysnmp implements them because deployed
equipment speaks them -- it warns at run time where one is configured, and
SHA-2 (:rfc:`7860`) and AES (:rfc:`3826`) are there to be used instead.

Code of conduct
---------------

The `Contributor Covenant 2.1
<https://github.com/pysnmp/.github/blob/main/CODE_OF_CONDUCT.md>`_, across
every repository here: issues, pull requests, discussions, code review and
commit messages.
