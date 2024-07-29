#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    InputHint,
    LevelDirection,
    migrate_to_integer_simple_levels,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostAndItemCondition


def _parameter_form_letsencrypt_certs():
    return Dictionary(
        elements={
            'validity': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Lets Encrypt Certificate Expiry'),
                    help_text=Help('Days until expiry of the certificate'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY]
                    ),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_fixed_levels=InputHint(value=(20, 10)),
                ),
                required=False,
            ),
        },
    )


rule_spec_letsencrypt_certs = CheckParameters(
    name='letsencrypt_certs',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_letsencrypt_certs,
    title=Title('Lets Encrypt Certificates'),
    help_text=Help('This rule configures thresholds for Lets Encrypt Certificates'),
    condition=HostAndItemCondition(item_title=Title('Lets Encrypt Certificates')),
)
