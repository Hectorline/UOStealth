""" This small script will calculate the summ of the suite your char is currentrly wearing.
	This will only run in Python 3.x"""

import stealth
import re

uo_layers = (
ArmsLayer(), BeardLayer(), BraceLayer(), CloakLayer(), EarLayer(), EggsLayer(), GlovesLayer(), HairLayer(), HatLayer(),
LegsLayer(),
LhandLayer(), NeckLayer(), PantsLayer(), RhandLayer(), RingLayer(), RobeLayer(), ShirtLayer(), ShoesLayer(),
TalismanLayer(), TorsoHLayer(),
TorsoLayer(), WaistLayer())

properties = {}


def to_sum_up(prop: 'string') -> 'Boolean':
    """ This sub will be used to get rid of unwanted properties like 'Insured' or such.
    As argument it is expecting a string and it will retur either True (if the property should not be ignored) or False"""

    # strigs to be ignored in tooltip. Add new if missing
    ignores = ['Insured', 'durability', 'Weight', 'artifact rarity', 'strength requirement', 'two-handed weapon',
           'skill required']

    for ignore in ignores:
        if prop.find(ignore) != -1 or prop == '':
            break
        else:
        return True

    return False


def sum_props(dressed_layers: 'dict') -> 'dict':
""" This sub will sum all the properties together.
As argument it is expeting a dictionary in this format {layer:[raw properties,]}
It is returning another dictionary with this format {prop name : total value}"""

totals = {}

# Property regex
reProps = re.compile(r"([a-zA-Z ].+?)[+]{0,}([\d]{1,})(%{0,1})")
for layer in dressed_layers:
    if dressed_layers[layer]:
        item = dressed_layers[layer][0]
        props = dressed_layers[layer][1:]
        for prop in props:
            match = reProps.search(prop)
            if match:
                prop_name = match.group(1).strip()
                prop_value = match.group(2)
                totals[prop_name] = totals.get(prop_name, 0) + int(prop_value)

return totals

for uo_layer in uo_layers:
    weared = ObjAtLayer(uo_layer)
    if weared > 0:
        properties[hex(uo_layer)] = [] + [x.strip() for x in GetTooltip(weared).split(' | ') if to_sum_up(x)]

totals = sum_props(properties)

for prop in sorted(totals.keys(), key=str.lower):
    print(prop + ' --> ' + str(totals[prop]))