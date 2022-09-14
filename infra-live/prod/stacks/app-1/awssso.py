from subprocess import Popen, PIPE
proc = Popen(['aws configure sso'],shell=True, stdin=PIPE)
proc.stdin.write(bytes("https://d-9267024070.awsapps.com/start#/\n",'UTF-8'))

proc.stdin.write(bytes("us-west-2\n",'UTF-8'))

proc.stdin.write(bytes("us-west-2\n",'UTF-8'))
proc.stdin.write(bytes("json\n",'UTF-8'))
proc.stdin.write(bytes("\n",'UTF-8'))


