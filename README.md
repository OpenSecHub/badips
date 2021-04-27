# badips

bad IPs collector, write to redis

## Config

config file is `src/conf/config.yml`

```yaml
# where to store the cralwer data
database:
  type: redis
  host: 10.130.12.66
  port: 6379
  db: 0
  table: 0
  passwd: red@6379
  ssl: no

# proxy to access the http url
proxy:
  # NO : do not use proxy
  # ALL: access all urls via proxy
  # TRY: if access fail, use proxy
  policy: TRY
  url: "http://192.168.254.1:1080"

sources:

  - source:
      name: alienvault.com
      status: ENABLE
      url: https://reputation.alienvault.com/reputation.generic
      # the source release date, get from HTTP reponse header or HTTP reponse body
      date:
        location: HEADER
        field: Last-Modified
      comment:
        pattern_str: "(\\s*)#.*$"
      data:
        # remove comments, this is a regular expression pattern, will replace with empty
        pattern_str: "^.+$"
        pattern_index: 0

  - source:
      name: feodotracker.abuse.ch
      status: ENABLE
      url: https://feodotracker.abuse.ch/downloads/ipblocklist.csv
      date:
        location: BODY
        pattern_str: "Last updated:\\s*(.+?)\\s*#"
        pattern_index: 1
      comment:
        pattern_str: "(\\s*)#.*$"
      data:
        pattern_str: ",\"([\\d\\.]+?)\","
        pattern_index: 1

```

## Run
```
cd src
python3 main.py
```

## Result

```bash
+-----+-------------------------------+---------+--------+-------------------------------+-------+
| No. | Name                          | Enable  | Status | Last Update                   | Count |
+-----+-------------------------------+---------+--------+-------------------------------+-------+
| 1   | alienvault.com                | True    | OK     | Tue, 23 Mar 2021 14:12:22 GMT | 1595  |
| 2   | feodotracker.abuse.ch         | True    | OK     | 2021-04-26 14:52:10 UTC       | 171   |
| 3   | danger.rulez.sk               | True    | OK     | Tue, 27 Apr 2021 05:40:22 GMT | 3398  |
| 4   | cinsscore.com                 | True    | OK     | Tue, 27 Apr 2021 05:04:01 GMT | 15000 |
| 5   | feeds.dshield.org             | True    | OK     | Tue, 27 Apr 2021 05:16:46 GMT | 36    |
| 6   | rules.emergingthreats.net     | True    | OK     | Mon, 26 Apr 2021 21:57:58 GMT | 3404  |
| 7   | blocklist.greensnow.co        | True    | OK     | Tue, 27 Apr 2021 05:41:44 GMT | 7388  |
| 8   | report.cs.rutgers.edu         | True    | OK     | Tue, 27 Apr 2021 05:37:32 GMT | 3413  |
| 9   | danger.rulez.sk               | True    | OK     | Tue, 27 Apr 2021 05:40:22 GMT | 3398  |
| 10  | dataplane.org:dnsrd           | True    | OK     | Tue, 27 Apr 2021 05:00:37 GMT | 1299  |
| 11  | dataplane.org:dnsrdany        | True    | OK     | Tue, 27 Apr 2021 05:00:39 GMT | 862   |
| 12  | dataplane.org:dnsversion      | True    | OK     | Tue, 27 Apr 2021 05:00:30 GMT | 289   |
| 13  | dataplane.org:sipinvitation   | True    | OK     | Tue, 27 Apr 2021 05:00:37 GMT | 68    |
| 14  | dataplane.org:sipquery        | True    | OK     | Tue, 27 Apr 2021 05:00:33 GMT | 1216  |
| 15  | dataplane.org:sipregistration | True    | OK     | Tue, 27 Apr 2021 05:00:37 GMT | 44    |
| 16  | dataplane.org:sshclient       | True    | OK     | Tue, 27 Apr 2021 05:01:25 GMT | 28321 |
| 17  | dataplane.org:sshpwauth       | True    | OK     | Tue, 27 Apr 2021 05:01:39 GMT | 23920 |
| 18  | dataplane.org:vncrfb          | True    | OK     | Tue, 27 Apr 2021 05:03:58 GMT | 1285  |
+-----+-------------------------------+---------+--------+-------------------------------+-------+
```
