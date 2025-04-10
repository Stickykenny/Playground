/**
 * Various function used to hide/unhide rows in a Google Sheet
 * Functions are assigned on buttons
 */

var grey = "#808080"; // Use lowercase
var blue = "#0000ff";

function HideRowsByColor() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var lastRow = sheet.getLastRow();
  var hidingColor = "#ff0000"; // Default Red

  var backgrounds = sheet.getRange(1, 1, lastRow).getBackgrounds();
  var totalHidden = 0;
  for (i = 0; i < lastRow; i++) {
    if (backgrounds[i] == hidingColor) {
      sheet.hideRows(i + 1);
      totalHidden++;
    }
  }
  SpreadsheetApp.getUi().alert("Hidden a total of " + totalHidden + " rows");
}

function UncolorGrey() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var lastRow = sheet.getLastRow();
  var hidingColor = grey;

  var backgrounds = sheet.getRange(1, 1, lastRow).getBackgrounds();
  for (i = 0; i < lastRow; i++) {
    console.log(backgrounds[i]);
    if (backgrounds[i] == hidingColor) {
      sheet.getRange(i + 1, 1).setBackground("white");
    }
  }
}

function UnhideRows() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var allRows = sheet.getRange("A:A");

  sheet.unhideRow(allRows);
}

function HideRowsIfTooLate() {
  var sheet = SpreadsheetApp.openByUrl("URL_NOT_GIVEN").getSheetByName(
    "SHEETNAME_NOT_GIVEN"
  );
  var lastRow = sheet.getLastRow();

  var defaultColor = "#ffffff"; // Default White
  var backgrounds = sheet.getRange(1, 1, lastRow).getBackgrounds();
  var thresholdDelta = 30;
  let date = new Date();
  date.setDate(date.getDate() - 1);

  var today = Utilities.formatDate(date, "GMT-2", "yyyy-MM-dd");

  var data = sheet.getDataRange().getValues();

  for (i = 1; i < lastRow; i++) {
    var fetched_date = data[i][12];
    try {
      fetched_date = Utilities.formatDate(fetched_date, "GMT-2", "yyyy-MM-dd");
      if (fetched_date == today) {
        if (data[i][13] < thresholdDelta) {
          continue;
        }
        if (backgrounds[i] == defaultColor || backgrounds[i] == grey) {
          sheet.getRange(i + 1, 1).setBackground(grey);
          sheet.hideRows(i);
        }
      }
    } catch (error) {
      console.log(i);
      console.log(fetched_date);
      console.log(error.message, error.stack);
      continue;
    }
  }
}
