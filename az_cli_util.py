from azure.cli.core import get_default_cli
import re
#https://aka.ms/azadsp-cli
# az cli util for auto logging in and also invoking commands
# error handling is included

def az_cli(args_str, verbose=True, debug=False):
	'''
	Invoke az_cli commands and make sure they executed correctly.
	Incase not logged-in, raise specific error
	'''
	# argument span
	args = f'{args_str} -o none'.split()
	args = [sub.replace('#', ' ') for sub in args] # When some argument needs spaces use '#' instead (# is comment in linux, thus a reasonable choice)
	if debug:
		print(args)
	
	# Invoke client
	cli = get_default_cli()
	res = cli.invoke(args)
	if cli.result.result:
		# Success
		return cli.result.result
	elif cli.result.error:
		# Failure
		if verbose:
			print(cli.result.error)
		#Please run 'az login' to setup account.
		x = re.findall("Please run .az login. to setup account", str(cli.result.error))
		if len(x) > 0:
			raise EnvironmentError('AZ Login Error')
		return None

# --------------------------------------------------
# Login
# --------------------------------------------------
def az_login():
	'''
	Sign-in to azure if not already signed in from terminal
	'''
	try:
		# Check we already logged in
		az_cli('ad signed-in-user show', verbose=False)
		print('az already logged_in')
	except EnvironmentError:
		print('az is not logged in, please perform manual login')
		az_cli('login --use-device-code')#, echo=True)
