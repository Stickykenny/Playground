function getLastRowCol(sheet, column) {
  let lastRow = 1;
  while (sheet.getRange(lastRow, column).getValue() != "") {
    lastRow += 1;
  }
  return lastRow;
}

function myFunction() {
  var spreadsheetID = "123123123123123123123123123";
  var playlistID = "123123123123123123123123123";

  var maxVideosToCheck = 10;

  var sheet =
    SpreadsheetApp.openById(spreadsheetID).getSheetByName("Main Sheet");
  var lr = sheet.getLastRow();

  for (var i = 3; i <= lr; i++) {
    var channelId = sheet.getRange(i, 3).getValue();
    var channelName = sheet.getRange(i, 2).getValue();

    Logger.log(sheet.getRange(i, 2).getValue());

    /*
    // OLDER APPROACH : API IS BUGGED DOESNT WORK
    var results = YouTube.Search.list('id,snippet', {
        channelId: channelId,
        maxResults: maxVideosToCheck,    
        order: "date" // Seems like this is not working //TODO // YOUTUBE API PROBLEM SEE https://issuetracker.google.com/issues/35172972 
        // Doesn't order correctly and randomly take vid
      });
    */

    var channelUploadPlaylist = channelId[0] + "U" + channelId.slice(2);
    var results = YouTube.PlaylistItems.list("snippet", {
      maxResults: 10,
      playlistId: channelUploadPlaylist,
    });

    var watchedVideosSheet2 =
      SpreadsheetApp.openById(spreadsheetID).getSheetByName("WatchedVid2.0");

    // Search for the column of watched videos related to correct channel id instead of watched ids of all
    var watchedVideosSheetLC = watchedVideosSheet2.getLastColumn();
    var foundColumn = false;
    var currentColumn = -1;

    for (var k = 1; k <= watchedVideosSheetLC; k++) {
      if (watchedVideosSheet2.getRange(2, k).getValue() == channelId) {
        currentColumn = k;
        foundColumn = true;
        break;
      }
    }
    if (!foundColumn) {
      watchedVideosSheet2
        .getRange(1, watchedVideosSheetLC + 1)
        .setValue(channelName);
      watchedVideosSheet2
        .getRange(2, watchedVideosSheetLC + 1)
        .setValue(channelId);
      currentColumn = watchedVideosSheetLC + 1;
      console.info(
        "added new column for " + channelName + " of Id : " + channelId
      );
    }
    var watchedVideosSheet2LR = getLastRowCol(
      watchedVideosSheet2,
      currentColumn
    );

    for (var j = 0; j < maxVideosToCheck; j++) {
      try {
        Logger.log(
          results.items[j].snippet.title +
            " ---  " +
            results.items[j].snippet.publishedAt
        );
        var alreadyAdded = false;

        for (var k = 1; k <= watchedVideosSheet2LR; k++) {
          if (
            watchedVideosSheet2
              .getRange(k, currentColumn)
              .getValue()
              .indexOf(results.items[j].snippet.resourceId.videoId) > -1
          ) {
            Logger.log("vid already added");
            alreadyAdded = true;
            break;
          }
        }

        if (!alreadyAdded) {
          //var details = {videoId: results.items[j].id.videoId,kind: 'youtube#video'}; // OLDER API
          var details = {
            videoId: results.items[0].snippet.resourceId.videoId,
            kind: "youtube#video",
          };
          var resource = {
            snippet: { playlistId: playlistID, resourceId: details },
          };

          try {
            Logger.log("Adding this video : " + results.items[j].snippet.title);
            YouTube.PlaylistItems.insert(resource, "snippet");

            /*Example ressource required to add to playlist
            { snippet:  
            { playlistId: '123123123123123123123123123',
            resourceId: { videoId: 'g5Uvq7OD6zk', kind: 'youtube#video' } } }
              */

            //Adding to the sheet "Watched Videos" for checking if that video is added or not
            console.log(watchedVideosSheet2LR);
            console.log(results.items[j].snippet.resourceId.videoId);
            watchedVideosSheet2
              .getRange(watchedVideosSheet2LR, currentColumn)
              .setValue(results.items[j].snippet.resourceId.videoId);
            //.setValue(results.items[j].id.videoId);
            watchedVideosSheet2LR += 1;

            console.log("ok");
          } catch (e) {
            Logger.log("failed inserting");
            Logger.log(e.toString());
          }
        }
      } catch (e) {
        console.error("myFunction() yielded an error: " + e);
        console.error("On this item :" + results.items[j]);
      }
    }

    sheet.getRange(i, 4).setValue(results.items[0].id.videoId);
  }
}
