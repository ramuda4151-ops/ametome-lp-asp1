/**
 * 【lp3（東北版）専用】LPからのフォーム送信を受け取り、写真をGoogle Driveに保存し
 * GmailとLINEグループに通知する
 *
 * ■ デプロイ手順
 * 1. script.google.com で新規プロジェクトを作成し、このコードを貼り付ける
 * 2. プロジェクト設定 > スクリプトプロパティ に以下を設定する（コードに直書きしない）
 *    - LINE_CHANNEL_ACCESS_TOKEN : LINE Messaging APIのチャネルアクセストークン
 *    - LINE_GROUP_ID             : 通知先LINEグループのID（東北用の新グループ）
 *    - DRIVE_FOLDER_ID           : 写真保存先DriveフォルダのID（省略時はマイドライブ直下）
 *    ※ LINEのプロパティが未設定の間はLINE通知をスキップし、Gmail通知のみ行う
 * 3. デプロイ > 新しいデプロイ > ウェブアプリ（全員がアクセス可能）で公開し、
 *    発行されたURLを lp3/index.html の gasUrl（2箇所）に設定して build.py を実行する
 */

var NOTIFY_PREFIX = '【アメトメ】"東北"専用';
var GMAIL_TO = 'ametome.official@gmail.com';

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // 写真をGoogle Driveに保存してURLリストを取得
    var photoUrls = [];
    if (data.photos && data.photos.length > 0) {
      photoUrls = savePhotosToDrive(data.photos, data);
    }

    var messageText = createMessage(data, photoUrls);
    sendGmail(messageText, data);
    sendLine(messageText);

    return ContentService.createTextOutput(JSON.stringify({ status: "success" })).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    console.log("エラー発生: " + error.toString());
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * 写真をGoogle Driveに保存し、共有URLの配列を返す
 */
function savePhotosToDrive(photos, data) {
  var urls = [];
  try {
    var folder;
    try {
      var folderId = PropertiesService.getScriptProperties().getProperty('DRIVE_FOLDER_ID');
      folder = DriveApp.getFolderById(folderId);
    } catch(e) {
      folder = DriveApp.getRootFolder();
    }

    // 問い合わせごとにサブフォルダを作成
    var timestamp = (data.timestamp || new Date().toLocaleString('ja-JP', {timeZone: 'Asia/Tokyo'})).replace(/[\/: ]/g, '-');
    var name = data.name || '匿名';
    var tel = data.tel || '不明';
    var subFolderName = timestamp + '_' + name + '_' + tel;
    var subFolder = folder.createFolder(subFolderName);

    for (var i = 0; i < photos.length; i++) {
      var photo = photos[i];
      var base64Data = photo.data.split(',')[1];
      var mimeType = photo.type || 'image/jpeg';
      var fileName = photo.name || ('photo_' + (i + 1) + '.jpg');

      var blob = Utilities.newBlob(Utilities.base64Decode(base64Data), mimeType, fileName);
      var file = subFolder.createFile(blob);

      // URLを知っている人のみ閲覧可能に設定
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

      var fileId = file.getId();
      var viewUrl = 'https://drive.google.com/file/d/' + fileId + '/view';
      urls.push({ name: fileName, url: viewUrl });
    }
  } catch(e) {
    console.log('Drive保存エラー: ' + e.toString());
  }
  return urls;
}

/**
 * 通知メッセージを作成する
 * ※LINEは開かないと2行しか表示されないため、重要情報を先頭に配置
 */
function createMessage(data, photoUrls) {
  var lpId = data.lp_id || "(IDなし)";
  var tel = data.tel || "(電話番号なし)";
  var selected = data.selected || "(選択なし)";
  var note = data.note || "";
  var timestamp = data.timestamp || new Date().toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });
  var formType = data.form_type || "call";

  // ASP判定（asp_keyフィールドまたはparams.aspから判別）
  var aspName = "";
  if (data.asp_key && data.asp_key !== 'default') {
    aspName = data.asp_key;
  } else if (data.params && data.params.asp) {
    aspName = data.params.asp;
  } else if (lpId.indexOf("a_") === 0 || lpId === "a") {
    aspName = "a";
  } else if (lpId.indexOf("b_") === 0 || lpId === "b") {
    aspName = "b";
  }

  var message = "";

  if (formType === "inquiry") {
    message += NOTIFY_PREFIX + " 詳細フォームCV\n";
    message += "お名前: " + (data.name || "") + "\n";
    message += "TEL: " + tel + "\n";
    message += "郵便番号: " + (data.zip || "") + "\n";
    message += "住所: " + (data.address || "") + "\n";
    if (data.status) message += "雨漏り状況: " + data.status + "\n";
    if (data.time) message += "希望連絡時間: " + data.time + "\n";
  } else {
    message += NOTIFY_PREFIX + " 10秒CV\n";
    message += "TEL: " + tel + "\n";
    message += "選択した内容: " + selected + "\n";
    if (note) message += "その他メモ: " + note + "\n";
  }

  message += "問い合わせ時間: " + timestamp + "\n";

  // ASP・ID表示
  if (aspName) {
    message += "asp: " + aspName + "\n";
  }
  message += "ID: " + lpId + "\n";

  // 写真情報
  if (photoUrls && photoUrls.length > 0) {
    message += "\n📷 写真の添付があります（" + photoUrls.length + "枚）\n";
    for (var i = 0; i < photoUrls.length; i++) {
      message += "写真" + (i + 1) + ": " + photoUrls[i].url + "\n";
    }
  }

  // その他タグ
  message += "\nその他タグ:\n";
  if (data.params && Object.keys(data.params).length > 0) {
    for (var key in data.params) {
      if (key !== "lp_id" && key !== "asp") {
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
 */
function sendGmail(messageText, data) {
  var formType = data ? (data.form_type || "call") : "call";
  var subject = formType === "inquiry"
    ? NOTIFY_PREFIX + " 詳細フォームからお問い合わせがありました"
    : NOTIFY_PREFIX + " 新規お問い合わせがありました";
  try {
    GmailApp.sendEmail(GMAIL_TO, subject, messageText);
  } catch (e) {
    console.log("Gmail送信エラー: " + e.toString());
  }
}

/**
 * LINEグループに通知を送信する
 * トークン・グループIDはスクリプトプロパティから取得。未設定の間はスキップする。
 */
function sendLine(messageText) {
  var props = PropertiesService.getScriptProperties();
  var channelAccessToken = props.getProperty('LINE_CHANNEL_ACCESS_TOKEN');
  var groupId = props.getProperty('LINE_GROUP_ID');

  if (!channelAccessToken || !groupId) {
    console.log("LINE通知は未設定のためスキップしました（LINE_CHANNEL_ACCESS_TOKEN / LINE_GROUP_ID をスクリプトプロパティに設定してください）");
    return;
  }

  var url = "https://api.line.me/v2/bot/message/push";
  var headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + channelAccessToken
  };
  var payload = {
    "to": groupId,
    "messages": [{ "type": "text", "text": messageText }]
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
