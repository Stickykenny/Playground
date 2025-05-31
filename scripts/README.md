# Minor scripts

For personnal usage and archiving purpose

## Google Appscripts

HideRowsByCOLOR.gs

NewVidsToPlaylist.gs

Why not directly put it into the Watch Later Playlist ?

> Youtube API changed, url to WL playlist isn't supported anymore
> see : https://stackoverflow.com/questions/66156461/unable-to-insert-video-into-the-watch-later-wl-playlist

Why not use YouTube.Search.list() ?

> Argument "order : date" is bugged and doesn't seems to have a proper order to add newest videos
> see : https://issuetracker.google.com/issues/128673552

Why have a WatchedVid2.0 sheet ?

> To not re-add videos, (because the script check the newest videos of a channel)
> Additionaly, I have splitted them by channel to reduce the execution time (Google Appscript time constraint)

Will you publish the Excel linked to this script ?

> No need to, it's a really a simple Excel if you understand the script
