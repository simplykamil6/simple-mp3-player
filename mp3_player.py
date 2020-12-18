import os

from PySimpleGUI import Window, Input, WIN_CLOSED, FilesBrowse, Button, Text, theme
from pygame import mixer


class MP3Player:
    def __init__(self):
        self.playing = False
        self.played = False
        self.current_track_name = ''
        self.current_track_path = ''
        self.theme = 'DarkAmber'
        self.title = 'MP3 Player'
        self.cwd = os.getcwd()
        self.playlist = {}
        self.last_index_played = None
        self.button_mappings = {
            'files_selector': 'Select the mp3 track you want to play',
            'previous_button': 'Previous',
            'play_pause_button': 'Play or Stop',
            'next_button': 'Next'
        }

        self.layout = [
            [Input(key='files_selector', default_text=self.button_mappings['files_selector'], enable_events=True),
             FilesBrowse(key='files_selector_dialog')],
            [Button(key='previous_button', button_text=self.button_mappings['previous_button'], disabled=True),
             Button(key='play_pause_button',
                    button_text=self.button_mappings['play_pause_button'], disabled=True),
             Button(key='next_button', button_text=self.button_mappings['next_button'], disabled=True)],
            [Text(key='currently_playing_label', text='Currently playing', size=(14, 1), justification='c'),
             Text(key='playing_text', text='', size=(25, 1), justification='c')],
            [Text(key='playlist_text', text='', size=(25, 1), justification='c')]]

        mixer.init()

        theme(self.theme)
        self.window = Window('MP3 Player', self.layout,
                             element_justification='c')

        while True:
            event, values = self.window.read()
            if event == WIN_CLOSED:
                break

            elif event == 'previous_button':
                last_index = self.last_index_played
                next_index = self.last_index_played - 1
                playlist_index = [int(x) for x in self.playlist.keys()]

                if next_index < min(playlist_index):
                    max_index = max(playlist_index)
                    self.last_index_played = max_index
                    next_index = max_index
                else:
                    self.last_index_played = next_index

                mixer.music.unload()
                self.playlist[last_index]['loaded'] = False
                track = self.playlist[next_index]
                mixer.music.load(track['full_path'])

                self.current_track_name = track['name']
                self.current_track_path = track['full_path']
                self.window.Element(key='playing_text').Update(
                    track['name'].replace('.mp3', ''))

                if self.playing:
                    mixer.music.play()
                else:
                    self.played = False

            elif event == 'play_pause_button':
                if self.playlist.keys:
                    self.window.Element(
                        key='files_selector_dialog').Update(disabled=True)
                    self.window.Element(key='files_selector').Update(
                        ' ')  # bug? can't update 2 properties at once
                    self.window.Element(
                        key='files_selector').Update(disabled=True)

                    if self.playing:
                        if self.played:
                            mixer.music.pause()
                            self.playing = False
                    else:
                        track = self.playlist[self.last_index_played]
                        if self.played:
                            mixer.music.unpause()
                            self.playing = True
                        elif not track['loaded']:

                            self.current_track_name = track['name']
                            self.current_track_path = track['full_path']

                            mixer.music.load(self.current_track_path)
                            mixer.music.play()

                            self.playlist[self.last_index_played]['loaded'] = True
                            self.window.Element(key='playing_text').Update(
                                track['name'].replace('.mp3', ''))
                            self.played = True

                        self.playing = True

            elif event == 'next_button':
                last_index = self.last_index_played
                next_index = self.last_index_played + 1

                playlist_index = [int(x) for x in self.playlist.keys()]
                if next_index > max(playlist_index):
                    self.last_index_played = 0
                    next_index = 0
                else:
                    self.last_index_played = next_index

                mixer.music.unload()
                self.playlist[last_index]['loaded'] = False
                track = self.playlist[next_index]
                mixer.music.load(track['full_path'])

                self.current_track_name = track['name']
                self.current_track_path = track['full_path']
                self.window.Element(key='playing_text').Update(
                    track['name'].replace('.mp3', ''))

                if self.playing:
                    mixer.music.play()
                else:
                    self.played = False

            elif event == 'files_selector':
                files = values['files_selector'].split(';')

                for i, track in enumerate(files):
                    track_path = track.split('/')[1:]
                    path = f'/{"/".join(track_path[:-1])}'
                    name = track_path[-1:][0]

                    self.playlist[i] = {'path': path, 'name': name,
                                        'loaded': False, 'full_path': f'{path}/{name}'}

                self.last_index_played = 0
                songs = [self.playlist[key]['name'].replace(
                    '.mp3', '') for key in self.playlist.keys()]
                text = '\n'.join(songs)

                self.window.Element(key='playlist_text').Update(text)
                self.window.Element(key='playlist_text').set_size(
                    size=(25, len(songs)))
                self.window.Element(key='next_button').Update(disabled=False)
                self.window.Element(
                    key='previous_button').Update(disabled=False)
                self.window.Element(
                    key='play_pause_button').Update(disabled=False)

        self.window.close()


if __name__ == '__main__':
    MP3Player()
