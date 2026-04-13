$(window).on('load', function() {
    if ($('.ct3_telno').length > 0) {
        /*#################################################################
         paramater settings : 動的発番の変数を設定する。

          def_telno     : 発番失敗時に表示するデフォルトの電話番号を指定する。
          baseurl       : 動的発番用のURLを指定する。(原則固定)
          partner_id    : 事業者IDを指定する。(原則固定)
          client_id     : 広告主IDを指定する。
          demand_key    : 番号在庫からトラッキング番号を発行するためのシード。(原則固定)
          dialinID      : 発番の単位となる一意なID(セッションID等)
          exp_at        : 番号を保持する期限をISO8061形式で指定する。
                       有効期限を経過したタイミングで、自動的に番号が削除される。
                        (例2016-12-27T15:00:00+00:00)
          phone         : 転送先の電話番号 (省略時は広告主の設定を引き継ぐ)
          fw_enable     : 転送可否 true：転送する／false:転送しない (省略時は広告主の設定を引き継ぐ)
          vars          : 通話ログに表示したい任意の変数と値をオブジェクトの形で指定してください。

        ###################################################################*/
        //RT ctパラメータ取得
        var __rt_match = RegExp('[?&]' + 'ct' + '=([^&]*)').exec(window.location.search);
		var __rt_ct = __rt_match && decodeURIComponent(__rt_match[1].replace(/\+/g, ' '));
        if(__rt_ct){__rt_ct = __rt_ct.replace('.', '_');}

        var def_telno = "0120094956";
        var baseurl = "https://dyn.calltracker.jp/ct/3.0a/dialins/demand_upsert/";
        var partner_id = "5b4ea9f99dfb1efd72a67ac1";

        var client_id = "6973212d3995bb710483ca98";

        var demand_key = "demand0078";
        var exp_at = moment.utc().add(24, "h").format(); // ## 番号有効期限を現在時刻。24時間を標準とします。
        var dialinID = __rt_ct + '_' + client_id;
        var phone = "";
        var fw_enable = true;
        var vars = {
            "attr01": __rt_ct,
        };
        ///// paramater settings ここまで /////



        $.ajax({
            timeout: 4000,
            async: true,
            crossDomain: true,
            url: baseurl + partner_id + "/" + client_id ,
            data: {
                "demand_key": demand_key,
                "_exp_at": exp_at,
                "dialinID": dialinID,
                "dp.forward_enable": fw_enable,
                "dp.vars": JSON.stringify(vars)
            },
            beforeSend: function(XMLHttpRequest) {
            },
            success: function(data, text_status, xhr) {
                if (xhr.status != "200") {
                    // 発番失敗時のデフォルト番号表示(ステータスコードが200以外)
                    $(".ct3_telno").each(function() {
                        $(this).html(def_telno);
                    });
                    $(".telno").each(function() {
                        $(this).attr('href', 'tel:' + def_telno);
                    });
                } else {
                    // 発番された番号の表示
                    $(".ct3_telno").each(function() {
                        //$(this).html(data.result.ct_phone);
                        phone = data.result.ct_phone;
                        $(this).html(phone.substr(0,4) + '-' + phone.substr(4,5)+ '-' + phone.substr(9,5));
                    });
                    $(".telno").each(function() {
                        $(this).attr('href', 'tel:' + data.result.ct_phone);
                    });
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                // 発番失敗時のデフォルト番号表示(リクエストのエラー時)
                $(".ct3_telno").each(function() {
                    $(this).html(def_telno);
                });
                $(".telno").each(function() {
                    $(this).attr('href', 'tel:' + def_telno);
                });
            },
            complete: function(XMLHttpRequest, textStatus) {}
        });
    } else {}
});
