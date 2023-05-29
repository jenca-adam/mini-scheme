from .run import cmdline,run_str
import argparse

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-f","--file",type=str,default="",help="Run a file instead of cmd prompt",nargs=1)
    args=parser.parse_args()
    if args.file:
        with open(args.file[0])as f:
            run_str(f.read(),True)
    else:
        cmdline()
