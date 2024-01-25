# Resources and Stuff

- 

## Models and Structure

Track: 
- title/bpm/key
- fks: genre_id
- ∞-∞: playlists(PlayTrack)/artists(thru artist_track)
- class: `create_track_data`
  - needs session, track(?), playlist
  - find or creates track with helper, then creates `PlayTrack` assoc
- instances: `times_played`, `average_length_played`

Playlist: 
- name
- 1-∞: play_tracks
- ∞-∞: tracks(play_tracks)
- class: `create_sets`
  - needs setlist(from parser)
  - creates `Playlist` (and commits)
  - then `Track.create_track_data` for each tracks in setlist

PlayTrack: 
- the track when actually played in a mix.
- playtime/start_time/end_time
- fks: playlist_id, track_id

Artist: (currently just for doc)
- name

artist_track:
- join of track/artist

Genre
- name