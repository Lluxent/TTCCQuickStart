from ClashLauncher import ClashLauncher
from ClashPatcher import ClashPatcher

import argparse, sys
ap = argparse.ArgumentParser(prog = 'launcher', description = 'Command-Line Launcher for Corporate Clash, by luna#4811', allow_abbrev = False)

ap.add_argument('--account', '-a', type = int, help = "Specifies an account to use to log in.")
ap.add_argument('--toon', '-t', type = int, help = "Specifies a toon, by index, to use to log in. 0 is top left, 5 is bottom right.")
ap.add_argument('--district', '-d', type = str, help = "Specifies a target district to log into. No district will launch the main menu page. Use '--district any' to guarantee a random district.")
ap.add_argument('--realm', '-r', type = str, help = "Forces a target realm to try to log into, overriding accounts.json. If unsure, don't use this flag.")
ap.add_argument('--continuous', '-c', action = 'store_true', help = "Will attempt to keep trying to relog into the game upon disconnecting or crashing.")

up = ap.add_mutually_exclusive_group()
up.add_argument('--forceupdate', '-fu', action = 'store_true', help = "Launch the game after forcing an update check.")
up.add_argument('--update', '-u', action = 'store_true', help = "Update the game. Does not launch it afterwards.")
up.add_argument('--updateloop', '-ul', action = 'store_true', help = "Continuously check the game for updates, runs until stopped, or an update is found.")

args = ap.parse_args()

pa = ClashPatcher()

if args.account is not None:
    ac = args.account
    toon = -1
    dist = ''
    if args.toon is not None:
        toon = args.toon
    if args.district.lower() == 'any':
        dist = ''
    elif args.district is not None:
        dist = args.district

    if args.forceupdate:
        pa.run()

    lc = ClashLauncher(ac, toon, dist)
    lc.overrideRealm(args.realm)
    while True:
        lc.connect()
        if not args.continuous:
            break
        print('----------------------------------------\nReconnecting due to "--continuous" flag.\n----------------------------------------')
    sys.exit()
if args.toon:
    print('Warning: Toon was specified without an account, ignoring.')
if args.district:
    print('Warning: District was specified without an account, ignoring.')

if args.update or args.updateloop:
    while True:
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time, '| Checking for update...')
        if not pa.isGameUpdated():
            print('Local files are old, update them?')
            userInput: str = input('Y/N >> ')
            if userInput.lower() == 'y':
                updated = True
                pa.run()
            sys.exit()
        if args.update:
            print('Gamefiles are up to date.')
            sys.exit()

print('No parameters? Use --account to log into the game, or use --update to update the game. Use -h for a list of all commands.')