from termcolor import colored
import subprocess
import sys


def _print_output(output):
    if output.stdout:
        print(output.stdout)
    if output.stderr:
        print(colored(output.stderr, "red"), file=sys.stderr)


def run(
        cmd_str,
        print_output_on_success=True,
        print_output_on_error=True,
        convert_stdout_stderr_to_list=True,
        show_empty_lines=True,
        exit_on_error=True,
        echo=False,
        timeout=60,
):

    if echo:
        print("$ " + cmd_str)

    try:
        output = subprocess.run(
            cmd_str,
            capture_output=True,
            timeout=timeout,
            check=True,
            shell=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        if print_output_on_error:
            _print_output(e)
        if exit_on_error:
            sys.exit(e.returncode)
        else:
            return e

    if print_output_on_success:
        _print_output(output)

    if convert_stdout_stderr_to_list:
        output.stdout = [x.strip() for x in output.stdout.split("\n") if show_empty_lines or x.strip()]
        output.stderr = [x.strip() for x in output.stderr.split("\n") if show_empty_lines or x.strip()]

    return output
