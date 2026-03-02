/**
 * LPからのフォーム送信を受け取り、GmailとLINEに通知する
 */
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // 1. メッセージ本文を作成
    var messageText = createMessage(data);

    // 2. Gmailへの通知送信
    sendGmail(messageText);

    // 3. LINE Messaging APIへの通知送信
    sendLine(messageText);

    // 4. 成功レスポンスを返す
    return ContentService.createTextOutput(JSON.stringify({ status: "success" })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    console.log("エラー発生: " + error.toString());
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * 通知メッセージを作成する
 * @param {object} data - フォームから送信されたデータ
 * @returns {string} - 通知用の整形済みテキスト
 */
function createMessage(data) {
  var lpId = data.lp_id || "(IDなし)";
  var tel = data.tel || "(電話番号なし)";
  var selected = data.selected || "(選択なし)";
  var timestamp = data.timestamp || new Date().toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });

  var message = "【アメトメ】新規お問い合わせがありました\n";
  message += "------------------------------------\n";
  message += "問い合わせID: " + lpId + "\n";
  message += "TEL: " + tel + "\n";
  message += "選択した内容: " + selected + "\n";
  message += "問い合わせ時間: " + timestamp + "\n";
  message += "------------------------------------\n";
  message += "その他タグ:\n";

  if (data.params && Object.keys(data.params).length > 0) {
    for (var key in data.params) {
      if (key !== "lp_id") { // lp_idは既に出力済みのため除外
        message += key + ": " + data.params[key] + "\n";
      }
    }
  } else {
    message += "(パラメータなし)\n";
  }

  return message;
}

/**
 * Gmailに通知を送信する
 * @param {string} messageText - 送信するメッセージ
 */
function sendGmail(messageText) {
  var email = "ametome.official@gmail.com";
  var subject = "【アメトメ】新規お問い合わせがありました";
  try {
    GmailApp.sendEmail(email, subject, messageText);
  } catch (e) {
    console.log("Gmail送信エラー: " + e.toString());
  }
}

/**
 * LINEに通知を送信する
 * @param {string} messageText - 送信するメッセージ
 */
function sendLine(messageText) {
  var channelAccessToken = "ZWODUF58G3ocE8g3NQ2hnyiI4iUkaunGosz+9V+DRK3Our5nbyQsihFLb73gZHLlxLrlkaCY3X2scFcAOFFD4rD8kr3BwDl4gB6AYSmQ500OyGCYfWD/PDAYT+x1agIYn+7IoxogdRU05mBFC6cKYAdB04t89/1O/w1cDnyilFU=";
  var userId = "Ued8b57cfa67ac9c5726e6051538d6d74";
  var url = "https://api.line.me/v2/bot/message/push";

  var headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + channelAccessToken
  };

  var payload = {
    "to": userId,
    "messages": [
      {
        "type": "text",
        "text": messageText
      }
    ]
  };

  var options = {
    "method": "post",
    "headers": headers,
    "payload": JSON.stringify(payload)
  };

  try {
    UrlFetchApp.fetch(url, options);
  } catch (e) {
    console.log("LINE送信エラー: " + e.toString());
  }
}
