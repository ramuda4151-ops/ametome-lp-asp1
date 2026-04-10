/**
 * LPからのフォーム送信を受け取り、写真をGoogle Driveに保存し
 * GmailとLINEグループに通知する
 *
 * 【Google Driveフォルダ設定】
 * DRIVE_FOLDER_ID に写真保存先フォルダのIDを設定してください。
 * フォルダIDはDriveのURLから取得: https://drive.google.com/drive/folders/{フォルダID}
 */
var DRIVE_FOLDER_ID = 'YOUR_FOLDER_ID_HERE'; // ← ここに保存先フォルダIDを設定

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // 1. 写真をGoogle Driveに保存してURLリストを取得
    var photoUrls = [];
    if (data.photos && data.photos.length > 0) {
      photoUrls = savePhotosToDrive(data.photos, data);
    }

    // 2. メッセージ本文を作成
    var messageText = createMessage(data, photoUrls);

    // 3. Gmailへの通知送信
    sendGmail(messageText, data);

    // 4. LINE Messaging APIへの通知送信
    sendLine(messageText);

    return ContentService.createTextOutput(JSON.stringify({ status: 'success' })).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    console.log('エラー発生: ' + error.toString());
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: error.toString() })).setMimeType(ContentService.MimeType.JSON);
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
      folder = DriveApp.getFolderById(DRIVE_FOLDER_ID);
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
 * 通知メッセージを作成する（LINE・Gmail共通テキスト部分）
 * ※LINEは開かないと2行しか表示されないため、重要情報を先頭に配置
 */
function createMessage(data, photoUrls) {
  var formType = data.form_type || 'call';
  var lpId = data.lp_id || '(IDなし)';
  var tel = data.tel || '(電話番号なし)';
  var timestamp = data.timestamp || new Date().toLocaleString('ja-JP', {timeZone: 'Asia/Tokyo'});

  var message = '';

  if (formType === 'inquiry') {
    // 詳細フォーム（問い合わせフォーム）
    message += '【アメトメ】詳細フォームCV\n';
    message += 'TEL: ' + tel + '\n';
    message += 'お名前: ' + (data.name || '') + '\n';
    message += '郵便番号: ' + (data.zip || '') + '\n';
    message += '住所: ' + (data.address || '') + '\n';
    if (data.status) message += '雨漏り状況: ' + data.status + '\n';
    if (data.time) message += '希望連絡時間: ' + data.time + '\n';
  } else {
    // 簡易フォーム（電話番号フォーム）
    var selected = data.selected || '(選択なし)';
    var note = data.note || '';
    message += '【アメトメ】リスCV\n';
    message += 'TEL: ' + tel + '\n';
    message += '選択した内容: ' + selected + '\n';
    if (note) message += 'その他メモ: ' + note + '\n';
  }

  message += '問い合わせ時間: ' + timestamp + '\n';
  message += '問い合わせID: ' + lpId + '\n';

  // 写真情報
  if (photoUrls && photoUrls.length > 0) {
    message += '\n📷 写真の添付があります（' + photoUrls.length + '枚）\n';
    for (var i = 0; i < photoUrls.length; i++) {
      message += '写真' + (i + 1) + ': ' + photoUrls[i].url + '\n';
    }
  }

  // その他パラメータ
  message += '\nその他タグ:\n';
  if (data.params && Object.keys(data.params).length > 0) {
    for (var key in data.params) {
      if (key !== 'lp_id') {
        message += key + ': ' + data.params[key] + '\n';
      }
    }
  } else {
    message += '(パラメータなし)\n';
  }

  return message;
}

/**
 * Gmailに通知を送信する
 */
function sendGmail(messageText, data) {
  var email = 'ametome.official@gmail.com';
  var formType = data ? (data.form_type || 'call') : 'call';
  var subject = formType === 'inquiry'
    ? '【アメトメ】詳細フォームからお問い合わせがありました'
    : '【アメトメ】新規お問い合わせがありました';
  try {
    GmailApp.sendEmail(email, subject, messageText);
  } catch (e) {
    console.log('Gmail送信エラー: ' + e.toString());
  }
}

/**
 * LINEグループに通知を送信する
 */
function sendLine(messageText) {
  var channelAccessToken = 'ZWODUF58G3ocE8g3NQ2hnyiI4iUkaunGosz+9V+DRK3Our5nbyQsihFLb73gZHLlxLrlkaCY3X2scFcAOFFD4rD8kr3BwDl4gB6AYSmQ500OyGCYfWD/PDAYT+x1agIYn+7IoxogdRU05mBFC6cKYAdB04t89/1O/w1cDnyilFU=';
  var groupId = 'Cce12474663e3936457a0270c4d82926e';
  var url = 'https://api.line.me/v2/bot/message/push';
  var headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + channelAccessToken
  };
  var payload = {
    'to': groupId,
    'messages': [
      {
        'type': 'text',
        'text': messageText
      }
    ]
  };
  var options = {
    'method': 'post',
    'headers': headers,
    'payload': JSON.stringify(payload)
  };
  try {
    UrlFetchApp.fetch(url, options);
  } catch (e) {
    console.log('LINE送信エラー: ' + e.toString());
  }
}
