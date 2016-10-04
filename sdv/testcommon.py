
def fabric_run(cmd):

    if installation_mode=='source':
        cmd=cmd.replace('sudo service synda','synda daemon')
        cmd=cmd.replace('sudo ','')
        cmd=cmd.replace('/etc/synda/sdt','/home/%s/sdt/conf'%normal_user)
    elif installation_mode=='system_package':
        pass # nothing to do as this is the default

    if exec_mode=='local':
        fabric.api.local(cmd)
    else:
        fabric.api.run(cmd)
