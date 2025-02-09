import pnd
import _thread
import time
print(pnd.cfg.tasks.gc_tasks)



## init pundo system
runtime = pnd.rt()
runtime.init(0)

## run backgroundtasks
_thread.start_new_thread(runtime.backgroundTask, ())

## run main Task
runtime.run()
