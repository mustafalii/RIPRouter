import sys

while(True):
    try:
        files = input("enter input")
    except EOFError:
        print("closing")
        sys.stdin = open('/dev/tty', 'r')
        # sys.stdin.close()
        # sys.stdin.flush()
        # exit()