import sys
with open(sys.argv[1]) as f:
    lines = f.readlines()
print(lines)
if '2\n' in lines and '5\n' in lines:
    # Failure reproduced; fail
    sys.exit(1)
sys.exit(0)