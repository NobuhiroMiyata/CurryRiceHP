#!/usr/bin/perl
require "jcode.pl";
require "cfg.cgi";
########
##	���[���X�N���v�g
########
# �e��ݒ�

##
## �t�H�[���f�[�^�̎�荞��
##
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

@wday_array = ('��','��','��','��','��','��','�y');
$date_now = sprintf("%02d\/%01d\/%01d(%s)%02d\:%02d",$year +1900,$mon +1,$mday,$wday_array[$wday],$hour,$min,$sec);

#�O���[�o���ϐ���`
#���Ȏc��
$g_zanseki;
#�\��
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

## �G���[�`�F�b�N
if ( $FORM{'day'} eq '' ) {
	push ( @error, '������I�����Ă��������B');
}
if ( $FORM{'mai'} eq '' ) {
	push ( @error, '��������͂��Ă��������B');
}
#$tmp1 = "$DATE" . "_zanseki";
if ( $FORM{$DATE} < $FORM{'mai'}) {
	push ( @error, '�������c���𒴂��Ă��܂��B');
}
if ( $FORM{'name'} eq '' ) {
	push ( @error, '��������͂��Ă��������B');
}
if ( $FORM{'email'} eq '' ) {
	push ( @error, '�A���p���[���A�h���X����͂��Ă��������B');
}
if ( $FORM{'email'} !~ /^[\!-~]+\@[\!-~]+\.[\!-~]+$/ && $FORM{'email'} ne '' ) {
	push ( @error, '�A���p���[���A�h���X������������܂���B');
}
if ( $FORM{'email'} =~ m/[<>]/ ) {
	push ( @error, '�A���p���[���A�h���X������������܂���B');
}
if ( $FORM{'tel'} eq '' ) {
	push ( @error, '�A���p�d�b�ԍ�����͂��Ă��������B');
}

## �G���[���Ȃ������Ƃ�
if ( ! @error ) {

		if ( length( $DATE ) >= 12 ) {
			$y2 = substr( $DATE,0,4 );
			$m2 = substr( $DATE,4,2 );
			$d2 = substr( $DATE,6,2 );
			$h2 = substr( $DATE,8,2 );
			$f2 = substr( $DATE,10,2 );
			$date = "$y2�N$m2��$d2��$h2��$f2���J��";
		}

	# �`�P�b�g�f�[�^�C��
	&ticket;


sub regist{

	$DATE = substr( $FORM{'day'},0,12 );

	# CSV�f�[�^�쐬
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


	## ���[�����M

	# ���[���f�[�^�쐬
	$maildata =<<END;
Subject:Ticket Order
From:$FORM{'email'}

���L�̒ʂ�A�`�P�b�g����������܂����B
���M����	: $date_now
��]����	: $date
����	: $FORM{'mai'} ��
�����O	: $FORM{'name'}
E-MAIL	: $FORM{'email'}
�d�b�ԍ�	: $FORM{'tel'}
���l	: $FORM{'biko'}

END

	# �T���N�X���[���f�[�^
	$maildata1 =<<END;
Subject:Thanks for your order!
From:$admin_email

����ɂ��́B
���c�J���[���C�X�ł��B
�`�P�b�g�\\������L�̂Ƃ��菳��܂����B
���M����	: $date_now
��]����	: $date
����		: $FORM{'mai'} ��
�����O	: $FORM{'name'}
E-MAIL	: $FORM{'email'}
�d�b�ԍ�	: $FORM{'tel'}

�ύX����$admin_email�ւ���񂭂������B

����ł́A����ŉ�܂��傤�I
�����̃��[���ɐg�Ɋo���̂Ȃ����͂��̂܂܂��ԐM���������B

END

	&jcode::convert(*maildata, 'sjis');
	&jcode::convert(*maildata1, 'sjis');

	# �Ǘ��҂Ƀ��[��
         if (!open(OUT,"| $sendmail $admin_email")) { last; }
         print OUT $maildata;
         close(OUT);

	# ���M��Ƀ��[��
         if (!open(OUT,"| $sendmail $send_email")) { last; }
         print OUT $maildata;
         close(OUT);

	# �\���҂Ƀ��[��
         if (!open(OUT,"| $sendmail $FORM{'email'}")) { last; }
         print OUT $maildata1;
         close(OUT);


	##
	## HTML�p���b�Z�[�W
	##
	$html_message =
"����ɂ��́I
���\\�񂠂肪�Ƃ��������܂����B���L�̂Ƃ��菳��܂����B<br><br>
���M����	: $date_now<br>
��]����	: $date <br>
����		: $FORM{'mai'} ��<br>
�����O	: $FORM{'name'} <br>
E-MAIL	: $FORM{'email'}<br>
�d�b�ԍ�	: $FORM{'tel'}<br>
<br>
����ł́A����ł��҂����Ă���܂��I<br>
<br>
<p>[<a href='#' onClick='window.close(); return false;'>����</a>]</p>
";
&HTML;

}

## �G���[���������Ƃ�
} else {
	$html_message =  "<p><font color=red><b>���󂯏o���܂���B<br>���L�̓��e�����m�F���������B</b></font></p><UL>\n";
	foreach ( @error ) {
		$html_message .= "\t<LI>$_</LI>\n";
	}
	$html_message .= "</UL>\n[<a href='' onClick='history.go(-1); return false;'>�߂�</a>]";
	&HTML;
}
	#�`�P�b�g��������
sub ticket{
		#���b�N����(�I��)
		$KEY = &Com::lockon("$FILEDIR/$LOCKFILE");
		if ( $KEY != 9 ) {
			$html_message = "��ύ��ݍ����Ă��܂��B���΂炭�҂��Ă���ēx���������������B";
			&HTML;
		}
		&Com::GetList( "$FILEDIR/$LSTFILE",$SORTFLG,*LIST,*MSG );
		#�t���O�̏�����
		$flg = 'NG';

		#�X�V�Ώۃ��R�[�h�̌���
		foreach $line ( @LIST ) {
			#day.dat����X�V�Ώۂ̃��R�[�h��T������BCSV�𕪉�(�������A���z�A�c���Ȑ��A�L���p�A���ݗ\��)
			( $ymdhm, $yen, $zanseki, $M_seki, $yoyakusu) = split( /,/,$line );
			#�X�V�Ώۃ��R�[�h������������A�c���Ȑ������Z�A���ݗ\�񐔂����Z����B
			if ( $ymdhm eq $DATE ) {
				$flg = 'OK';
				#�c�Ȑ��̌v�Z
				$g_zanseki = $zanseki - $FORM{'mai'};
				#�\�񐔂��C���N�������g
				$g_yoyakusu = ++$yoyakusu;
				next;
			}
			#�X�V�ΏۊO�̃��R�[�h��z��ɏ����o��
			push( @OUTLIST,$line );
		}

		#NG�̏ꍇ(�X�V�Ώۃ��R�[�h�����݂��Ȃ��ꍇ)�����I��
		if ( $flg eq 'NG' ) {
				$html_message = "�Ώۂ�������܂���B";
				&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
				&HTML;
		}

		#��OUTLIST�ɍX�V�Ώۃ��R�[�h���܂܂�Ă��邩����
		foreach $line ( @OUTLIST ) {
			#( $file,$seki,$mai ) = split( /,/,$line );
			( $ymdhm, $yen, $zanseki, $M_seki, $yoyakusu) = split( /,/,$line );
			if ( $ymdhm eq $DATE ) { last; }
		}
		#��OUTLIST�ɍX�V�Ώۃ��R�[�h���܂܂�Ă���ꍇ�����I��
		if ( $ymdhm eq $DATE ) {
			$MSG = "�Ώۂ����ɂ���܂��B";
			&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
			&HTML;
		}

		#�X�V�ς݃f�[�^����OUTLIST�z��ɒǉ�����
		$line = "$DATE,$yen,$g_zanseki,$M_seki,$g_yoyakusu";
		push( @OUTLIST,$line );

		#day.dat�ւ̏������ݏ���
		if ( open( OUT,">$FILEDIR/$LSTFILE" ) ) {
			@OUTLIST = sort( @OUTLIST );
			foreach $line ( @OUTLIST ) { print OUT "$line\n"; }
			close( OUT );
		} else {
			$html_message = "���X�g�t�@�C���ɕۑ����邱�Ƃ��o���܂���B";
			&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
			&HTML;
		}
		&Com::lockoff("$FILEDIR/$LOCKFILE",$KEY);
		&regist;
}

## HTML�\��
sub HTML {
printf <<END;

<html>
<head>
<title>�`�P�b�g���̓t�H�[��</title>
<meta http-equiv="Content-Type" content="text/html; charset=sjis">
</head>
<body bgcolor="#FFFFFF">
  <p>$html_message</p>
</body>
</html>
END
}
