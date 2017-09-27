##チケット予約フォーム 設定ファイル　2002/03/03
## -------------------------------------------------------------------
## このスクリプトはみのノートを元にseoが改造しました。
$MKNAME  = 'みのノート';        # v1.0 1999/10/12
$MKURL   = 'http://www.mino.net/cgi/';
## このスクリプトを使用したいかなる損害も作者はその責を負いません。
## -------------------------------------------------------------------
## -------------------------------------------------------------------
## --- 基本設定 任意に修正 [*]項目は任意 省略する場合''
## -------------------------------------------------------------------

$MGRPASS = 'curry1012';		# 管理パスワード※必ず変更

# 各ファイル名の設定
$MENUCGI = './form.cgi';	# メールフォームＣＧＩ
$MAILCGI = './mail.cgi';	# メール送信ＣＧＩ
$MGRCGI  = './mgr.cgi';		# 管理&ヘルプ画面ＣＧＩ
$FILEDIR = './';		# 各種ファイル格納ディレクトリ
$LSTFILE = 'day.dat';		# 日時データ一覧ファイル※自動生成
$LOCKFILE= 'day.loc';		# ロックファイル※自動生成

# メール設定
$sendmail = '/usr/sbin/sendmail'; #sendmailのパス プロバイダに確認すること
$admin_email = 'info@gekidan-curryrice.com';	# 管理者メールアドレス
					# お客様に通知されます。
$send_email = 'uchuzine@gmail.com';	# 上以外の送付先メールアドレス、客への通知なし
					# 複数設定するときはカンマ(,)でくぎる

# 予約データ格納ファイル設定
$csvmode = '1';		# 0->全データを1ファイルに。1->公演ごとにファイル生成
			# ※read.cgiを使う場合は、1にすること。
$csvf = 'yoyaku.csv';	# 0の場合必要。申込ログファイル※自動生成、必ず名前変更
$csvd = './log/';	# 1の場合必要。申込ログ格納場所のパス
			# ※パーミッション707にて作成、必ず名前変更

# 画面の設定
$TITLE   = '予約申込みフォーム';# ページタイトル

$BGGIF   = '';	# 背景画像[*]
$BGCOLOR = '#FFFFFF';	# 背景色[*]
$FGCOLOR = '#333333';	# 文字色
$LINK    = '#0000FF';	# LINK色
$VLINK   = '#FF0000';	# VLINK色
$ALINK   = '#00FF00';	# ALINK色
$BASURL  = 'http://gekidan-curryrice.com/';	# あなたのHPのアドレス
$HEADMSG = 		# ページヘッダーメッセージ[*]
'次回公演のお申込みはこちらから';

$zan= '100';		# チケットがこの枚数以下になったら残数表示
			# 表示したくない場合は0

$end= '6';		# 開演$end時間前になったら受付終了
			# ただし分切り捨て。13時30分開演の場合は、2を入力すると11時00分終了。
			# 公演前日に終了が最大設定（公演時間以上の数字入力）

$MGRFLG  = 'ON';	# 管理フラグ（管理ボタン有／無）
	
## メニューの設定
$SORTFLG = 1;		# 表示順序
			#   0:日付の新しいものから
			#   1:日付の古いものから
			#   2:チケット残数の少ないものから

## --- 基本設定 ここまで
$BCKURL  = "$MENUCGI";	# メニュー画面以外からのバックＵＲＬ

## -------------------------------------------------------------------
## パッケージ・ライブラリ宣言
## -------------------------------------------------------------------
package Com;
## -------------------------------------------------------------------
## 引数解析
## -------------------------------------------------------------------
sub getagv {
	if ($ENV{'REQUEST_METHOD'} eq 'POST') {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else {
		$buffer = $ENV{'QUERY_STRING'};
	}
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/\r//g;
		$value =~ s/<!--(.|\n)*-->//g;	#SSI 	除去(セキュリティ対策)
		$value =~ s/applet//gi;		#Java		除去(セキュリティ対策)
		$value =~ s/<script//gi;		#Javascript	除去(セキュリティ対策)
		$value =~ s/<META(.+)Refresh(.*)>(\s*)(\n?)//ig; #METAタグ飛ばし禁止
		$value =~ s/<(.*)style(\s*)=(.|\n)*>//ig;        #Styleタグ禁止
		&jcode'convert(*value, 'sjis');
		$FORM{$name} = $value;
	}
}
## -------------------------------------------------------------------
## リスト取得処理サブルーチン
## -------------------------------------------------------------------
sub GetList {
	local($lfile,$flg,*list,*msg) = @_;
	@list = ();
	if ( open( FP,$lfile ) ) {
		while ( <FP> ) {
			chop $_;
			$line = $_;
			&jcode'convert(*line, 'sjis');
			if ( $flg == 2 ) {
				( $file,$title,$name ) = split( /,/,$line );
				$line = "$title,$file,$name";
			}
			push( @list,$line );
		}
		close( FP );
	}
	if ( $#list < 0 ) {
		$msg = '現在お申込みを受け付けておりません。';
		return 1;
	}
	@list = sort( @list );
	if ( $flg == 0 ) { @list = reverse( @list ); }
	if ( $flg == 2 ) {
		@list2 = ();
		foreach $line ( @list ) {
			( $title,$file,$name ) = split( /,/,$line );
			$line = "$file,$title,$name";
			push( @list2,$line );
		}
		@list = @list2;
	}
	return 0;
}
## -------------------------------------------------------------------
## 本文表示処理サブルーチン
## -------------------------------------------------------------------
sub GetData {
	local($lfile,*msg) = @_;
	$msg = '';
	if ( open( FP,$lfile ) ) {
		while ( <FP> ) {
			$msg = "$msg$_";
		}
		close( FP );
	}
	&jcode'convert(*msg, 'sjis');
}
## -------------------------------------------------------------------
## ロック処理サブルーチン
## -------------------------------------------------------------------
sub lockon {
	local($lfile) = @_;
	$lckkey = 0;
	foreach (1 .. 5) {
		unless (-e "$lfile") {
			open(LOCK,">$lfile");
			close(LOCK);
			$lckkey = 9;
			last;
		} else { sleep(1); }
	}
	if ($lckkey == 0) { return 0; }
	return 9;
}
## -------------------------------------------------------------------
## アンロック処理サブルーチン
## -------------------------------------------------------------------
sub lockoff {
	local($lfile,$key) = @_;
	if ($key == 9) { unlink("$lfile"); }
}
1;

