#!/usr/bin/perl
require "jcode.pl";
require "cfg.cgi";
##�`�P�b�g�\��t�H�[�� �t�H�[��CGI�@2002/03/03
## -------------------------------------------------------------------
## ���̃X�N���v�g�݂͂̃m�[�g������seo���������܂����B
## ���̃X�N���v�g���g�p���������Ȃ鑹�Q����҂͂��̐ӂ𕉂��܂���B
## ���̃X�N���v�g�̉����O�f�[�^��http://www.mino.net/cgi/
## -------------------------------------------------------------------
## ���C�������X�^�[�g
## -------------------------------------------------------------------
## �������
&Com'getagv;
if ( $Com'FORM{'SORTFLG'} ne '' ) { $SORTFLG = $Com'FORM{'SORTFLG'}; }
if ( $Com'FORM{'SKEY'} ne '' ) { $SKEY = $Com'FORM{'SKEY'}; }
if ( $Com'FORM{'BACK'} ne '' ) { $BACK = $Com'FORM{'BACK'}; }
$MSG  = '';
@LIST = ();
## HTML�w�b�_�[�\��
&HtmlStart;
## ���e�\��
&DispView;
## HTML�t�b�^�[�\��
&HtmlEnd;
exit(0);

## -------------------------------------------------------------------
## ���e�\���T�u���[�`��
## -------------------------------------------------------------------
sub DispView {
	$KEY = &Com'lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "��ύ��ݍ����Ă��܂��B���΂炭�҂��Ă���ēx���������������B";
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
			$date = "$yy�N$mm��$dd��\t$hh��$ff���J�n\t$seki";
		} else { $date = "�s��"; }

if ( $year >= $yy && $mon > $mm ) {
print "<font color=red><b>�~</b></font><b>$date</b>\t\t<font color=red>��t�I��</font>\n";
}elsif( $year >= $yy && $mon >= $mm && $mday > $dd ) {
print "<font color=red><b>�~</b></font><b>$date</b>\t\t<font color=red>��t�I��</font>\n";
}elsif( $year >= $yy && $mon >= $mm && $mday >= $dd && $hour >= $hh-$end ) {
print "<font color=red><b>�~</b></font><b>$date</b>\t\t<font color=red>��t�I��</font>\n";
}else{
if ( $mai <= 0 ) {
	print "<font color=red><b>�~</b></font>\n";
		}else{
	print "<input type=radio name=day value=$yy$mm$dd$hh$ff checked>\n";
	print "<input type=hidden name=\"$yy$mm$dd$hh$ff\" value=\"$mai\">\n";
		}
			print "<b>$date</b>\n";

if ( $mai <= $zan && $mai >= 1 ) {
	print "\t\t<font color=red>�c��$mai�l</font>\n";
		}
if ( $mai <= 0 ) {
	print "\t\t<font color=red>����</font>\n";
		}
}
			print "<br>\n";

	}
}

## -------------------------------------------------------------------
## HTML�w�b�_�[�\���T�u���[�`��
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
## HTML�t�b�^�[�\���T�u���[�`��
## -------------------------------------------------------------------
sub HtmlEnd {
	if ( $MSG ne '' ) {
		print "</form><br><br><font color=\"#FF0000\" size=+1><b>$MSG</b></font><br><br>\n";
	}else{
	print "<div style='display:none'><br>����\n";
	print "<input type=radio name=\"mai\" value=\"1\" checked>1\n";
	print "<input type=radio name=\"mai\" value=\"2\">2\n";
	print "<input type=radio name=\"mai\" value=\"3\">3\n";
	print "<input type=radio name=\"mai\" value=\"4\">4\n";
	print "<input type=radio name=\"mai\" value=\"5\">5\n";
	print "<input type=radio name=\"mai\" value=\"6\">6\n";
	print "<br></div>\n";
	
	print "<p>�Q���Ҏ����i�J�^�J�i��t���l�[���j<br><input type=text size=30 name=\"name\"></p>\n";
	print "<p>�N�� <input type=text size=3 name=\"age\">��</p>\n";
	print "<p>���� <label><input type=radio name=\"gender\" value=\"�j��\">�j��</label>�@<label><input type=radio name=\"gender\" value=\"����\">����</label></p>\n";
	print "<p>E-Mail <input type=text size=30 name=\"email\"></p>\n";
	print "<p>TEL <input type=text size=13 name=\"tel\"></p>\n";
	print "<p>���l <input type=text size=30 name=\"biko\"></p>\n";
	print "�m���M�n�{�^�����P��̂݉����Ă��������B<br>\n";
	print "<input type=submit value=\"���M\">�@\n";
	print "<input type=reset value=\"���Z�b�g\">\n";
	print "<br><br>���M�ł��Ȃ��ꍇ�A<a href=\"mailto:yoyaku\@gekidan-curryrice.com\">���[��</a>�ɂĂ��A�����������B<br>\n";
	print "</form><br><br>\n";
	}
print "<br>\n";

	print "<p align=right>\n";
	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	if ( $MGRFLG eq 'ON' ) {
		print "<input type=\"submit\" name=\"ACT\" value=\"�Ǘ�\">\n";
		print "<br>\n";
print "<br>\n";
print "<br>\n";

		
	}
	print "</form>\n";

	print "</body></html>\n";
	exit(0);
}

