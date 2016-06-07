import subprocess

# Builder method for API/Error handling.
def syscall(command):
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    # Handle if we got an stderr or stdout, return the correct one.
    if err is None:
        return out
    else:
        return err