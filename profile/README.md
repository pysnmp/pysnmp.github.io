## SNMP for Python

Four projects, one stack. An SNMP engine, the MIB compiler it resolves modules
with, the ASN.1 codec underneath both, and the MIB corpus they read — all pure
Python, BSD licensed, and maintained together.

**[pysnmp.github.io/.github](https://pysnmp.github.io/.github/)**

| | | |
|---|---|---|
| **[pysnmp](https://github.com/pysnmp/pysnmp)** | the engine | SNMPv1, v2c and v3: command generator and responder, notifications, USM, VACM, asyncio |
| **[pysmi](https://github.com/pysnmp/pysmi)** | the compiler | ASN.1 MIBs into pysnmp modules, JSON or a corpus database; `mibdump`, `mibcopy`, `mibcorpus` |
| **[pyasn1](https://github.com/pysnmp/pyasn1)** | the codec | ASN.1 types to X.208 with BER, CER and DER codecs |
| **[mibs](https://github.com/pysnmp/mibs)** | the corpus | 5,510 modules as ASN.1, JSON, an OID index and SQLite — served over HTTP, shipped as images and a Helm chart |

```bash
uv add pysnmplib
```

Resolve MIBs against the corpus without installing it:

```
https://pysnmp.github.io/mibs/asn1/@mib@
```

These are maintained forks of Ilya Etingof's original work. Ilya passed away on
10 August 2022; his work remains of great use to the Python community.
