import os
import sys


def main(work_dir, fname, min_time):

    verified = True

    fn = work_dir + fname

# If the "NHM-PRMS.out" file is not there, assume the run failed.
    if not os.path.isfile(fn):
        print('prms_verifier: ' + fn + ' not found')
        verified = False

    else:

        # Read through the "NHM-PRMS.out" file. If the line that starts with "Execution elapsed time"
        # is not there, then PRMS did not make it all the way through the time step loop and assumed the
        # run failed.
        with open(fn, 'r') as f:
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

    # Create an empty file where the name indicates the status of the last check.
    fn_true = 'PRMS_VERIFIED_TRUE.txt'
    fn_false = 'PRMS_VERIFIED_FALSE.txt'
    if os.path.isfile(fn_true):
        os.remove(fn_true)

    if os.path.isfile(fn_false):
        os.remove(fn_false)

    if verified:
        fn2 = work_dir + fn_true
    else:
        fn2 = work_dir + fn_false

    try:
        os.utime(fn2, None)
    except OSError:
        open(fn2, 'a').close()

    if verified:
        return 0
    else:
        return 1


if __name__ == '__main__':
    # Assumes this runs in the "work_dir" where PRMS ran.
    # If no command line argument given, assume operational NHM
    work_dir = '/var/lib/nhm/NHM-PRMS_CONUS/'
    argc = len(sys.argv) - 1
    # print(argc)

    if argc == 1:
        print('setting dir = ' + sys.argv[1])
        work_dir = sys.argv[1]


    fname = 'output/NHM-PRMS.out'

    # The "minimum" run time is set to 1 minute. This means that if the PRMS
    # run takes less than one minute, it was too fast and assume that the run
    # failed.
    min_time = 1

    main(work_dir, fname, min_time)
