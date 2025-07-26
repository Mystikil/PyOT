import os
import xml.etree.ElementTree as ET
import config

SKILL_NAMES = {}
SKILL_COLORS = {}

path = os.path.join(config.dataDirectory, 'skillinfo.xml')
if os.path.exists(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for skill in root.findall('skill'):
        sid = int(skill.get('id'))
        SKILL_NAMES[sid] = skill.get('name')
        SKILL_COLORS[sid] = skill.get('color')

