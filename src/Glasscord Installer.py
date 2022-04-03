import os
import json
import urllib.request
from datetime import datetime

files = []
versions = []
mainpath = ''
update = False

def main():
    global files
    global versions
    global mainpath
    global update
    temp = ''
    appfiles = []
    print('Install/Update Glasscord - Glasscord by AryToNeX - Installer by Randymations\n')
    install = True
    if input('Press ENTER to install/update. Otherwise, submit "X" (without quotes) to uninstall. > ').lower() == 'x':
        install = False
        print('Ensure Discord is fully closed before continuing')
    mainpath = input('If Discord is installed in its default location, press ENTER now.\nOtherwise, submit the installation path. (Normally under Local AppData) >\n')
    print()
    if mainpath == '':
        mainpath = os.path.expandvars('%LOCALAPPDATA%/Discord/')
    else:
        mainpath = mainpath + '/'
    dircheck('Error: Invalid path')
    for i in range(len(files)):
        if files[i][:4] == 'app-':
            for j in range(len(files[i])):
                    if files[i][j].isnumeric():
                        temp = temp + files[i][j]
            versions.append(int(temp))
            appfiles.append(files[i])
    if len(versions) == 0:
        end('Error: No builds detected')
    for i in range(len(appfiles)):
        if versions[i] == max(versions):
            timeprint(f'Found build "{appfiles[i]}"')
            mainpath = mainpath + appfiles[i] + '/resources/'
    dircheck('Error: "resources" folder missing')
    mainpath = mainpath + 'app/'
    dircheck('Error: "app" folder missing')
    if not install:
        operations = 0
        successes = 0
        installed = True
        if not os.path.exists(mainpath+'package.original.json'):
            timeprint('Error: "package.original.json" missing - Checking "package.json"...')
            if not os.path.exists(mainpath+'package.json'):
                end('Error: "package.json" missing - Reinstall Discord')
            try:
                infile = open(mainpath+'package.json', 'r')
                file = json.load(infile)
                infile.close()
            except:
                end('Error: Unable to access "package.json"')
            try:
                if file['main'] == './glasscord.asar':
                    end('Error: "package.original.json" required - Reinstall Discord')
                installed = False
                timeprint('Glasscord likely not installed - Continuing with deletions')
            except:
                end('"package.json" invalid format - Reinstall Discord')
        timeprint('Deleting files...')
        for i in range(len(files)):
            if files[i][:9] == 'glasscord' or (installed and files[i] == 'package.json'):
                operations += 1
                timeprint(f'Deleting "{files[i]}"...')
                try:
                    os.remove(mainpath+files[i])
                    timeprint('Deletion successful')
                    successes += 1
                except:
                    timeprint('Error: Unable to delete file')
        timeprint(f'Deleted {successes} of {operations} files')
        if os.path.exists(mainpath+'package.original.json'):
            timeprint('Restoring "package.json"...')
            operations += 1
            try:
                os.rename(mainpath+'package.original.json',mainpath+'package.json')
                successes += 1
            except:
                timeprint('Error: Unable to restore "package.json"')
        timeprint(f'Successfully completed {successes} of {operations} operations')
        if operations == successes:
            end('Uninstallation successful - Reinstall Discord if any issues arise')
        end('Uninstallation unsuccessful - Reinstall Discord')
    try:
        infile = open(mainpath+'package.json', 'r')
        file = json.load(infile)
        infile.close()
    except:
        end('Error: Unable to access "package.json"')
    try:
        if file['main'] == './glasscord.asar':
            timeprint('Previous Glasscord installation detected')
            if not os.path.isfile(mainpath+'package.original.json'):
                end('Error: "package.original.json" file missing - Reinstall Discord')
            update = True
    except:
        end('"package.json" invalid format - Reinstall Discord')
    timeprint('File checks passed')
    try:
        if update:
            timeprint('Updating Glasscord')
        timeprint('Begun download of "glasscord.asar"...')
        glasscord, headers = urllib.request.urlretrieve('https://github.com/AryToNeX/Glasscord/releases/download/v0.9999.9999/glasscord.asar', filename=mainpath + 'glasscord.asar')
        timeprint('Download complete')
    except:
        end('Error: Download failed')
    if update:
        end('Update successful')
    try:
        infile = open(mainpath+'package.original.json', 'w')
        json.dump(file, infile)
        infile.close()
    except:
        end('Error: Unable to create/access "package.original.json"')
    timeprint('"package.original.json" created')
    file['main'] = './glasscord.asar'
    try:
        infile = open(mainpath+'package.json', 'w')
        json.dump(file, infile)
        infile.close()
    except:
        end('Error: Unable to access "package.json"')
    timeprint('"package.json" altered')
    print('Installation successful')
    end('Visit https://github.com/AryToNeX/Glasscord/ for more information.')

def end(message):
    if message[:6] == 'Error:':
        timeprint(message)
        print('\nVisit https://github.com/AryToNeX/Glasscord/ for manual installation instructions.')
    else:
        print(f'\n{message} (You may now close this window)')
    input()
    quit()

def dircheck(message):
    global files
    global mainpath
    try:
        files = os.listdir(mainpath)
    except:
        end(message)

def timeprint(message):
    print(f'[{datetime.now().time()}] {message}')

main()
