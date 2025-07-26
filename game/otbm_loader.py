import os
import gc
import io
import xml.dom.minidom
import importlib.util

_GENERATOR_PATH = os.path.join(
    os.path.dirname(__file__), "..", "extra", "tools", "generator.py"
)
_spec = importlib.util.spec_from_file_location("generator", _GENERATOR_PATH)
_generator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_generator)
Map = _generator.Map
Item = _generator.Item
Spawn = _generator.Spawn

SECTOR_SIZE = (32, 32)

# global reader instance used while parsing
otbm = None

class Reader:
    """Utility to read little endian values from bytes."""

    __slots__ = ('pos', 'data')

    def __init__(self, data):
        if isinstance(data, str):
            data = data.encode('latin-1')
        self.pos = 0
        self.data = data

    def byte(self):
        self.pos += 1
        val = self.data[self.pos - 1]
        if isinstance(val, int):
            return chr(val)
        return val

    def uint8(self):
        self.pos += 1
        val = self.data[self.pos - 1]
        return val if isinstance(val, int) else ord(val)

    def peekUint8(self):
        try:
            val = self.data[self.pos]
            return val if isinstance(val, int) else ord(val)
        except IndexError:
            return None

    def uint16(self):
        self.pos += 2
        return int.from_bytes(self.data[self.pos-2:self.pos], 'little')

    def uint32(self):
        self.pos += 4
        return int.from_bytes(self.data[self.pos-4:self.pos], 'little')

    def string(self):
        length = self.uint16()
        self.pos += length
        return self.data[self.pos - length:self.pos].decode('latin-1')

    def getData(self):
        return self.data[self.pos:]

LEVEL = 1

dummyItems = {}

def genItem(itemid):
    if itemid not in dummyItems:
        dummyItems[itemid] = Item(itemid)
    return dummyItems[itemid]

class Node:
    __slots__ = ('data', 'nodes', 'begin', 'size', 'index')

    def __init__(self, begin, size=None):
        self.data = b''
        self.nodes = []
        self.begin = begin
        self.size = size
        self.index = 0

    def parse(self):
        global LEVEL, otbm
        otbm.pos = self.begin
        byte = otbm.byte()
        nextEscaped = False
        data = ''
        while otbm.pos < (self.begin + self.size):
            if byte == '\xFE' and not nextEscaped:
                block_size = self.sizer()
                self.handleBlock(otbm.pos, block_size)
                otbm.pos += block_size
            elif byte == '\xFF' and not nextEscaped:
                LEVEL -= 1
                break
            elif byte == '\xFD' and not nextEscaped:
                nextEscaped = True
            else:
                nextEscaped = False
                data += byte
            byte = otbm.byte()
        self.data = Reader(data)

    def sizer(self):
        global otbm
        oldPos = otbm.pos
        sub = 1
        byte = otbm.uint8()
        nextEscaped = False
        while byte is not None:
            if byte == 0xFE and not nextEscaped:
                sub += 1
            elif byte == 0xFF and not nextEscaped:
                sub -= 1
                if sub == 0:
                    break
            elif byte == 0xFD and not nextEscaped:
                nextEscaped = True
            else:
                nextEscaped = False
            byte = otbm.uint8()
        size = otbm.pos - oldPos
        otbm.pos = oldPos
        return size

    def handleBlock(self, begin, size):
        global LEVEL
        LEVEL += 1
        node = Node(begin, size)
        self.nodes.append(node)
        return node

    def next(self):
        if self.index < len(self.nodes):
            node = self.nodes[self.index]
            self.index += 1
            node.parse()
            return node
        return None

def _parse_spawns(m, at, spawns_path):
    dom = xml.dom.minidom.parse(spawns_path)
    for xSpawn in dom.getElementsByTagName('spawn'):
        baseX = int(xSpawn.getAttribute('centerx'))
        baseY = int(xSpawn.getAttribute('centery'))
        baseZ = int(xSpawn.getAttribute('centerz'))
        radius = int(xSpawn.getAttribute('radius'))
        sector_data = {}
        for elem in xSpawn.getElementsByTagName('monster'):
            x = int(elem.getAttribute('x'))
            y = int(elem.getAttribute('y'))
            z = int(elem.getAttribute('z'))
            if z != baseZ:
                continue
            name = ' '.join(
                s[0].upper() + s[1:] for s in elem.getAttribute('name').split(' ')
            ).replace(' Of ', ' of ')
            sector = (int((baseX + x) / 32), int((baseY + y) / 32))
            sector_data.setdefault(sector, []).append(
                (
                    'monster',
                    name,
                    x,
                    y,
                    z,
                    int(elem.getAttribute('spawntime') or 0),
                )
            )
        for elem in xSpawn.getElementsByTagName('npc'):
            x = int(elem.getAttribute('x'))
            y = int(elem.getAttribute('y'))
            z = int(elem.getAttribute('z'))
            if z != baseZ:
                continue
            name = ' '.join(
                s[0].upper() + s[1:] for s in elem.getAttribute('name').split(' ')
            ).replace(' Of ', ' of ')
            sector = (int((baseX + x) / 32), int((baseY + y) / 32))
            sector_data.setdefault(sector, []).append(
                (
                    'npc',
                    name,
                    x,
                    y,
                    z,
                    int(elem.getAttribute('spawntime') or 0),
                )
            )
        for sector, entries in sector_data.items():
            sx = sector[0] * 32 + 16
            sy = sector[1] * 32 + 16
            s = Spawn(radius, (baseX, baseY))
            for info in entries:
                if info[0] == 'monster':
                    s.monster(info[1], info[2], info[3], info[4], info[5])
                else:
                    s.npc(info[1], info[2], info[3], info[4], info[5])
            at(sx, sy, s, baseZ)

def convert_otbm_to_sec(otbm_path, output_dir):
    """Convert an OTBM file to `.sec` map sectors under ``output_dir``."""

    global otbm
    with io.open(otbm_path, 'rb') as f:
        data = f.read()
    otbm = Reader(data)
    root = Node(5, len(data))
    root.parse()
    root.data.pos += 1

    version = root.data.uint32()
    width = root.data.uint16()
    height = root.data.uint16()
    root.data.uint32()  # majorVersionItems
    root.data.uint32()  # minorVersionItems

    m = Map(width, height, None, 15)
    at = m.addTo
    nodes = root.next()
    nodes.data.pos += 1
    description = ''
    spawns_file = ''
    while nodes.data.peekUint8():
        attr = nodes.data.uint8()
        if attr == 1:
            description += nodes.data.string() + '\n'
        elif attr == 11:
            spawns_file = nodes.data.string()
        elif attr == 13:
            nodes.data.string()  # houses path, ignored
        else:
            nodes.data.getData()
    m.description(description)
    m.author('otbm_loader')
    node = nodes.next()
    while node:
        t = node.data.uint8()
        if t == 4:
            baseX = node.data.uint16()
            baseY = node.data.uint16()
            baseZ = node.data.uint8()
            tile = node.next()
            while tile:
                tileType = tile.data.uint8()
                if tileType in (5, 14):
                    tileX = tile.data.uint8() + baseX
                    tileY = tile.data.uint8() + baseY
                    houseId = 0
                    if tileType == 14:
                        houseId = tile.data.uint32()
                    render = False
                    ground = None
                    flags = 0
                    while tile.data.peekUint8() is not None:
                        attr = tile.data.uint8()
                        if attr == 3:
                            flags = tile.data.uint32()
                        elif attr == 9:
                            ground = genItem(tile.data.uint16())
                            render = True
                        else:
                            break
                    tile_items = []
                    if ground:
                        tile_items.append(ground)
                    item = tile.next()
                    while item:
                        if item.data.uint8() == 6:
                            itemId = item.data.uint16()
                            if not item.data.peekUint8():
                                curr = genItem(itemId)
                            else:
                                curr = Item(itemId)
                            while item.data.peekUint8():
                                attr = item.data.uint8()
                                if attr == 10:
                                    curr.attribute('depotId', item.data.uint16())
                                elif attr == 14:
                                    curr.attribute('doorId', item.data.uint8())
                                    curr.action('houseDoor')
                                elif attr == 20:
                                    item.data.uint32()
                                elif attr == 21:
                                    item.data.uint32()
                                elif attr == 8:
                                    curr.attribute(
                                        'teledest',
                                        [
                                            item.data.uint16(),
                                            item.data.uint16(),
                                            item.data.uint8(),
                                        ],
                                    )
                                elif attr in (15, 22):
                                    curr.attribute('count', item.data.uint8())
                                elif attr == 4:
                                    curr.action(str(item.data.uint16()))
                                elif attr == 5:
                                    curr.action(str(item.data.uint16() + 0xFFFF))
                                elif attr == 6:
                                    curr.attribute('text', item.data.string())
                                elif attr == 18:
                                    curr.attribute('written', item.data.uint32())
                                elif attr == 19:
                                    curr.attribute('writtenBy', item.data.string())
                                elif attr == 7:
                                    curr.attribute('description', item.data.string())
                                elif attr == 12:
                                    item.data.uint8()
                                elif attr == 16:
                                    item.data.uint32()
                                elif attr == 17:
                                    item.data.uint8()
                                elif attr == 23:
                                    item.data.uint32()
                                    break
                                else:
                                    pass
                            render = True
                            tile_items.append(curr)
                        item = tile.next()
                    if render:
                        at(tileX, tileY, tile_items, baseZ)
                        if houseId:
                            m.houses[(tileX, tileY, baseZ)] = houseId
                        if flags:
                            m.flags[(tileX, tileY, baseZ)] = flags
                tile = node.next()
        elif t == 12:
            town = node.next()
            while town:
                if town.data.uint8() == 13:
                    tid = town.data.uint32()
                    name = town.data.string()
                    temple = [town.data.uint16(), town.data.uint16(), town.data.uint8()]
                    m.town(tid, name, temple)
                town = node.next()
        elif t == 15 and version >= 2:
            waypoint = node.next()
            while waypoint:
                if waypoint.data.uint8() == 16:
                    name = waypoint.data.string()
                    cords = [
                        waypoint.data.uint16(),
                        waypoint.data.uint16(),
                        waypoint.data.uint8(),
                    ]
                    m.waypoint(name, cords)
                waypoint = node.next()
        node = nodes.next()

    if spawns_file:
        spawns_path = os.path.join(os.path.dirname(otbm_path), spawns_file)
        _parse_spawns(m, at, spawns_path)

    os.makedirs(output_dir, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(output_dir)
    try:
        gc.collect()
        m.compile(SECTOR_SIZE)
    finally:
        os.chdir(cwd)
    return m
