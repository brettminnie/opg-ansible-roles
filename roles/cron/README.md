#Cron 

Role for managing cronjobs

```
cronjobs:
  jobs:
    - name: btrfsbalance
      enabled: True
      user: root
      hour: '4'
      minute: random
      daymonth: "'*'"
      month: "'*'"
      dayweek: "'*'"
      command: /sbin/btrfs fi balance start -dusage=10 /srv
    - name: test
      enabled: False
      user: root
      hour: 2
      command: echo "this is a test job"
```

The `enabled` key can be set to `False` to remove jobs previously added when it was set to `True`.

Default values for the following are used when not supplied via pillar:

* Hour      (Random)
* Minute    (Random)
* Daymonth  (Every day of the month)
* Month     (Every month of the year)
* Dayweek   (Every day of the week)

Where data exists, the following values MUST be specified as default values cannot be derived:

* User
* Command
