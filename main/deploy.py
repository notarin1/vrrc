# def deploy(channel):
#     try:
#         if channel==24:
#             deploy = ['cd /home/pi/vrrc; git pull']
#             restart = ['systemctl restart vrrcd.service']
#             print(subprocess.check_output(deploy, shell=True))
#             print(subprocess.check_output(restart, shell=True))
#     except subprocess.CalledProcessError as e:
#         print(e.returncode)
#         print(e.cmd)
#         print(e.output)
