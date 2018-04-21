# Personal Notes on Python

## Threading and Multiprocessing Modules

The threading module uses threads which operate in the same memory space. The multiprocessing module uses processes which have separate memory.

### Threads and Threading

A thread is an entity within a process that can be scheduled for execution. All threads of a process share the process's system resources. 

- shares the same memory (low memory footprint)
- subject to Global Interpreter Lock (for cPython, see below)
- can run concurrently by context switching (useful for IO-bound operations)
- CPython C extension modules that properly release the Global Interpreter Lock can execute in parallel 

### Processes and Multiprocessing

A process is an entity that provides resources for program execution. Each process is started with a primary thread and can create additional threads. 

- has separate memory
- can sidestep the Global Interpreter Lock with subprocesses
- can utilize multiple cores (useful for CPU-bound processing)
- interprocess communication (IPC) is more complicated and has communication overheads

### Global Interpreter Lock (GIL)

Mechanism used to synchronize thread execution so that only one thread can execute at a time (GIL is a mutex). GIL limits parallelism by preventing threads from running in parallel (although threads can run concurrently/context switch during IO-bound operations).

### CPython

CPython is the original Python implementation. It compiles Python code into bytecode and interprets that bytecode in an evaluation loop. It implements the GIL.


### References
- [Process vs. Thread](https://stackoverflow.com/questions/200469/what-is-the-difference-between-a-process-and-a-thread)
- [Multiprocessing vs. Threading](https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python)
- [Python GIL](https://cs.nyu.edu/~lerner/spring10/projects/Python_GIL.pdf)
- [Python vs. CPython](https://stackoverflow.com/questions/17130975/python-vs-cpython)