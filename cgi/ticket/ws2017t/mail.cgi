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
		&jcode'convert(*value, 'sjis');
		$FORM{$label} = $value;
	}
}
		$DATE = substr( $FORM{'day'},0,12 );
		
		$seki2= substr($FORM{'day'},11,1 );
		$seki2='￥500';

## エラーチェック
if ( $FORM{'day'} eq '' ) {
	push ( @error, '日時を選択してください。');
}
if ( $FORM{'mai'} eq '' ) {
	push ( @error, '人数を入力してください。');
}
if ( $FORM{$DATE} < $FORM{'mai'}) {
	push ( @error, '人数が残数を超えています。');
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

	# CSVデータ作成
	$csvdata = '"' .
		   $date_now		. '","' .
		   $date	. '","' .
		   $FORM{'mai'}	. '","' .
		   $FORM{'name'}	. '","' .
		   $FORM{'age'}		. '","' .
		   $FORM{'email'}	. '","' .
		   $FORM{'tel'}		. '","' .
		   $FORM{'biko'}	. '"' .

		   "\n";


	&jcode'convert(*csvdata, 'sjis');

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
Subject:WorkShop Order
From:$FORM{'email'}

下記の通り、ワークショップへの予\約がありました。

送信時刻	: $date_now
お名前	: $FORM{'name'} 
年齢	: $FORM{'age'}歳
E-MAIL	: $FORM{'email'}
電話番号	: $FORM{'tel'}
備考	: $FORM{'biko'}

END

	# サンクスメールデータ
	$maildata1 =<<END;
Subject:Thanks! from Gekidan-CurryRice
From:$admin_email

こんにちは。
劇団カレーライスです。
下記のとおりご予\約を承りました。

●演劇ワークショップ「劇団カレーライス レシピ ～ひとつのお芝居ができるまで～」ご出席

お名前	: $FORM{'name'} 
年齢	: $FORM{'age'}歳
E-MAIL	: $FORM{'email'}
電話番号	: $FORM{'tel'}

●日時
2017年1/29(日) 11:50～16:00

●会場
平塚市中央公民館 ４階･小ホール
【徒歩】ＪＲ東海道線平塚駅北・西口より徒歩15分 
【バス】ＪＲ東海道線平塚駅北口バス乗り場 4番線　平63・平65・平68・平86・平97・平62に乗車（注：平67は通りません）江陽中学校前下車 徒歩1分
google Mapはこちら→ https://goo.gl/maps/bEtBDz3hvz82

●参加費：500円
●ご持参いただくもの：動きやすい服装、室内履き、筆記用具

お問い合わせ・変更等は、$admin_emailへご一報ください。
それでは、ご来場をお待ちしております！

※このメールに身に覚えのない方はそのままご返信ください。

END

	&jcode'convert(*maildata, 'sjis');
	&jcode'convert(*maildata1, 'sjis');

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
"<h2>送信完了</h2><br>
ご予\約ありがとうございました。<br>
下記のとおり承りました。<br><br>
<hr>
お名前	: $FORM{'name'} <br>
年齢	: $FORM{'age'}歳<br>
E-MAIL	: $FORM{'email'}<br>
電話番号	: $FORM{'tel'}<br>
<hr><br>
2017年1月29日(日) 平塚市中央公民館４階・小ホールにお越しください。<br><br>
※参加費（500円）、動きやすい服装、室内履き、筆記用具をお持ちください。<br>
<br>
それでは、ご来場をお待ちしております！
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
		$KEY = &Com'lockon("$FILEDIR/$LOCKFILE");
		if ( $KEY != 9 ) {
			$html_message = "大変混み合っています。しばらく待ってから再度お試しください。";
			&HTML;
		}
		&Com'GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
		$flg = 'NG';
		foreach $line ( @LIST ) {
			( $file,$seki,$mai ) = split( /,/,$line );
			if ( $file eq $DATE ) { $flg = 'OK'; next; }
			push( @OUTLIST,$line );
		}
			if ( $flg eq 'NG' ) { 
			$html_message = "対象が見つかりません。";
				&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HTML;
			}
			foreach $line ( @OUTLIST ) {
				( $file,$seki,$mai ) = split( /,/,$line );
				if ( $file eq $DATE ) { last;}
			}
			if ( $file eq $DATE ) {
				$MSG = "対象が既にあります。";
				&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HTML;
			}
			$MAI = $FORM{$DATE}-$FORM{'mai'};
			$line = "$DATE,$seki2,$MAI";
			push( @OUTLIST,$line );

		if ( open( OUT,">$FILEDIR/$LSTFILE" ) ) {
			@OUTLIST = sort( @OUTLIST );
			foreach $line ( @OUTLIST ) { print OUT "$line\n"; }
			close( OUT ); 
		} else {
			$html_message = "リストファイルに保存することが出来ません。";
			&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);
			&HTML;
		}
		&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);
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
