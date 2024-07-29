#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.agent_based.v2 import (
    Service,
    CheckPlugin,
    StringTable,
    AgentSection,
    check_levels,
    render,
)


def parse_letsencrypt_certs(string_table: StringTable):
    parsed = {}
    for item in string_table:
        if len(item) != 2:
            continue
        parsed[item[0]] = item[1]

    return parsed


agent_section_letsencrypt_certs = AgentSection(
    name='letsencrypt_certs',
    parse_function=parse_letsencrypt_certs
)


def discovery_letsencrypt_certs(section):
    for name, expiry in section.items():
        yield Service(item=name)


def check_letsencrypt_certs(item, params, section):
    expiry = int(section[item]) * 24 * 60 * 60

    yield from check_levels(
        int(expiry),
        levels_lower=params.get('validity'),
        label='Validity left',
        render_func=lambda f: render.timespan(f if f > 0 else -f),
        metric_name='letsencrypt_certs_days_left'
    )


check_plugin_letsencrypt_certs = CheckPlugin(
    name='letsencrypt_certs',
    service_name='Lets Encrypt Certificate %s',
    discovery_function=discovery_letsencrypt_certs,
    check_function=check_letsencrypt_certs,
    check_ruleset_name='letsencrypt_certs',
    check_default_parameters={
        'validity': ('fixed', (20 * 24 * 60 * 60, 10 * 24 * 60 * 60))
    }
)
