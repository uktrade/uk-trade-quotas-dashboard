import datetime
import sys

sys.stdout.buffer.write(b'generated\n')
sys.stdout.buffer.write(str(datetime.datetime.now().timestamp()).encode('utf-8'))
