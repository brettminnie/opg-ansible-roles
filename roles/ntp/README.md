###ntp
===
install ntp package and ensure it's running


####example
-------
meta-data:
```yaml
    ntp:
      servers:
        - 0.pool.ntp.org
        - 1.pool.ntp.org
        - 2.pool.ntp.org
        - 3.pool.ntp.org
```