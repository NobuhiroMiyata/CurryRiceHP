#!/usr/bin/perl
require "jcode.pl";
require "cfg.cgi";
##�`�P�b�g�\��t�H�[�� �Ǘ�CGI�@2002/03/03
## -------------------------------------------------------------------
## ���̃X�N���v�g�݂͂̃m�[�g������seo���������܂����B
## ���̃X�N���v�g���g�p���������Ȃ鑹�Q����҂͂��̐ӂ𕉂��܂���B
## ���̃X�N���v�g�̉����O�f�[�^��http://www.mino.net/cgi/
## -------------------------------------------------------------------
## ���C�������X�^�[�g
## -------------------------------------------------------------------
@monthday = (0,31,28,31,30,31,30,31,31,30,31,30,31);
## �������
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
## ��������
if ( $ACT eq '�Ǘ�' )     {
	if ( $MGRPASS ne '' ) { &InputPass; }
	else { $ACT = '�Ǘ����'; &DispView; }
}
elsif ( $PASS ne $MGRPASS ) {
	$SUBTITLE = '���O�C��';
	&HtmlStart;
	$MSG = '�Ǘ��p�X���[�h���Ⴂ�܂��B';
	&HtmlEnd;
}
elsif ( $ACT eq '�Ǘ����' ) { &DispView; }
elsif ( $ACT eq '�V�K�o�^' ) { &InputNote; }
elsif ( $ACT eq '�ύX' )     { &InputNote; }
elsif ( $ACT eq '�폜' )     { &ConfNote; }
elsif ( $ACT eq '���s' )     { &ConfNote; }
elsif ( $ACT eq '�n�j' )     { &ExecNote; }
else                         { $MSG = '���삪�ςł��B'; }
$SUBTITLE = '�G���[';
&HtmlStart;
&HtmlEnd;
exit(0);

## -------------------------------------------------------------------
## �p�X���[�h���͉�ʃT�u���[�`��
## -------------------------------------------------------------------
sub InputPass {
	$SUBTITLE = '���O�C��';
	&HtmlStart;
	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	print "�Ǘ��p�X���[�h�F\n";
	print "<input type=\"hidden\" name=\"ACT\" value=\"�Ǘ����\">\n";
   	print "<input type=\"password\" name=\"PASS\" value=\"\">\n";
   	print "<input type=\"submit\" value=\"�n�j\">\n";
	print "</form>\n";
	&HtmlEnd;
}
## -------------------------------------------------------------------
## �ꗗ�\���T�u���[�`��
## -------------------------------------------------------------------
sub DispView {
	$SUBTITLE = '�Ǘ����';
	&HtmlStart;
	$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "��ύ��ݍ����Ă��܂��B���΂炭�҂��Ă���ēx���������������B";
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
			$date = "$yy�N$mm��$dd��\t$hh��$ff���J��";
		} else { $date = "�s��"; }
		$page++;
		print "<form method=\"POST\" action=\"$MGRCGI\">\n";
		print "<input type=\"hidden\" name=\"PASS\" value=\"$PASS\">\n";
		print "<input type=\"hidden\" name=\"FILE\" value=\"$file\">\n";
    	print "<input type=\"submit\" name=\"ACT\" value=\"�ύX\">\n";
    	print "<input type=\"submit\" name=\"ACT\" value=\"�폜\">\n";
	print "<b>$date\t\t$seki\t\t$mai��</b>\n";

		print "</form>\n";
	}
	print "<br>\n";
	if ( $page <= 0 ) { $MSG = "�Ώۂ�����܂���B"; }
	&HtmlEnd;
}
## -------------------------------------------------------------------
## �V�K�o�^�A�C�����A�m�[�g���e���̓T�u���[�`��
## -------------------------------------------------------------------
sub InputNote {
	$SUBTITLE = "$ACT";
	&HtmlStart;
	$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "��ύ��ݍ����Ă��܂��B���΂炭�҂��Ă���ēx���������������B";
		&HtmlEnd;
	}
	&Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
	&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
	$MSG = '';
	if ( $ACT eq '�V�K�o�^' ) {
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

	print "���t(2002�N5��20��14��00���J���Ȃ�200205201400�Ɠ���)\n";
	print "<br><FONT color=\"#ff0080\">���J���Q���ԑO�ɔ̔��I������ݒ�ł��̂ŁA�K�������̓����ɂ��Ă��������B\n";
	print "<br>���ύX�͖��������o���܂���B�����ύX�͍폜���V�K�쐬���Ă��������B</FONT>\n";
	print "<br><input type=\"text\" name=\"DATE\" value=\"$DATE\" size=20 maxlength=12><br>\n";
	##print "�Ȏ�<input type=\"text\" name=\"SEKI\" value=\"$SEKI\" size=10maxlength=12><br>\n";
	print "����<input type=\"text\" name=\"MAI\" size=4>��<br>\n";
   	print "<input type=\"submit\" name=\"ACT\" value=\"���s\">\n";
	print "</form>\n";
	&HtmlEnd;
}
## -------------------------------------------------------------------
## �m�F�T�u���[�`��
## -------------------------------------------------------------------
sub ConfNote {
	if ( $ACT eq '�폜' ) { $MODE = $ACT; }
	$SUBTITLE = '�X�V�m�F';
	&HtmlStart;
	if ( $MODE ne '�폜' ) {
		$MSG = &CheckNote;
		if ( $MSG ne '' ) { &HtmlEnd; }
	}
	if ( $MODE eq '�V�K�o�^' ) {
		($ss,$mm,$hh,$DD,$MM,$YY,$w,$y,$i) = localtime(time);
		$FILE = sprintf("$DATE");
	}
	$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
	if ( $KEY != 9 ) {
		$MSG = "��ύ��ݍ����Ă��܂��B���΂炭�҂��Ă���ēx���������������B";
		&HtmlEnd;
	}
	&Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
	&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
	$MSG = '';
	foreach $line ( @LIST ) {
		( $file,$seki,$mai ) = split( /,/,$line );
		if ( $file eq $FILE ) { last; }
	}
	if ( ($MODE eq '�ύX' || $MODE eq '�폜') && $file ne $FILE ) {
		$MSG = "�Ώۂ�������܂���B";
		&HtmlEnd;
	}
	if ( $MODE eq '�V�K�o�^' && $file eq $FILE ) {
		$MSG = "�Ώۂ����ɂ���܂��B�B";
		&HtmlEnd;
	}
	if ( $MODE eq '�폜' ) {
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
			$date2 = "$y2�N$m2��$d2��$h2��$f2���J��";
		}

	print "<p>$date2\t\t$SEKI\t\t$MAI��</p>\n";

	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	print "<input type=\"hidden\" name=\"PASS\" value=\"$PASS\">\n";
	print "<input type=\"hidden\" name=\"MODE\" value=\"$MODE\">\n";
	print "<input type=\"hidden\" name=\"FILE\" value=\"$FILE\">\n";
	print "<input type=\"hidden\" name=\"DATE\" value=\"$DATE\">\n";
	print "<input type=\"hidden\" name=\"SEKI\" value=\"$SEKI\">\n";
	print "<input type=\"hidden\" name=\"MAI\" value=\"$MAI\">\n";
	print "�ȏ�̓��e��$MODE���܂��B��낵���ł����H\n";
	print "<input type=\"submit\" name=\"ACT\" value=\"�n�j\">\n";

	print "</form>\n";
	&HtmlEnd;
}
## -------------------------------------------------------------------
## �X�V�T�u���[�`��
## -------------------------------------------------------------------
sub ExecNote {
	$SUBTITLE = '�X�V�m�F';
	$MSG = &CheckNote;
	if ( $MSG ne '' ) { &HtmlStart; &HtmlEnd; }
	if ( $DEMOFLG ne 'ON' ) {
		$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
		if ( $KEY != 9 ) {
			$MSG = "��ύ��ݍ����Ă��܂��B���΂炭�҂��Ă���ēx���������������B";
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
		if ( $MODE eq '�V�K�o�^' ) {
			if ( $flg eq 'OK' ) {
				$MSG = "�Ώۂ����ɂ���܂��B";
				&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HtmlStart;
				&HtmlEnd;
			}
			$line = "$FILE,$SEKI,$MAI";
			push( @OUTLIST,$line );
		}
		if ( $MODE eq '�ύX' ) {
			if ( $flg eq 'NG' ) {
				$MSG = "�Ώۂ�������܂���B";
				&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HtmlStart;
				&HtmlEnd;
			}
			foreach $line ( @OUTLIST ) {
				( $file,$seki,$mai ) = split( /,/,$line );
				if ( $file eq $DATE ) { last; }
			}
			#if ( $file eq $DATE ) {
			#	$MSG = "�Ώۂ����ɂ���܂��B";
			#	&Com'lockoff("$FILEDIR/$LOCKFILE",$KEY);
			#	&HtmlStart;
			#	&HtmlEnd;
			#}
			$line = "$DATE,$SEKI,$MAI";
			push( @OUTLIST,$line );
		}
		if ( $MODE eq '�폜' ) {
			if ( $flg eq 'NG' ) {
				$MSG = "�Ώۂ�������܂���B";
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
			$MSG = "���X�g�t�@�C���ɕۑ����邱�Ƃ��o���܂���B";
			&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
			&HtmlStart;
			&HtmlEnd;
		}
		&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
	}
	&DispView;
}
## -------------------------------------------------------------------
## �m�[�g�`�F�b�N�T�u���[�`��
## -------------------------------------------------------------------
sub CheckNote {
	if ( length($DATE) != 12 || $DATE =~ /[^0-9]/ ) {
	 	return '�����͔��p����12���ŕ\�����Ă��������BYYYYMMDDhhmm';
	}
	$yy = substr( $DATE,0,4 );
	$mm = substr( $DATE,4,2 );
	$dd = substr( $DATE,6,2 );
	$hh = substr( $DATE,8,2 );
	$ff = substr( $DATE,10,2 );
	if ( $yy <= 1899 || $yy >= 3000 ) {
		return '�N�́A1900�N����2999�N�܂łł��B';
	}
	if ( $mm <= 0 || $mm >= 13 ) {
		return '���́A01������12���܂łł��B';
	}
	if ( ($yy % 4) == 0 ) { $monthday[2] = $monthday[2] + 1; }
	if ( $dd <= 0 || $dd > $monthday[$mm] ) {
		return sprintf "%02d���́A01������%02d���܂łł��B",$mm,$monthday[$mm];
	}
	if ( $hh < 0 || $hh >= 24 ) {
		return '���́A00������23���܂łł��B';
	}
	if ( $ff = 0 || $ff >= 60 ) {
		return '���́A00������59���܂łł��B';
	}
	if ( $MAI =~ /[^0-9]/ ) {
	 	return '�����͔��p�����œ��͂��Ă��������B';
	}
	if ( $MAI eq '' ) {
		return '���������͂���Ă��܂���B';
	}
	return '';
}
## -------------------------------------------------------------------
## HTML�w�b�_�[�\���T�u���[�`��
## -------------------------------------------------------------------
sub HtmlStart {
	print "Content-type: text/html\n\n";
	print "<html><head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "<title>$TITLE�i$SUBTITLE�j</title></head>\n";
	if ( -f $BGGIF ) { print "<body background=\"$BGGIF\" TEXT=\"$FGCOLOR\" LINK=\"$LINK\" VLINK=\"$VLINK\" ALINK=\"$ALINK\">\n"; }
	else { print "<body bgcolor=\"$BGCOLOR\" TEXT=\"$FGCOLOR\" LINK=\"$LINK\" VLINK=\"$VLINK\" ALINK=\"$ALINK\">\n"; }

    print "$TITLE�i$SUBTITLE�j\n";
	if ( $SUBTITLE eq '�Ǘ����' ) {
	print "<form method=\"POST\" action=\"$MGRCGI\">\n";
	print "<input type=\"hidden\" name=\"PASS\" value=\"$PASS\">\n";
    	print "<input type=\"submit\" name=\"ACT\" value=\"�V�K�o�^\">\n";
   	print "</form>\n";
	}
}
## -------------------------------------------------------------------
## HTML�t�b�^�[�\���T�u���[�`��
## -------------------------------------------------------------------
sub HtmlEnd {
		print "<p align=right>[<A HREF=\"$MENUCGI\">�t�H�[��</A>]</p>\n";
	print "</body></html>\n";
	exit(0);
}
