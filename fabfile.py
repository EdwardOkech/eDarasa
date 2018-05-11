from fabric.api import *

prod_server = 'fraogongi@web512.webfaction.com'

def prod():
    env.hosts = [prod_server]
    env.remote_app_dir = '~/webapps/workstry_app/workstry_project/jmlms/jmlms'
    env.remote_apache_dir = '~/webapps/workstry_app/apache2'
    env.remote_venv_dir = '~/webapps/workstry_app/venv'
    
def commit():
    message = raw_input("Enter a git commit message:  ")
    local("git add -A && git commit -m \"%s\"" % message)
    local("git push origin master")
    print "Changes have been pushed to remote repository..."
    
def collectstatic():
    require('hosts', provided_by=[prod])
    run("cd %s; python manage.py collectstatic --noinput" % env.remote_app_dir)
    
def restart():
    """Restart apache on the server."""
    require('hosts', provided_by=[prod])
    require('remote_apache_dir', provided_by=[prod])

    run("%s/bin/restart;" % (env.remote_apache_dir))
    
def deploy():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])
    require('remote_venv_dir', provided_by=[prod])

    # First lets commit changes to bitbucket ( Should really change to allow for cases when there is nothing to commit.)
    commit()
    
    with prefix("source %s/bin/activate" % env.remote_venv_dir):
        with cd(env.remote_app_dir):
    
            # Now lets pull the changes to the server
            run("git pull origin master")
            
            # Installing the requirements
            run('pip install -r jm_lms/requirements/requirements.txt')

            # Update the database schema
            run('python manage.py migrate --settings=jm_lms.settings.prod')
            
            # Update static media files
            #collectstatic()
            run('python manage.py collectstatic --noinput --settings=jm_lms.settings.prod')
            
            # Finally, restart apache2
            restart()
