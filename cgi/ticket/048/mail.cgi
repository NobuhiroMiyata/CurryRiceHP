#!/usr/bin/perl
require "jcode.pl";
require "cfg.cgi";
########
##	メールスクリプト
########
# 各種設定

##
## フォームデータの取り込み
##
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

@wday_array = ('日','月','火','水','木','金','土');
$date_now = sprintf("%02d\/%01d\/%01d(%s)%02d\:%02d",$year +1900,$mon +1,$mday,$wday_array[$wday],$hour,$min,$sec);

#グローバル変数定義
#座席残数
$g_zanseki;
#予約数
$g_yoyakusu;

print "Content-type: text/html\n\n";

if ( $ENV{'REQUEST_METHOD'} eq 'POST' ) {
	read(STDIN, $input, $ENV{'CONTENT_LENGTH'});
} else {
	$input = $ENV{'QUERY_STRING'};
}

if ( $input ne '' ) {
	foreach $temp ( split(/&/, $input) ) {
		( $label, $value ) = split( /=/, $temp );
		$value =~ tr/+/ /;
		$value =~  s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		$value =~  s/\r\n/\r/g;
		$value =~  s/\n/\r/g;
		$value =~ tr/\t//d;
		&jcode::convert(*value, 'sjis');
		$FORM{$label} = $value;
	}
}
		$DATE = substr( $FORM{'day'},0,12 );

## エラーチェック
if ( $FORM{'day'} eq '' ) {
	push ( @error, '日時を選択してください。');
}
if ( $FORM{'mai'} eq '' ) {
	push ( @error, '枚数を入力してください。');
}
#$tmp1 = "$DATE" . "_zanseki";
if ( $FORM{$DATE} < $FORM{'mai'}) {
	push ( @error, '枚数が残数を超えています。');
}
if ( $FORM{'name'} eq '' ) {
	push ( @error, '氏名を入力してください。');
}
if ( $FORM{'email'} eq '' ) {
	push ( @error, '連絡用メールアドレスを入力してください。');
}
if ( $FORM{'email'} !~ /^[\!-~]+\@[\!-~]+\.[\!-~]+$/ && $FORM{'email'} ne '' ) {
	push ( @error, '連絡用メールアドレスが正しくありません。');
}
if ( $FORM{'email'} =~ m/[<>]/ ) {
	push ( @error, '連絡用メールアドレスが正しくありません。');
}
if ( $FORM{'tel'} eq '' ) {
	push ( @error, '連絡用電話番号を入力してください。');
}

## エラーがなかったとき
if ( ! @error ) {

		if ( length( $DATE ) >= 12 ) {
			$y2 = substr( $DATE,0,4 );
			$m2 = substr( $DATE,4,2 );
			$d2 = substr( $DATE,6,2 );
			$h2 = substr( $DATE,8,2 );
			$f2 = substr( $DATE,10,2 );
			$date = "$y2年$m2月$d2日$h2時$f2分開演";
		}

	# チケットデータ修正
	&ticket;


sub regist{

	$DATE = substr( $FORM{'day'},0,12 );

	# CSVデータ作成
	$csvdata = '"' .
		   $date_now			. '","' .
		   $date					. '","' .
		   $FORM{'mai'}		. '","' .
		   $FORM{'name'}	. '","' .
		   $FORM{'email'}	. '","' .
		   $FORM{'tel'}		. '","' .
#		   $FORM{'biko'}		. '"' .
		   $FORM{'biko'}	. '","' .
			 "$g_yoyakusu"	. '","' .
			 "0"						.	'"' .
		   "\n";


	&jcode::convert(*csvdata, 'sjis');

			if ( $csvmode eq '1' ) {
  	$tuika_csv="$csvd$FORM{'day'}.csv";
		} else {
  	$tuika_csv="$csvf";
		}
		if (!open(DB,">> $tuika_csv"))
			{
				open(DB,">$tuika_csv");
				flock DB, 2;
				print DB  $csvdata;
				flock DB, 8;
	  		close(DB);
	  	}
		else{
				flock DB, 2;
				print DB  $csvdata;
				flock DB, 8;
	  		close(DB);
  	}


	chmod 0666,$tuika_csv;


	## メール送信

	# メールデータ作成
	$maildata =<<END;
Subject:Ticket Order
From:$FORM{'email'}

下記の通り、チケット注文がありました。
送信時刻	: $date_now
希望日時	: $date
枚数	: $FORM{'mai'} 枚
お名前	: $FORM{'name'}
E-MAIL	: $FORM{'email'}
電話番号	: $FORM{'tel'}
備考	: $FORM{'biko'}

END

	# サンクスメールデータ
	$maildata1 =<<END;
Subject:Thanks for your order!
From:$admin_email

こんにちは。
劇団カレーライスです。
チケット予\約を下記のとおり承りました。
送信時刻	: $date_now
希望日時	: $date
枚数		: $FORM{'mai'} 枚
お名前	: $FORM{'name'}
E-MAIL	: $FORM{'email'}
電話番号	: $FORM{'tel'}

変更等は$admin_emailへご一報ください。

それでは、劇場で会いましょう！
※このメールに身に覚えのない方はそのままご返信ください。

END

	&jcode::convert(*maildata, 'sjis');
	&jcode::convert(*maildata1, 'sjis');

	# 管理者にメール
         if (!open(OUT,"| $sendmail $admin_email")) { last; }
         print OUT $maildata;
         close(OUT);

	# 送信先にメール
         if (!open(OUT,"| $sendmail $send_email")) { last; }
         print OUT $maildata;
         close(OUT);

	# 申込者にメール
         if (!open(OUT,"| $sendmail $FORM{'email'}")) { last; }
         print OUT $maildata1;
         close(OUT);


	##
	## HTML用メッセージ
	##
	$html_message =
"こんにちは！
ご予\約ありがとうございました。下記のとおり承りました。<br><br>
送信時刻	: $date_now<br>
希望日時	: $date <br>
枚数		: $FORM{'mai'} 枚<br>
お名前	: $FORM{'name'} <br>
E-MAIL	: $FORM{'email'}<br>
電話番号	: $FORM{'tel'}<br>
<br>
それでは、劇場でお待ちしております！<br>
<br>
<p>[<a href='#' onClick='window.close(); return false;'>閉じる</a>]</p>
";
&HTML;

}

## エラーがあったとき
} else {
	$html_message =  "<p><font color=red><b>お受け出来ません。<br>下記の内容をご確認ください。</b></font></p><UL>\n";
	foreach ( @error ) {
		$html_message .= "\t<LI>$_</LI>\n";
	}
	$html_message .= "</UL>\n[<a href='' onClick='history.go(-1); return false;'>戻る</a>]";
	&HTML;
}
	#チケット枚数処理
sub ticket{
		#ロック処理(オン)
		$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
		if ( $KEY != 9 ) {
			$html_message = "大変混み合っています。しばらく待ってから再度お試しください。";
			&HTML;
		}
		&Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
		#フラグの初期化
		$flg = 'NG';

		#更新対象レコードの検索
		foreach $line ( @LIST ) {
			#day.datから更新対象のレコードを探索する。CSVを分解(公演日、金額、残座席数、キャパ、現在予約数)
			( $ymdhm, $yen, $zanseki, $M_seki, $yoyakusu) = split( /,/,$line );
			#更新対象レコードが見つかったら、残座席数を減算、現在予約数を加算する。
			if ( $ymdhm eq $DATE ) {
				$flg = 'OK';
				#残席数の計算
				$g_zanseki = $zanseki - $FORM{'mai'};
				#予約数をインクリメント
				$g_yoyakusu = ++$yoyakusu;
				next;
			}
			#更新対象外のレコードを配列に書き出す
			push( @OUTLIST,$line );
		}

		#NGの場合(更新対象レコードが存在しない場合)処理終了
		if ( $flg eq 'NG' ) {
				$html_message = "対象が見つかりません。";
				&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HTML;
		}

		#＠OUTLISTに更新対象レコードが含まれているか検索
		foreach $line ( @OUTLIST ) {
			#( $file,$seki,$mai ) = split( /,/,$line );
			( $ymdhm, $yen, $zanseki, $M_seki, $yoyakusu) = split( /,/,$line );
			if ( $ymdhm eq $DATE ) { last; }
		}
		#＠OUTLISTに更新対象レコードが含まれている場合処理終了
		if ( $ymdhm eq $DATE ) {
			$MSG = "対象が既にあります。";
			&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
			&HTML;
		}

		#更新済みデータを＠OUTLIST配列に追加する
		$line = "$DATE,$yen,$g_zanseki,$M_seki,$g_yoyakusu";
		push( @OUTLIST,$line );

		#day.datへの書き込み処理
		if ( open( OUT,">$FILEDIR/$LSTFILE" ) ) {
			@OUTLIST = sort( @OUTLIST );
			foreach $line ( @OUTLIST ) { print OUT "$line\n"; }
			close( OUT );
		} else {
			$html_message = "リストファイルに保存することが出来ません。";
			&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
			&HTML;
		}
		&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
		&regist;
}

## HTML表示
sub HTML {
printf <<END;

<html>
<head>
<title>チケット入力フォーム</title>
<meta http-equiv="Content-Type" content="text/html; charset=sjis">
</head>
<body bgcolor="#FFFFFF">
  <p>$html_message</p>
</body>
</html>
END
}
