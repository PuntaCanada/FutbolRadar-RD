# Source audit — 2026-11-26

Observed in [run 45780393923, job 139774151044](https://github.com/PuntaCanada/FutbolRadar-RD/actions/runs/45780393923/job/139774151044), PR head 941d1e017fb67e6b7e4917e2c10c166250c5f411.

| Source | Parsed records | Latest / range |
|---|---:|---|
| Fedofutbol RSS | 10 | first item 2026-11-25 03:55:54 UTC |
| Futbol Total RD RSS | 10 | first item 2026-11-02 13:22:58 UTC |
| international_results CSV | 164 Dominican Republic candidate rows | 1949-05-14 to 2026-11-17 |

The probe checks XML parsing, existence of links and matching CSV team names and dates. It does not establish deduplication, historical completeness, accuracy of scores, classification of every match or publication rights. The RSS dates are the first item in each feed, not independently verified maxima. No records are published; source rights remain pending, API-Football blocked. No sponsorship enabled.
