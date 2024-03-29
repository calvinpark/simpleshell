# Simple Shell

Run a shell command, and receive `stdout`, `stderr`, and `returncode`.  It's dead simple.

```python
$ python3
[...]
>>> from simpleshell import ss
>>> output = ss('head -3 LICEN*')
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>> print(output)
CompletedProcess(
    args='head LICEN*',
    returncode=0,
    stdout=['MIT License', '', 'Permission is hereby granted, free of charge, to any person obtaining a copy'],
    stderr=['']
)
>>>
```
All calls are synchronous, therefore it's not possible to see the output until the command exits. This makes Simple Shell unsuitable for `tail`ing a log.

## Install
`$ python3 -m pip install simpleshell`

## Use
```python
from simpleshell import ss

output = ss('ls -la')  # Prints the result on the screen through stdout

pprint(vars(output))   # Prints the dict below
{'args': 'ls -la',
 'returncode': 0,
 'stderr': [''],
 'stdout': ['total 28',
            'drwxr-xr-x 13 calvin staff  416 Oct 23 00:08 .',
            'drwxr-xr-x  7 calvin staff  224 Oct 22 16:56 ..',
            'drwxr-xr-x 13 calvin staff  416 Oct 22 23:51 .git',
            '-rw-r--r--  1 calvin staff   63 Oct 22 21:28 .gitignore',
            'drwxr-xr-x  9 calvin staff  288 Oct 23 00:08 .idea',
            '-rw-r--r--  1 calvin staff 1036 Oct 22 22:27 LICENSE',
            '-rw-r--r--  1 calvin staff  287 Oct 22 23:24 Makefile',
            '-rw-r--r--  1 calvin staff 4320 Oct 23 00:08 README.md',
            'drwxr-xr-x  4 calvin staff  128 Oct 22 23:51 dist',
            '-rw-r--r--  1 calvin staff  104 Oct 22 21:57 pyproject.toml',
            '-rw-r--r--  1 calvin staff  594 Oct 22 23:50 setup.cfg',
            'drwxr-xr-x  4 calvin staff  128 Oct 22 23:51 src',
            'drwxr-xr-x  2 calvin staff   64 Oct 22 17:03 tests',
            '']}

```

## Return values
### On success
`CompletedProcess` object with member variables `args`, `returncode`, `stdout`, `stderr`.

`stdout` and `stderr` may be a `str` or a `list[str]` based on optional parameter `convert_stdout_stderr_to_list`.
### On error
```python
if optional parameter 'exit_on_error':
    nothing
else:
    subprocess.CalledProcessError exception object
```

## Optional parameters
* ### `print_output_on_success=True`
When `False`, nothing gets printed when the command exits with `0`.
```python
>>> output = ss('head -3 LICEN*', print_output_on_success=False)
>>>
```

* ### `print_output_on_error=True`
When `False`, nothing gets printed when the command exists with a non-`0`.  
In the below example, the command exited with return code `127` and caused the `python3` process to exit.
```python
>>> output = ss('invalid command', print_output_on_error=False)
$ echo $?
127
$
```

* ### `convert_stdout_stderr_to_list=True`
When `False`, `output.stdout` and `output.stderr` are strings with `\n` embedded in them.
```python
>>> output = ss('head -3 LICEN*', convert_stdout_stderr_to_list=False)
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>> print(output)
CompletedProcess(
    args='head LICEN*',
    returncode=0,
    stdout='MIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\n',
    stderr=''
)
>>>
```

* ### `keep_empty_lines=True`
When `False` and `convert_stdout_stderr_to_list` is `True`, empty lines form `output.stdout` and `output.stderr` lists are removed.

In the below example, there is an empty line after the first line `MIT License`, but `output.stdout` list doesn't contain the empty line.

⚠️ This parameter does not change the way output is printed.
```python
>>> output = ss('head -3 LICEN*', keep_empty_lines=False)
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>> print(output)
CompletedProcess(
    args='head LICEN*',
    returncode=0,
    stdout=['MIT License', 'Permission is hereby granted, free of charge, to any person obtaining a copy'],
    stderr=[]
)
>>>
```

* ### `exit_on_error=True`
When `False`, a command exiting with a non-`0` return code doesn't cause the `python3` process to exit.
Afterward, `subprocess.CalledProcessError` exception object is returned so that the caller can further examine the error.

This is useful for using `grep` to monitor for something to disappear.
In the below example, `grep` is waiting for `process_waiting_to_finish` process to complete and exit.
```python
>>> output = ss('ps | grep "[p]rocess_waiting_to_finish"', print_output_on_error=False, exit_on_error=False)
>>> print(type(output))
<class 'subprocess.CalledProcessError'>
>>> print(output.returncode)
1
```
Examining the output's return code is important. In the below example, we have specified an invalid flag `-Y` to `grep`,
and as a result `grep` exited with `2`. This is different from the previous example which exited with `1`,
which signals that the error is about missing search results, as opposed to failing because of an invalid flag.
```python
>>> output = ss('ps | grep -Y "[p]rocess_waiting_to_finish"', print_output_on_error=False, exit_on_error=False)
>>> print(output.returncode)
2
```

* ### `echo=False`
When `True`, the command is printed before the output is printed. This is useful for creating a screen capture which shows the command that was run.

⚠️ The leading `$` does not change to `#` even if you're `root`. PR welcome.
```python
>>> output = ss('head -3 LICEN*', echo=True)
$ head -3 LICEN*
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>>
```

* ### `timeout=60`
Number of seconds to wait for the process to finish before exiting with an error. Since all calls are synchronous, it's not possible to see the output until the command exits.

In the below example, the exception detail was printed because `print_output_on_error` defaults to `True`, and the `python3` process exited because `exit_on_error` also defaults to `True`.
```python
>>> ss('sleep 10', timeout=3)
Command 'sleep 10' timed out after 3 seconds
$
```
