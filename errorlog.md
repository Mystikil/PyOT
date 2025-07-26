2025-07-25 22:12:28,461 [ERROR] Uncaught exception
Traceback (most recent call last):
  File "C:\Users\J\Desktop\Devnexus-v2\v2\gameserver.py", line 62, in <module>
    import game.loading
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\loading.py", line 26, in <module>
    import game.otbm_loader
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\otbm_loader.py", line 12, in <module>
    _spec.loader.exec_module(_generator)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\..\extra\tools\generator.py", line 12, in <module>
    parse = json.load(io.open("../../data/items.json", 'r'))
                      ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '../../data/items.json'
2025-07-25 22:28:42,447 [ERROR] Exception in callback functools.partial(<function wrap.<locals>.null_wrapper at 0x00000232F6DE8540>, <game.hack_concurrent.Future object at 0x00000232F6C01E20>)
Traceback (most recent call last):
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\service\gameserver.py", line 250, in onFirstPacket
    tile.placeCreature(self.player)
    ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'placeCreature'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\ioloop.py", line 605, in _run_callback
    ret = callback()
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1152, in inner
    self.run()
    ~~~~~~~~^^
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1094, in run
    self.result_future.set_exc_info(sys.exc_info())
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 282, in set_exc_info
    self.set_exception(exc_info[1])
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 265, in set_exception
    self._set_done()
    ~~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 292, in _set_done
    cb(self)
    ~~^^^^^^
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 200, in final_callback
    if future.result() is not None:
       ~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 204, in result
    raise_exc_info(self._exc_info)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "<string>", line 4, in raise_exc_info
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1069, in run
    yielded = self.gen.send(value)
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\service\gameserver.py", line 257, in onFirstPacket
    tile.placeCreature(self.player)
    ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'placeCreature'
2025-07-25 22:40:06,559 [ERROR] Exception in callback functools.partial(<function wrap.<locals>.null_wrapper at 0x00000232F6DE9E40>, <game.hack_concurrent.Future object at 0x00000232F61C7AD0>)
Traceback (most recent call last):
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\service\gameserver.py", line 250, in onFirstPacket
    tile.placeCreature(self.player)
    ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'placeCreature'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\ioloop.py", line 605, in _run_callback
    ret = callback()
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1152, in inner
    self.run()
    ~~~~~~~~^^
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1094, in run
    self.result_future.set_exc_info(sys.exc_info())
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 282, in set_exc_info
    self.set_exception(exc_info[1])
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 265, in set_exception
    self._set_done()
    ~~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 292, in _set_done
    cb(self)
    ~~^^^^^^
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 200, in final_callback
    if future.result() is not None:
       ~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 204, in result
    raise_exc_info(self._exc_info)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "<string>", line 4, in raise_exc_info
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1069, in run
    yielded = self.gen.send(value)
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\service\gameserver.py", line 257, in onFirstPacket
    tile.placeCreature(self.player)
    ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'placeCreature'
2025-07-25 22:59:19,252 [ERROR] Exception in callback functools.partial(<function wrap.<locals>.null_wrapper at 0x00000235B70BA020>, <game.hack_concurrent.Future object at 0x00000235B6A78A50>)
Traceback (most recent call last):
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\ioloop.py", line 605, in _run_callback
    ret = callback()
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\ioloop.py", line 626, in _discard_future_result
    future.result()
    ~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 204, in result
    raise_exc_info(self._exc_info)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "<string>", line 4, in raise_exc_info
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1069, in run
    yielded = self.gen.send(value)
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\loading.py", line 380, in loader
    game.otbm_loader.convert_otbm_to_sec(otbm_path, sec_dir)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\otbm_loader.py", line 345, in convert_otbm_to_sec
    _parse_spawns(m, at, spawns_path)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\otbm_loader.py", line 186, in _parse_spawns
    s.monster(info[1], info[2], info[3], info[4], info[5])
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\..\extra\tools\generator.py", line 631, in monster
    self.cret.append(chr(61) + chr(len(name)) + name + struct.pack("<bbI", x, y, spawntime))
                                                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
struct.error: required argument is not an integer
2025-07-25 23:16:03,499 [ERROR] Exception in callback functools.partial(<function wrap.<locals>.null_wrapper at 0x000001975789E020>, <game.hack_concurrent.Future object at 0x000001975729CA50>)
Traceback (most recent call last):
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\ioloop.py", line 605, in _run_callback
    ret = callback()
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\ioloop.py", line 626, in _discard_future_result
    future.result()
    ~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 204, in result
    raise_exc_info(self._exc_info)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "<string>", line 4, in raise_exc_info
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1069, in run
    yielded = self.gen.send(value)
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\loading.py", line 380, in loader
    game.otbm_loader.convert_otbm_to_sec(otbm_path, sec_dir)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\otbm_loader.py", line 359, in convert_otbm_to_sec
    _parse_spawns(m, at, spawns_path)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\otbm_loader.py", line 200, in _parse_spawns
    s.monster(info[1], info[2], info[3], info[4], info[5])
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\..\extra\tools\generator.py", line 631, in monster
    self.cret.append(chr(61) + chr(len(name)) + name + struct.pack("<bbI", x, y, spawntime))
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TypeError: can only concatenate str (not "bytes") to str
2025-07-25 23:16:08,704 [ERROR] Exception in callback functools.partial(<function wrap.<locals>.null_wrapper at 0x000001980B99EA20>, <game.hack_concurrent.Future object at 0x0000019757B8B2F0>)
Traceback (most recent call last):
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\service\gameserver.py", line 250, in onFirstPacket
    tile.placeCreature(self.player)
    ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'placeCreature'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\ioloop.py", line 605, in _run_callback
    ret = callback()
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1152, in inner
    self.run()
    ~~~~~~~~^^
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1094, in run
    self.result_future.set_exc_info(sys.exc_info())
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 282, in set_exc_info
    self.set_exception(exc_info[1])
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 265, in set_exception
    self._set_done()
    ~~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 292, in _set_done
    cb(self)
    ~~^^^^^^
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\stack_context.py", line 277, in null_wrapper
    return fn(*args, **kwargs)
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 200, in final_callback
    if future.result() is not None:
       ~~~~~~~~~~~~~^^
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\hack_concurrent.py", line 204, in result
    raise_exc_info(self._exc_info)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "<string>", line 4, in raise_exc_info
  File "C:\Users\J\AppData\Roaming\Python\Python313\site-packages\tornado\gen.py", line 1069, in run
    yielded = self.gen.send(value)
  File "C:\Users\J\Desktop\Devnexus-v2\v2\game\service\gameserver.py", line 257, in onFirstPacket
    tile.placeCreature(self.player)
    ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'placeCreature'
