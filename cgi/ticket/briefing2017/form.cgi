#!/usr/bin/perl
require "jcode.pl";
require "cfg.cgi";
##チケット予約フォーム フォームCGI　2002/03/03
## -------------------------------------------------------------------
## このスクリプトはみのノートを元にseoが改造しました。
## このスクリプトを使用したいかなる損害も作者はその責を負いません。
## このスクリプトの改造前データはhttp://www.mino.net/cgi/
## -------------------------------------------------------------------
## メイン処理スタート
## -------------------------------------------------------------------
## 引数解析
&Com'getagv;
if ( $Com'FORM{'SORTFLG'} ne '' ) { $SORTFLG = $Com'FORM{'SORTFLG'}; }
if ( $Com'FORM{'SKEY'} ne '' ) { $SKEY = $Com'FORM{'SKEY'}; }
if ( $Com'FORM{'BACK'} ne '' ) { $BACK = $Com'FORM{'BACK'}; }
$MSG  = '';
@LIST = ();
## HTMLヘッダー表示
&HtmlStart;
## 内容表示
&DispView;
## HTMLフッター表示
&HtmlEnd;
exit(0);

## -------------------------------------------------------------------
## 内容表示サブルーチン
## -------------------------------------------------------------------
sub DispView {
	$KEY = &Com'lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "大変混み合っています。しばらく待ってから再度お試しください。";
		return;
	}
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$year=$year+1900;$mon ++;
	if ( &Com'GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG ) != 0 ) {
		&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);
		return;
	}
	&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);

	$cnt = -1;
	foreach $line ( @LIST ) {
		$cnt++;
		( $file,$seki,$mai ) = split( /,/,$line );
		if ( length( $file ) >= 12 ) {
			$yy = substr( $file,0,4 );
			$mm = substr( $file,4,2 );
			$dd = substr( $file,6,2 );
			$hh = substr( $file,8,2 );
			$ff = substr( $file,10,2 );
			$date = "$yy年$mm月$dd日\t$hh時$ff分開始\t$seki";
		} else { $date = "不明"; }

if ( $year >= $yy && $mon > $mm ) {
print "<font color=red><b>×</b></font><b>$date</b>\t\t<font color=red>受付終了</font>\n";
}elsif( $year >= $yy && $mon >= $mm && $mday > $dd ) {
print "<font color=red><b>×</b></font><b>$date</b>\t\t<font color=red>受付終了</font>\n";
}elsif( $year >= $yy && $mon >= $mm && $mday >= $dd && $hour >= $hh-$end ) {
print "<font color=red><b>×</b></font><b>$date</b>\t\t<font color=red>受付終了</font>\n";
}else{
if ( $mai <= 0 ) {
	print "<font color=red><b>×</b></font>\n";
		}else{
	print "<input type=radio name=day value=$yy$mm$dd$hh$ff checked>\n";
	print "<input type=hidden name=\"$yy$mm$dd$hh$ff\" value=\"$mai\">\n";
		}
			print "<b>$date</b>\n";

if ( $mai <= $zan && $mai >= 1 ) {
	print "\t\t<font color=red>残り$mai人</font>\n";
		}
if ( $mai <= 0 ) {
	print "\t\t<font color=red>満員</font>\n";
		}
}
			print "<br>\n";

	}
}

## -------------------------------------------------------------------
## HTMLヘッダー表示サブルーチン
## -------------------------------------------------------------------
sub HtmlStart {
	print "Content-type: text/html\n\n";
	print "<html><head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "<meta name=viewport content=\"width=320px\">\n";
	print "<title>$TITLE</title></head>\n";
	if ( -f $BGGIF ) { print "<body background=\"$BGGIF\" TEXT=\"$FGCOLOR\" LINK=\"$LINK\" VLINK=\"$VLINK\" ALINK=\"$ALINK\">\n"; }
	else { print "<body bgcolor=\"$BGCOLOR\" TEXT=\"$FGCOLOR\" LINK=\"$LINK\" VLINK=\"$VLINK\" ALINK=\"$ALINK\">\n"; }
	print "<H2>$TITLE</H2>\n";
	if ( $HEADMSG ne '' ) {
		print "$HEADMSG<hr>\n";
	}
	print "<form method=POST action=$MAILCGI>\n";
}
## -------------------------------------------------------------------
## HTMLフッター表示サブルーチン
## -------------------------------------------------------------------
sub HtmlEnd {
	if ( $MSG ne '' ) {
		print "</form><br><br><font color=\"#FF0000\" size=+1><b>$MSG</b></font><br><br>\n";
	}else{
	print "<div style='display:none'><br>枚数\n";
	print "<input type=radio name=\"mai\" value=\"1\" checked>1\n";
	print "<input type=radio name=\"mai\" value=\"2\">2\n";
	print "<input type=radio name=\"mai\" value=\"3\">3\n";
	print "<input type=radio name=\"mai\" value=\"4\">4\n";
	print "<input type=radio name=\"mai\" value=\"5\">5\n";
	print "<input type=radio name=\"mai\" value=\"6\">6\n";
	print "<br></div>\n";
	
	print "<p>参加者氏名（カタカナ･フルネーム）<br><input type=text size=30 name=\"name\"></p>\n";
	print "<p>年齢 <input type=text size=3 name=\"age\">歳</p>\n";
	print "<p>性別 <label><input type=radio name=\"gender\" value=\"男性\">男性</label>　<label><input type=radio name=\"gender\" value=\"女性\">女性</label></p>\n";
	print "<p>E-Mail <input type=text size=30 name=\"email\"></p>\n";
	print "<p>TEL <input type=text size=13 name=\"tel\"></p>\n";
	print "<p>備考 <input type=text size=30 name=\"biko\"></p>\n";
	print "［送信］ボタンを１回のみ押してください。<br>\n";
	print "<input type=submit value=\"送信\">　\n";
	print "<input type=reset value=\"リセット\">\n";
	print "<br><br>送信できない場合、<a href=\"mailto:yoyaku\@gekidan-curryrice.com\">メール</a>にてご連絡ください。<br>\n";
	print "</form><br><br>\n";
	}
print "<br>\n";

	print "<p align=right>\n";
	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	if ( $MGRFLG eq 'ON' ) {
		print "<input type=\"submit\" name=\"ACT\" value=\"管理\">\n";
		print "<br>\n";
print "<br>\n";
print "<br>\n";

		
	}
	print "</form>\n";

	print "</body></html>\n";
	exit(0);
}

