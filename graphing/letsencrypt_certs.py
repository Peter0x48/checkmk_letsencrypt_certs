#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.graphing.v1 import (
    metrics as m,
)

metric_letsencrypt_certs_days_left = m.Metric(
    name='letsencrypt_certs_days_left',
    title=m.Title('Days left'),
    unit=m.Unit(m.TimeNotation()),
    color=m.Color.GREEN,
)
