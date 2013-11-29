opsview-downtime
================

This tool allow you to quickly and conveniently schedule downtime
for Opsview hosts from your favourite terminal.

<pre>
usage: opsview-downtime.py [-h] [-u OpsviewUser] [-p OpsviewPassword]
                           [-s OpsviewServer] [-m DowntimeComment]
                           [-t DowntimeStartTime] [-T DowntimeEndTime] [-v]
                           (-o Host | -f InputFile)

Opsview Downtime Tool

optional arguments:
  -h, --help            show this help message and exit
  -u OpsviewUser, --user OpsviewUser
                        Opsview username. Will prompt if not provided.
  -p OpsviewPassword, --password OpsviewPassword
                        Opsview password. Will prompt if not provided.
  -s OpsviewServer, --server OpsviewServer
                        Opsview server
  -m DowntimeComment, --comment DowntimeComment
                        Downtime comment
  -t DowntimeStartTime, --starttime DowntimeStartTime
                        When to start the downtime. Default: now
  -T DowntimeEndTime, --endtime DowntimeEndTime
                        How much downtime (eg. +30m, +1h). Default: +2h
  -v, --verbose         Print more messages
  -o Host, --opsviewhost Host
                        Host to schedule downtime for (the name of the host in
                        Opsview)
  -f InputFile, --file InputFile
                        File to read hosts from (one host per line)


Example usage:
python opsview-downtime.py -o myhost.example.com -T +1h -c SimpleComment

Example usage:
python opsview-downtime.py -f InputHosts.txt -t +30m -T +2h -c ChangeNumber001

Example InputFile:
host1.example.com
host2.example.com
host3.example.com
</pre>
