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
&Com::getagv;
if ( $Com::FORM{'SORTFLG'} ne '' ) { $SORTFLG = $Com::FORM{'SORTFLG'}; }
if ( $Com::FORM{'SKEY'} ne '' ) { $SKEY = $Com::FORM{'SKEY'}; }
if ( $Com::FORM{'BACK'} ne '' ) { $BACK = $Com::FORM{'BACK'}; }
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
	$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "大変混み合っています。しばらく待ってから再度お試しください。";
		return;
	}
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$year=$year+1900;$mon ++;
	if ( &Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG ) != 0 ) {
		&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
		return;
	}
	&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);

	$cnt = -1;
	foreach $line ( @LIST ) {
		$cnt++;
		#CSVから先の値を取得(公演日、金額、残渣席数、キャパ、現在予約数)
		( $ymdhm, $yen, $zanseki, $M_seki, $yoyakusu) = split( /,/,$line );
		if ( length( $ymdhm ) >= 12 ) {
			$yy = substr( $ymdhm,0,4 );
			$mm = substr( $ymdhm,4,2 );
			$dd = substr( $ymdhm,6,2 );
			$hh = substr( $ymdhm,8,2 );
			$ff = substr( $ymdhm,10,2 );
			$date = "$yy年$mm月$dd日\t$hh時$ff分開演\t$yen";
		} else { $date = "不明"; }

		if ( $year >= $yy && $mon > $mm ) {
			print "<font color=red><b>×</b></font><b>$date</b>\t\t<font color=red>受付終了</font>\n";
		}elsif( $year >= $yy && $mon >= $mm && $mday > $dd ) {
			print "<font color=red><b>×</b></font><b>$date</b>\t\t<font color=red>受付終了</font>\n";
		}elsif( $year >= $yy && $mon >= $mm && $mday >= $dd && $hour >= $hh-$end ) {
			print "<font color=red><b>×</b></font><b>$date</b>\t\t<font color=red>受付終了</font>\n";
		}else{
			if ( $zanseki <= 0 ) {
				print "<font color=red><b>×</b></font>\n";
			}else{
				print "<input type=radio name=\"day\" value=\"$yy$mm$dd$hh$ff\">\n";
				print "<input type=hidden name=\"$yy$mm$dd$hh$ff\" value=\"$zanseki\">\n";
			}
			print "<b>$date</b>\n";

			if ( $zanseki <= $zan && $zanseki >= 1 ) {
				print "\t\t<font color=red>残り$zanseki枚</font>\n";
			}
			if ( $zanseki <= 0 ) {
				print "\t\t<font color=red>販売終了</font>\n";
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
	print "<br>枚数\n";
	print "<input type=radio name=\"mai\" value=\"1\" checked>1\n";
	print "<input type=radio name=\"mai\" value=\"2\">2\n";
	print "<input type=radio name=\"mai\" value=\"3\">3\n";
	print "<input type=radio name=\"mai\" value=\"4\">4\n";
	print "<input type=radio name=\"mai\" value=\"5\">5\n";
	print "<input type=radio name=\"mai\" value=\"6\">6\n";
	print "<br><br>\n";

	print "名前（カタカナ･フルネーム）<input type=text size=30 name=\"name\"><br>\n";
	print "来場者E-Mail<input type=text size=30 name=\"email\"><br>\n";
	print "TEL<input type=text size=13 name=\"tel\"><br>\n";
	print "備考<input type=text size=30 name=\"biko\"><br><br>\n";
	print "［送信］ボタンを１回のみ押してください。<br>\n";
	print "<input type=submit value=\"送信\">\n";
	print "<input type=reset value=\"リセット\">\n";
	print "<br>送信できない場合、メールにてご連絡ください。<br>\n";
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
