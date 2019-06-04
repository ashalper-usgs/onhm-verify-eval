import os

# Assumes this runs in the "work_dir" where PRMS ran.
fname = './output/NHM-PRMS.out'

# The "minimum" run time is set to 1 minute. This means that if the PRMS
# run takes less than one minute, it was too fast and assume that the run
# failed.
min_time = 1
verified = True

cwd = os.getcwd()
print('prms_verifier: cwd = ' + cwd)

# If the "NHM-PRMS.out" file is not there, assume the run failed.
if not os.path.isfile(fname):
    print('prms_verifier: ' + fname + ' not found')
    verified = False
    
else:

    # Read through the "NHM-PRMS.out" file. If the line that starts with "Execution elapsed time"
    # is not there, then PRMS did not make it all the way through the time step loop and assumed the
    # run failed.
    with open(fname, 'r') as f:
        found = False
        for line in f:
            if 'Execution elapsed time' in line:
                found = True
                break
                
        if not found:
            print('prms_verifier: PRMS did not make it through the time loop')
            verified = False
            
        else:
            tok = line.split()
            mn = int(tok[3])
            sc = float(tok[5])

            # If the run time is less than "min_time", then PRMS raced through not really running
            # and assumed the run failed.
            if mn < min_time:
                print('prms_verifier: execution time ' + str(mn) + ':' + str(sc) + ' to short')
                verified = False


print(verified)  # this should be the return value of the container

# Create an empty file where the name indicates the status of the last check.
fn_true = 'PRMS_VERIFIED_TRUE.txt'
fn_false = 'PRMS_VERIFIED_FALSE.txt'
if os.path.isfile(fn_true):
    os.remove(fn_true)

if os.path.isfile(fn_false):
    os.remove(fn_false)

if verified:
    fn2 = fn_true
else:
    fn2 = fn_false

try:
    os.utime(fn2, None)
except OSError:
    open(fn2, 'a').close()
