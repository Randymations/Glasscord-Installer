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
    print('Install/Update Glasscord - Glasscord by AryToNeX - Installer by Randymations\n')
    mainpath = input('If Discord is installed in its default location, press ENTER now. Otherwise, submit the installation path. (Normally under Local AppData) > \n')
    print()
    if mainpath == '':
        mainpath = os.path.expandvars('%LOCALAPPDATA%/Discord/')
    else:
        mainpath = mainpath + '/'
    dircheck('Error: Invalid path')
    for i in range(len(files)):
        if files[i][:4] == 'app-':
            versions.append(int(files[i][-3:]))
    if len(versions) == 0:
        end('Error: No builds detected')
    for i in range(len(files)):
        if files[i][-3:] == str(max(versions)):
            mainpath = mainpath + files[i] + '/resources/'
    dircheck('Error: "resources" folder missing')
    mainpath = mainpath + 'app/'
    dircheck('Error: "app" folder missing')
    try:
        infile = open(mainpath+'package.json', 'r')
        file = json.load(infile)
        infile.close()
    except:
        end('Error: "package.json" file missing')
    if file['main'] == './glasscord.asar':
        timeprint('Previous Glasscord installation detected')
        if not os.path.isfile(mainpath+'package.original.json'):
            end('Error: "package.original.json" file missing')
        update = True
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
    infile = open(mainpath+'package.original.json', 'w')
    json.dump(file, infile)
    infile.close()
    timeprint('"package.original.json" created')
    file['main'] = './glasscord.asar'
    infile = open(mainpath+'package.json', 'w')
    json.dump(file, infile)
    infile.close()
    timeprint('"package.json" altered')
    print('Installation successful')
    end('Visit https://github.com/AryToNeX/Glasscord/ for more information.')

def end(message):
    if message[:6] == 'Error:':
        timeprint(message)
        print('\nVisit https://github.com/AryToNeX/Glasscord/ for manual installation instructions.')
    else:
        print(f'\n{message} (You may now close this window)')
    while True:
        pass

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
