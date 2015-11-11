import xbmc
import xbmcaddon

import csv
import os.path
import subprocess

def light(color,blink=''):
    neouartCmd = [addonResourcePath + 'neouart','-i']   

    if blink == 'rainbow':
	f = open(addonResourcePath + 'rainbow.nua','r')
        subprocess.call(neouartCmd,stdin=f)
    elif 1000 >= blink >= 1:
        duration = hex(blink / 10).split('x')[1]
        repeat = 1000 / blink
        subprocess.call(neouartCmd + [duration + x for x in ['000000', color]] * repeat)
    else:
        subprocess.call(neouartCmd + ['64' + color])

def run():
    csvFile = open(addonResourcePath + 'episodes.csv','rb')        
    episodesTable = []
    for kv in csv.DictReader(csvFile):
        episodesTable.append(kv)

    while not xbmc.abortRequested:
        if xbmc.Player().isPlaying():
            playingFile = xbmc.Player().getPlayingFile()
            playTime = xbmc.Player().getTime()
            she = her = ( x for x in episodesTable if x['filename'] in playingFile ).next()
            blink = ''
            if she['kisses']:
                leftTime = int(she['kisses']) - playTime
                if 180 >= leftTime > 120:
                    blink = 1000
                elif 120 >= leftTime > 60:
                    blink = 500
                elif 60 >= leftTime > 10:
                    blink = 250
                elif 10 >= leftTime > 0:
                    blink = 50
                elif 0 >= leftTime > -5:
                    blink = 'rainbow'
            light(her['color'],blink)
            #xbmc.sleep(1000)
        else:
            light('000000')
            xbmc.sleep(5000)

if __name__ == '__main__':
    addon = xbmcaddon.Addon()
    addonPath = addon.getAddonInfo('path')
    addonResourcePath = xbmc.translatePath(os.path.join(addonPath, 'resources')) + '/'

    run()
