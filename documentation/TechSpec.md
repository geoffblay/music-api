# rock-api
CSC365 Databases Project

### Programmers: 
* Cole Robinson: crobin27@calpoly.edu
* Geoff Blaylock: blaylock@calpoly.edu


This API will allow users to quickly access information about their favorite artists, albums, and songs. We will include endpoints that track items like genre, release year, runtime, and more. Or they can choose to list tracks, albums, or artists based on many sorting and filtering options. Additionally, users will be able to write new music data to the database.

**v3 Phenomenon Write-Up**





**Technical Specification for Music API**

Cole Robinson, Geoff Blaylock

**Overview**

Our music API will hold information on all different aspects of the music industry. The database will consist of multiple schemas such as artist, album, song, and playlist. Utilizing this data, the API will be able to make music recommendations, artist recommendations, album recommendations, and create playlists based on given input. Additionally, the API will have read/write capabilities, allowing users to update the database themselves. 

**User Stories**


1. As a user, I want to search for a specific song, artist, or album so that I can find the desired information quickly.
2. As a musician, I want to add new songs, artists, and albums to the database so my music can be shared with others.
3. As a musician, I would like to be able to update or delete my music from the database.
4. As a user, I want to be able to have a playlist created for me based on my previous song, artist, or album interests. 
5. As a user, I would like to find similar music from individual songs, artists, or albums to broaden my music knowledge. 

**Endpoints**

**1.) /artists/: (GET)** This endpoint returns a list of artists. For each artist, the following information is returned:

* artist_id: internal id of the artist
* name: the name of the artist

You can filter for artists whose names contain a string by using the *name* query parameter

The *limit* and *offset* query parameters can be used to limit the number of results returned and to offset the results returned. For example, if you wanted to return the second page of results with 10 results per page, you would use the following query parameters: ?limit=10&offset=10

**2.) /artists/{id}: (GET)** This endpoint will return a single artist by its identifier: For each artist, the following is returned:

* artist_id: internal id of the artist
* name: the name of the artist
* birthdate: the birthdate of the artist
* deathdate: the deathdate of the artsit (if applicable)
* gender: the gender of the artist
* age: the current age of the artist
* tracks: a list of tracks associated with the artist.
* albums: a list of albums associated with the artist.

Each track is represented by a dictionary with the following keys:

* track_id: the internal id of the track
* title: the title of the track
* release_date: the release date of the track

Each album is represented by a dictionary with the following keys:

* album_id: the internal id of the album
* title: the title of the album
* release_date: the release date of the album

**3.) /albums/: (GET)** This endpoint returns a list of albums. For each album, the following information is returned:

* album_id: the internal id of the album
* title: the title of the album
* release_date: the release date of the album
* artist_names: a list of all of the artist names that the album belongs to

You can filter for albums whose titles contain a string by using the *name* query parameter

The *limit* and *offset* query parameters can be used to limit the number of results returned and to offset the results returned. For example, if you wanted to return the second page of results with 10 results per page, you would use the following query parameters: ?limit=10&offset=10

**4.) /albums/{id}: (GET)** This endpoint will return a single album by its identifier

* album_id: the internal id of the album
* title: the title of the album
* release_date: the release date of the album
* artists: a list of artists associated with the album
* tracks: a list of tracks associated with the album

Each artist is represented by a dictionary with the following keys:

* artist_id: the internal id of the artist
* name: the name of the artist

Each track is represented by a dictionary with the following keys:

* track_id: the internal id of the track
* title: the title of the track
* runtime: the runtime of the track

**5.) /albums/recommend/: (GET)** This endpoint will return an album based on a location, the time of day at that location, the user's current mood, and the preffered number of tracks.

* album_id: the internal id of the album
* title: the title of the album
* release_date: the release date of the album
* genre: the genre of the album
* artists: a list of artists associated with the album
* tracks: a list of tracks associated with the album

Each artist is represented by a dictionary with the following keys:

* artist_id: the internal id of the artist
* name: the name of the artist

Each track is represented by a dictionary with the following keys:

* track_id: the internal id of the track
* title: the title of the track
* runtime: the runtime of the track

You can curate the album recommendation by using the following query parameters:

* location: the location of the user. Specifying location will return tracks that match the current weather and time in a given location. Location must be a valid city, US zip, or lat,long (decimal degree, e.g: 35.2828,120.6596).
* mood: the mood of the user. Specifying mood will return tracks that match the mood of the user. Mood must be one of the following: happy, party, workout, focus, chill, sleep, heartbroken
* num_tracks: specifying num_tracks will return an album with close to the specified number of tracks.

**6.) /tracks/: (GET)** This endpoint returns a list of tracks. For each track, the following information is returned:

* track_id: the internal id of the track
* title: the title of the track
* runtime: the runtime of the track
* album_title: the title of the album that the track belongs to
* artist_names: a list of all of the artist names that the track belongs to

You can filter for tracks whose titles contain a string by using the *name* query parameter

The *limit* and *offset* query parameters can be used to limit the number of results returned and to offset the results returned. For example, if you wanted to return the second page of results with 10 results per page, you would use the following query parameters: ?limit=10&offset=10

**7.) /tracks/: (POST)** This endpoint is used to add a new track to the database. The following information is required:

* title: the title of the track
* album_id: the internal id of the album that the track belongs to
* runtime: the runtime of the track
* genre: the genre of the track
* release_date: the release date of the track
* artist_ids: a list of all of the artist ids that the track belongs to
* vibe_score: the vibe score of the track

**8.) /tracks/{track_id}: (GET)** This endpoint will return a single track by its identifier. For each track, the following information is returned:

* track_id: the internal id of the track
* title: the title of the track
* runtime: the runtime of the track
* genre: the genre of the track
* release_date: the release date of the track
* album: the album that the track belongs to
* artists: a list of artists associated with the track

Each artist is represented by a dictionary with the following keys:

* artist_id: the internal id of the artist
* name: the name of the artist

**9.) /playlists/{playlist_id}: (GET)** This endpoint will return a single playlist by its identifier. For each playlist, the following information is returned:

* playlist_id: the internal id of the playlist
* name: the name of the playlist
* tracks: a list of tracks associated with the playlist

Each track is represented by a dictionary with the following keys:

* track_id: the internal id of the track
* title: the title of the track
* runtime: the runtime of the track
* artists: a list of artists associated with the track

Each artist is represented by a dictionary with the following keys:

* artist_id: the internal id of the artist
* name: the name of the artist

**10.) /playlists/{playlist_id}: (DELETE)** This endpoint will delete a single playlist by its identifier.

**11.) /playlists/{playlist_id}/tracks/{track_id}: (DELETE)** This endpoint will delete a single track from a playlist by its identifier.

**12.) /playlists/generate/: (GET)** This endpoint will generate a playlist based on a location, the time of day at that location, the user's current mood, and the preffered number of tracks.

* tracks: a list of tracks associated with the playlist

Each track is represented by a dictionary with the following keys:

* track_id: the internal id of the track
* title: the title of the track
* runtime: the runtime of the track
* genre: the genre of the track
* artists: a list of artists associated with the track

Each artist is represented by a dictionary with the following keys:

* artist_id: the internal id of the artist
* name: the name of the artist

You can curate the playlist by using the following query parameters:

* location: the location of the user. Specifying location will return tracks that match the current weather and time in a given location. Location must be a valid city, US zip, or lat,long (decimal degree, e.g: 35.2828,120.6596).
* mood: the mood of the user. Specifying mood will return tracks that match the mood of the user. Mood must be one of the following: happy, party, workout, focus, chill, sleep, heartbroken
* num_tracks: specifying num_tracks will return a playlist with the specified number of tracks.

**13.) /playlists/{playlist_id}/track/{track_id} (PUT)** This endpoint will add a track to a playlist by its identifier. Accepts a JSON object with the following fields:

* playlist_id: the internal id of the playlist
* track_id: the internal id of the track

**14.) /playlists/ (POST)** This endpoint will create a new playlist. Accepts a JSON object with the following fields:

* name: the name of the playlist
* track_ids: a list of track ids to add to the playlist
* user_id: the internal id of the user

**15.) /users/ (POST)** This endpoint will create a new user. Accepts a JSON object with the following fields:

* username: the username of the user - must be larger than four characters
* password: the password of the user - must be larger than eight characters

This endpoint returns the internal id of the user.

**16.) /users/validate/ (POST)** This endpoint will validate a user. Accepts a JSON object with the following fields:

* username: the username of the user
* password: the password of the user

This endpoint returns True if the user is valid.

**Edge Cases**

**1.) Singles:** To handle cases where a user may search for a single that does not belong to an album, we should notify the user. 

**2.) Multiple artist tracks:** In the case that multiple artists are credited for a track, our API should return a data structure that contains data for all artists credited.

**3) Bands:** In the case that users search for a band or group using the artist endpoint, a data structure containing relevant information on all members should be returned.

**4) Input validation:** When input does not correspond to any valid data, make sure to raise a detailed error documenting the issue. 

**5) Multi genre:** In the case that a song or album falls into multiple genres, a data structure containing both genres should be returned. 

**6) Duplicate Entries** In the event that a song, album, or artist potentially gets posted twice, this could lead to undesirable behavior and have transitive effects on other attributes. In order to prevent this, we will make sure that our schema definitions ensure that certain fields are unique. For instance, artist_name will likely be a unique key, as well as the combination of song_id and artist_id. 

**7) Missing/Incomplete Data** In the event that a song, album, or artist potentially gets posted twice, this could lead to undesirable behavior and have transitive effects on other attributes. In order to prevent this, we will make sure that our schema definitions ensure that certain fields are unique. For instance, artist_name will likely be a unique key, as well as the combination of song_id and artist_id. 

**8)Large Requests** Our query parameters for the search function will help to limit the amount of data requested by the user. Though we may decide to define a hard limit on the amount of data returned, if this proves to be an issue. 
