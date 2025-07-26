In order to run PyOT you need:
================================

* Python 3.4+ or (pypy currently NOT supported until they get python 3.4 support ATM on 3.2)

* Tornado 4+

* pymysql

* Optional: pywin32 may give a better eventloop on windows

* Optional: cffi enable some C extension for better performance.

Links for Windows:
------------------

https://www.python.org/ftp/python/3.4.1/python-3.4.1.amd64.msi

http://www.lfd.uci.edu/~gohlke/pythonlibs/#tornado (tornado-4.0.2-win-amd64-py3.4.exe)

=======

Open cmd and run:
c:\Python34\Scripts\easy_install.exe pymysql

Optional:
http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download



Installation
============

Copy "config.py.dist" to "config.py" and edit it to match your database settings.
The default configuration is also used when running the automated tests,
so ensure `config.py` exists before executing them.
The new `pingInterval` option controls how often the server sends a keepalive
packet to connected clients. Lower it if players randomly disconnect.
Enabling `pingIncludeTimestamp` in the config will append a millisecond
timestamp to these keepalive packets, helping clients keep their clocks in sync.

Run gameserver.py, it will automatically set up your database :)

Linux (any distro)
---------------------------------------------

Install python3.3+ from package management. You may loop for tornado4 and pymysql there as well.
Otherwise:

pip install tornado
pip install pymysql

or

pip3 install tornado
pip3 install pymysql 


Documentation
=============

You can find additional documentation of PyOT here: http://vapus.net/pyot_doc/index.html

Useful scripting guide here: http://vapus.net/pyot_doc/scriptevents.html

Testing
-------
The automated tests expect the default configuration to be available as
`config.py`. Copy `config.py.dist` to `config.py` before running
``python -m unittest``.

Modular Combat System
---------------------
A new combat engine lives in ``game/combat``. It is composed of small
components which operate on a :class:`CombatContext` instance. Components can be
combined in a :class:`CombatResolver` to implement various attack behaviors.

Example::

    from game.combat import (CombatContext, CombatResolver,
                             BaseDamageComponent, CriticalHitComponent,
                             ResistanceComponent, HitChanceComponent)

    context = CombatContext(attacker, target, spell=my_fireball)
    resolver = CombatResolver([
        BaseDamageComponent(50, 100),
        CriticalHitComponent(0.2, 1.5),
        ResistanceComponent('fire'),
        HitChanceComponent(0.85),
    ])
    result = resolver.resolve(context)
    if result.hit:
        target.apply_damage(result.damage)

Permissions
===========

Access levels are defined in the `groups` table. Each entry contains a
JSON encoded list of `group_flags` which represent the actions allowed for
that group. During startup these flags are loaded into
``game.functions.groups`` and checked whenever a player performs an action.

A character's permissions are determined by both its own ``group_id`` and
the ``group_id`` on its account. The flags from both groups are combined,
so raising either value grants the associated rights to the player.

Example setups
--------------

- **Admin** – account and player ``group_id`` set to ``6``. Grants every
  flag from the Admin entry, including script reloads and banning.
- **Player** – both IDs set to ``1``. Only basic flags like ``SPEAK`` and
  ``ATTACK`` are available.

Website Configuration
---------------------
The bundled character manager uses the account's ``group_id`` to decide
whether a user can access the admin panel. The threshold is configured in
``website/config.php`` via the ``$ADMIN_GROUP_ID`` setting (default ``6``).
Update this value to match your desired admin group and all admin checks will
use it automatically.

Map Formats
-----------
PyOT can load both compiled sector files (`.sec`) and the traditional
`map.otbm` format. Both the sectors and optional ``map.otbm`` reside in
``data/<config.mapDirectory>/``.

At startup the loader checks for ``map.otbm``. If it exists and
``config.preferSecFormat`` is **False**, the server converts it into ``.sec``
files (when none already exist) and loads the OTBM data. When
``preferSecFormat`` is **True``—the default—the ``.sec`` sectors are used
directly for faster loading. A message like ``Map format loaded: sec`` or
``Map format loaded: otbm`` appears during startup to indicate the choice.

Recommended workflow:

1. Place your OTBM file as ``data/<config.mapDirectory>/map.otbm``.
2. Temporarily set ``preferSecFormat = False`` and start the server once.
   This converts the map into ``.sec`` files inside ``data/<config.mapDirectory>/``.
3. Re-enable ``preferSecFormat`` so subsequent runs load the compiled sectors.
4. ``data/<config.mapDirectory>/`` should now contain your world data.
   You can keep ``map.otbm`` as a backup or delete it once sectors are generated.
