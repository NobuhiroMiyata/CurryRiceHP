#!/usr/bin/perl
require "jcode.pl";
require "cfg.cgi";
##チケット予約フォーム 管理CGI　2002/03/03
## -------------------------------------------------------------------
## このスクリプトはみのノートを元にseoが改造しました。
## このスクリプトを使用したいかなる損害も作者はその責を負いません。
## このスクリプトの改造前データはhttp://www.mino.net/cgi/
## -------------------------------------------------------------------
## メイン処理スタート
## -------------------------------------------------------------------
@monthday = (0,31,28,31,30,31,30,31,31,30,31,30,31);
## 引数解析
&Com::getagv;
if ( $Com::FORM{'ACT'} ne '' ) { $ACT = $Com::FORM{'ACT'}; }
if ( $Com::FORM{'MODE'} ne '' ) { $MODE = $Com::FORM{'MODE'}; }
if ( $Com::FORM{'PASS'} ne '' ) { $PASS = $Com::FORM{'PASS'}; }
if ( $Com::FORM{'FILE'} ne '' ) { $FILE = $Com::FORM{'FILE'}; }
if ( $Com::FORM{'DATE'} ne '' ) { $DATE = $Com::FORM{'DATE'}; }
if ( $Com::FORM{'SEKI'} ne '' ) { $SEKI = $Com::FORM{'SEKI'}; }
if ( $Com::FORM{'MAI'} ne '' ) { $MAI = $Com::FORM{'MAI'}; }
$MSG  = '';
@LIST = ();
## 処理分割
if ( $ACT eq '管理' )     {
	if ( $MGRPASS ne '' ) { &InputPass; }
	else { $ACT = '管理画面'; &DispView; }
}
elsif ( $PASS ne $MGRPASS ) {
	$SUBTITLE = 'ログイン';
	&HtmlStart;
	$MSG = '管理パスワードが違います。';
	&HtmlEnd;
}
elsif ( $ACT eq '管理画面' ) { &DispView; }
elsif ( $ACT eq '新規登録' ) { &InputNote; }
elsif ( $ACT eq '変更' )     { &InputNote; }
elsif ( $ACT eq '削除' )     { &ConfNote; }
elsif ( $ACT eq '実行' )     { &ConfNote; }
elsif ( $ACT eq 'ＯＫ' )     { &ExecNote; }
else                         { $MSG = '操作が変です。'; }
$SUBTITLE = 'エラー';
&HtmlStart;
&HtmlEnd;
exit(0);

## -------------------------------------------------------------------
## パスワード入力画面サブルーチン
## -------------------------------------------------------------------
sub InputPass {
	$SUBTITLE = 'ログイン';
	&HtmlStart;
	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	print "管理パスワード：\n";
	print "<input type=\"hidden\" name=\"ACT\" value=\"管理画面\">\n";
   	print "<input type=\"password\" name=\"PASS\" value=\"\">\n";
   	print "<input type=\"submit\" value=\"ＯＫ\">\n";
	print "</form>\n";
	&HtmlEnd;
}
## -------------------------------------------------------------------
## 一覧表示サブルーチン
## -------------------------------------------------------------------
sub DispView {
	$SUBTITLE = '管理画面';
	&HtmlStart;
	$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "大変混み合っています。しばらく待ってから再度お試しください。";
		&HtmlEnd;
	}
	if ( &Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG ) != 0 ) {
		&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
		&HtmlEnd;
	}
	&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
	$page = 0;
	foreach $line ( @LIST ) {
		$cnt++;
		( $file,$seki,$mai ) = split( /,/,$line );
		if ( length( $file ) >= 12 ) {
			$yy = substr( $file,0,4 );
			$mm = substr( $file,4,2 );
			$dd = substr( $file,6,2 );
			$hh = substr( $file,8,2 );
			$ff = substr( $file,10,2 );
			$date = "$yy年$mm月$dd日\t$hh時$ff分開演";
		} else { $date = "不明"; }
		$page++;
		print "<form method=\"POST\" action=\"$MGRCGI\">\n";
		print "<input type=\"hidden\" name=\"PASS\" value=\"$PASS\">\n";
		print "<input type=\"hidden\" name=\"FILE\" value=\"$file\">\n";
    	print "<input type=\"submit\" name=\"ACT\" value=\"変更\">\n";
    	print "<input type=\"submit\" name=\"ACT\" value=\"削除\">\n";
	print "<b>$date\t\t$seki\t\t$mai枚</b>\n";

		print "</form>\n";
	}
	print "<br>\n";
	if ( $page <= 0 ) { $MSG = "対象がありません。"; }
	&HtmlEnd;
}
## -------------------------------------------------------------------
## 新規登録、修正時、ノート内容入力サブルーチン
## -------------------------------------------------------------------
sub InputNote {
	$SUBTITLE = "$ACT";
	&HtmlStart;
	$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "大変混み合っています。しばらく待ってから再度お試しください。";
		&HtmlEnd;
	}
	&Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
	&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
	$MSG = '';
	if ( $ACT eq '新規登録' ) {
		($ss,$mm,$hh,$DD,$MM,$YY,$w,$y,$i) = localtime(time);
		$YY = 1900 + $YY;
		$MM = 1 + $MM;
		$FILE = sprintf("%04d%02d%02d%02d%02d",$YY,$MM,$DD,$hh,$mm);
	} else {
		foreach $line ( @LIST ) {
			( $file,$seki,$mai ) = split( /,/,$line );
		}
	}

	$MODE = $ACT;
	$yy = substr( $FILE,0,4 );
	$mm = substr( $FILE,4,2 );
	$dd = substr( $FILE,6,2 );
	$hh = substr( $FILE,8,2 );
	$ff = substr( $FILE,10,2 );
	$DATE = "$yy$mm$dd$hh$ff";
	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	print "<input type=\"hidden\" name=\"PASS\" value=\"$PASS\">\n";
	print "<input type=\"hidden\" name=\"MODE\" value=\"$MODE\">\n";
	print "<input type=\"hidden\" name=\"FILE\" value=\"$FILE\">\n";

	print "日付(2002年5月20日14時00分開演なら200205201400と入力)\n";
	print "<br><FONT color=\"#ff0080\">※開演２時間前に販売終了する設定ですので、必ず未来の日時にしてください。\n";
	print "<br>※変更は枚数しか出来ません。日時変更は削除→新規作成してください。</FONT>\n";
	print "<br><input type=\"text\" name=\"DATE\" value=\"$DATE\" size=20 maxlength=12><br>\n";
	##print "席種<input type=\"text\" name=\"SEKI\" value=\"$SEKI\" size=10maxlength=12><br>\n";
	print "枚数<input type=\"text\" name=\"MAI\" size=4>枚<br>\n";
   	print "<input type=\"submit\" name=\"ACT\" value=\"実行\">\n";
	print "</form>\n";
	&HtmlEnd;
}
## -------------------------------------------------------------------
## 確認サブルーチン
## -------------------------------------------------------------------
sub ConfNote {
	if ( $ACT eq '削除' ) { $MODE = $ACT; }
	$SUBTITLE = '更新確認';
	&HtmlStart;
	if ( $MODE ne '削除' ) {
		$MSG = &CheckNote;
		if ( $MSG ne '' ) { &HtmlEnd; }
	}
	if ( $MODE eq '新規登録' ) {
		($ss,$mm,$hh,$DD,$MM,$YY,$w,$y,$i) = localtime(time);
		$FILE = sprintf("$DATE");
	}
	$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "大変混み合っています。しばらく待ってから再度お試しください。";
		&HtmlEnd;
	}
	&Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
	&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
	$MSG = '';
	foreach $line ( @LIST ) {
		( $file,$seki,$mai ) = split( /,/,$line );
		if ( $file eq $FILE ) { last; }
	}
	if ( ($MODE eq '変更' || $MODE eq '削除') && $file ne $FILE ) {
		$MSG = "対象が見つかりません。";
		&HtmlEnd;
	}
	if ( $MODE eq '新規登録' && $file eq $FILE ) {
		$MSG = "対象が既にあります。。";
		&HtmlEnd;
	}
	if ( $MODE eq '削除' ) {
		$FILE = $file;
		$DATE = substr( $FILE,0,12 );
		$SEKI = $seki;
		$MAI = $mai;
	}

		if ( length( $DATE ) >= 12 ) {
			$y2 = substr( $DATE,0,4 );
			$m2 = substr( $DATE,4,2 );
			$d2 = substr( $DATE,6,2 );
			$h2 = substr( $DATE,8,2 );
			$f2 = substr( $DATE,10,2 );
			$date2 = "$y2年$m2月$d2日$h2時$f2分開演";
		}

	print "<p>$date2\t\t$SEKI\t\t$MAI枚</p>\n";

	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	print "<input type=\"hidden\" name=\"PASS\" value=\"$PASS\">\n";
	print "<input type=\"hidden\" name=\"MODE\" value=\"$MODE\">\n";
	print "<input type=\"hidden\" name=\"FILE\" value=\"$FILE\">\n";
	print "<input type=\"hidden\" name=\"DATE\" value=\"$DATE\">\n";
	print "<input type=\"hidden\" name=\"SEKI\" value=\"$SEKI\">\n";
	print "<input type=\"hidden\" name=\"MAI\" value=\"$MAI\">\n";
	print "以上の内容を$MODEします。よろしいですか？\n";
	print "<input type=\"submit\" name=\"ACT\" value=\"ＯＫ\">\n";

	print "</form>\n";
	&HtmlEnd;
}
## -------------------------------------------------------------------
## 更新サブルーチン
## -------------------------------------------------------------------
sub ExecNote {
	$SUBTITLE = '更新確認';
	$MSG = &CheckNote;
	if ( $MSG ne '' ) { &HtmlStart; &HtmlEnd; }
	if ( $DEMOFLG ne 'ON' ) {
		$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
		if ( $KEY != 9 ) {
			$MSG = "大変混み合っています。しばらく待ってから再度お試しください。";
			&HtmlStart;
			&HtmlEnd;
		}
		&Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
		$flg = 'NG';
		foreach $line ( @LIST ) {
			( $file,$seki,$mai ) = split( /,/,$line );
			if ( $file,$seki eq $FILE,$SEKI ) { $flg = 'OK'; next; }
			push( @OUTLIST,$line );
		}
		if ( $MODE eq '新規登録' ) {
			if ( $flg eq 'OK' ) {
				$MSG = "対象が既にあります。";
				&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HtmlStart;
				&HtmlEnd;
			}
			$line = "$FILE,$SEKI,$MAI";
			push( @OUTLIST,$line );
		}
		if ( $MODE eq '変更' ) {
			if ( $flg eq 'NG' ) {
				$MSG = "対象が見つかりません。";
				&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HtmlStart;
				&HtmlEnd;
			}
			foreach $line ( @OUTLIST ) {
				( $file,$seki,$mai ) = split( /,/,$line );
				if ( $file eq $DATE ) { last; }
			}
			#if ( $file eq $DATE ) {
			#	$MSG = "対象が既にあります。";
			#	&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);
			#	&HtmlStart;
			#	&HtmlEnd;
			#}
			$line = "$DATE,$SEKI,$MAI";
			push( @OUTLIST,$line );
		}
		if ( $MODE eq '削除' ) {
			if ( $flg eq 'NG' ) {
				$MSG = "対象が見つかりません。";
				&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HtmlStart;
				&HtmlEnd;
			}
		}
		if ( open( OUT,">$FILEDIR/$LSTFILE" ) ) {
			@OUTLIST = sort( @OUTLIST );
			foreach $line ( @OUTLIST ) { print OUT "$line\n"; }
			close( OUT );
		} else {
			$MSG = "リストファイルに保存することが出来ません。";
			&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
			&HtmlStart;
			&HtmlEnd;
		}
		&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
	}
	&DispView;
}
## -------------------------------------------------------------------
## ノートチェックサブルーチン
## -------------------------------------------------------------------
sub CheckNote {
	if ( length($DATE) != 12 || $DATE =~ /[^0-9]/ ) {
	 	return '日時は半角数字12桁で表現してください。YYYYMMDDhhmm';
	}
	$yy = substr( $DATE,0,4 );
	$mm = substr( $DATE,4,2 );
	$dd = substr( $DATE,6,2 );
	$hh = substr( $DATE,8,2 );
	$ff = substr( $DATE,10,2 );
	if ( $yy <= 1899 || $yy >= 3000 ) {
		return '年は、1900年から2999年までです。';
	}
	if ( $mm <= 0 || $mm >= 13 ) {
		return '月は、01月から12月までです。';
	}
	if ( ($yy % 4) == 0 ) { $monthday[2] = $monthday[2] + 1; }
	if ( $dd <= 0 || $dd > $monthday[$mm] ) {
		return sprintf "%02d月は、01日から%02d日までです。",$mm,$monthday[$mm];
	}
	if ( $hh < 0 || $hh >= 24 ) {
		return '時は、00時から23時までです。';
	}
	if ( $ff = 0 || $ff >= 60 ) {
		return '分は、00分から59分までです。';
	}
	if ( $MAI =~ /[^0-9]/ ) {
	 	return '枚数は半角数字で入力してください。';
	}
	if ( $MAI eq '' ) {
		return '枚数が入力されていません。';
	}
	return '';
}
## -------------------------------------------------------------------
## HTMLヘッダー表示サブルーチン
## -------------------------------------------------------------------
sub HtmlStart {
	print "Content-type: text/html\n\n";
	print "<html><head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "<title>$TITLE（$SUBTITLE）</title></head>\n";
	if ( -f $BGGIF ) { print "<body background=\"$BGGIF\" TEXT=\"$FGCOLOR\" LINK=\"$LINK\" VLINK=\"$VLINK\" ALINK=\"$ALINK\">\n"; }
	else { print "<body bgcolor=\"$BGCOLOR\" TEXT=\"$FGCOLOR\" LINK=\"$LINK\" VLINK=\"$VLINK\" ALINK=\"$ALINK\">\n"; }

    print "$TITLE（$SUBTITLE）\n";
	if ( $SUBTITLE eq '管理画面' ) {
	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	print "<input type=\"hidden\" name=\"PASS\" value=\"$PASS\">\n";
    	print "<input type=\"submit\" name=\"ACT\" value=\"新規登録\">\n";
   	print "</form>\n";
	}
}
## -------------------------------------------------------------------
## HTMLフッター表示サブルーチン
## -------------------------------------------------------------------
sub HtmlEnd {
		print "<p align=right>[<A HREF=\"$MENUCGI\">フォーム</A>]</p>\n";
	print "</body></html>\n";
	exit(0);
}
