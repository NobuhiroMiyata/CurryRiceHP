#!/usr/bin/perl

require './jcode.pl';
require './cfg.cgi';
##�`�P�b�g�\��t�H�[�� �ꗗ�\��CGI�@2002/03/03
## -------------------------------------------------------------------
## ���̃X�N���v�g�͈ȉ��̃X�N���v�g������seo���������܂����B
## ������g���ɂ�cfg.cgi��$csvmode��1�ɐݒ肵�Ă��������B
#----------------------------
$ver="BBS-i v3.3";
# (i-mode�����ȈՌf����/���L)
#----------------------------
# Copyright(C) ��イ����
# E-Mail:ryu@cj-c.com
# W W W :http://www.cj-c.com/

#-- �ݒ�t�@�C�� -------------*

$met  = "POST";			# ���M�`��(POST or GET(J-Sky�̏ꍇ�����I��GET�ɂȂ�܂�))
$pass = "curry1012";			# �Ǘ��p�̃p�X���[�h���v�ύX
$a_max= 10;			# 1�y�[�W�\������

$cgi_f= "./read.cgi";		# ���̃t�@�C��

$lockf= "./bi.loc";		# ���b�N�t�@�C��(�g�p��17�s�ڂɈˑ�)

# �A�N�Z�X�Ώۂ�?
# => (0=�Ƃ��ɖ��� 1=J-Sky 2=i-mode 3=�h�b�gi 4=J-Sky�y��i-mode�y�уh�b�gi)
$access= 0;

#--- �ݒ肱���܂�---------------*
$j_=0;$i_=0;$a_=0;
$Imode=$ENV{'HTTP_USER_AGENT'};
$Jskyw=$ENV{'HTTP_X_JPHONE_MSNAME'};
if($Jskyw ne ""){$j_=1;}
if($Imode=~ /DoCoMo/){$i_=1;}
elsif($Imode=~ /J-PHONE\/2/){$j_=1;}
elsif($Imode=~ /J-PHONE\/3/){$j_=2;}
elsif($Imode=~ /ASTEL/){$a_=1;}
if($j_ || $i_ || $a_){$PC=0;}else{$PC=1;}
$html="";
&d_code_;

if($j_==1){$met="GET";}
if($j){$MAX=" maxlength=50";}else{$MAX="";}
if($mode eq "edit"){&Edit; }
if($mode eq "bak"){ &bak_; }
if($mode eq "del"){ &del_; }
if($access){
	if($access==1 && $j_==0){&er_("J-Sky�[���ű������Ă�������!");}
	elsif($access==2 && $i_==0){&er_("i-mode�[���ű������Ă�������!");}
	elsif($access==3 && $a_==0){&er_("�ޯ�i�[���ű������Ă�������!");}
	elsif($access==4 && $a_==0 && $i_==0 && $j_==0){&er_("i-mode/J-Sky/�ޯ�i�[���ű������ĉ�����!");}
}
&html_;
#
# [�g�b�v�y�[�W]
#
sub html_ {

open(LOG,"$LSTFILE") || &er_("Can't open $LSTFILE");
@lines = <LOG>;
close(LOG);

&hed_;
$html.= "\�\\��ꗗ<hr>\n";
$html.="<form action=\"$cgi_f\" method=$met>";

$total=@lines;
$page_=int(($total-1)/$a_max);
if ($FORM{'page'} eq '') { $page = 0; } 
	else { $page = $FORM{'page'}; }
	$end_data = @lines - 1;
	$page_end = $page + ($a_max - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }

foreach ($page .. $page_end) {
($file,$mai) = split(/,/,$lines[$_]);
		if ( length( $file ) >= 12 ) {
			$yy = substr( $file,0,4 );
			$mm = substr( $file,4,2 );
			$dd = substr( $file,6,2 );
			$hh = substr( $file,8,2 );
			$ff = substr( $file,10,2 );
			$date = "$yy�N$mm��$dd��\t$hh��$ff���J��";
		} else { $date = "�s��"; }

$html.= "<input type=radio name=log value=$yy$mm$dd$hh$ff>\n";
$html.= "$date\t\t<font color=red>\n";

if ( $mai <= 0 ) {
$html.=  "�̔��I��\n";
}else{
$html.=  "�c��$mai��\n";}
$html.=  "</font><br>\n";

}

$html.= <<"_HTML_";
<input type=hidden name=mode value=del>
<input type=password name=pass size=6>
<input type=submit value="�\\��"><br>
</form></div>
_HTML_
	&foot_;
}
#
# [�w�b�_�\��]
#
sub hed_ {
$html.= <<"_HTML_";
<html><head><title>Reserve List</title>
<!--$ver--><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
</head>
<body>
_HTML_
}
#
# [�t�b�^�\��]
#
sub foot_ {
	$html.= <<"_HTML_";
<hr><!--���쌠�\\�� �폜�s��-->
<a href="http://www.cj-c.com/i/" target=_top>BBS-i</a>
_HTML_
	$html.= "</body></html>\n";
	&htmlp;
}
#
# [�t�H�[���Ȃǂ̃f�R�[�h]
#
sub d_code_ {
if($ENV{'REQUEST_METHOD'} eq "POST"){
	if ($ENV{'CONTENT_LENGTH'} > 10000) { &er_("���͂����܂�ɒ������܂�!"); }
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}else{ $buffer = $ENV{'QUERY_STRING'}; }

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value,'sjis');
		$value =~ s/&/\&amp\;/g;
		$value =~ s/</\&lt\;/g;
		$value =~ s/>/\&gt\;/g;
		$value =~ s/\"/\&quot\;/g;
		$value =~ s/<>/\&lt\;\&gt\;/g;
		$value =~ s/<!--(.|\n)*-->//g;
	$FORM{$name} = $value;
	if($name eq 'del'){push(@d_,$value);}
	if($name ne 'comment'){$value =~ s/\r|\n|\r\n/ /g;}
}
$name = $FORM{'name'};
$comment=$FORM{'comment'};$comment=~ s/\r\n|\r|\n/<br>/g;
$email= $FORM{'email'};
$mode = $FORM{'mode'};
$kiji = $FORM{'kiji'};
$namber=$FORM{'namber'};
$no   = $FORM{'no'};

}

#
# [�Ǘ��p�y�[�W]
#
sub del_ {
if ($FORM{'pass'} ne "$pass") { &er_("�p�X���[�h���Ⴂ�܂�!"); }

$file = $FORM{'log'};
$log="$csvd$file.csv";

open(LOG,"$log") || &er_("Can't open $log");
@lines = <LOG>;
close(LOG);

		if ( length( $FORM{'log'} ) >= 12 ) {
			$yy = substr( $file,0,4 );
			$mm = substr( $file,4,2 );
			$dd = substr( $file,6,2 );
			$hh = substr( $file,8,2 );
			$ff = substr( $file,10,2 );
			$date = "$yy�N$mm��$dd��\t$hh��$ff���J��";
		} else { $date = "�s��"; }

&hed_;
$html.= "<center>\n";
$html.= "$date\n";

$html.= <<"_HTML_";
<hr>
[<a href="$cgi_f">��</a>]
</center><hr><table border=1>
_HTML_

$total=@lines;
$page_=int(($total-1)/$a_max);
if ($FORM{'page'} eq '') { $page = 0; } 
	else { $page = $FORM{'page'}; }
	$end_data = @lines - 1;
	$page_end = $page + ($a_max - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }

foreach ($page .. $page_end) {
$lines[$_] =~ s/"//g;
($date_now,$date,$mai,$name,$email,$tel,$biko) = split(/,/,$lines[$_]);
$html.= "<tr><td>$name</td><td>$mai��</td><td>$tel</td><td>$biko</td><td>$date_now</td></tr>\n";
}
$html.= "</table>\n";
$a=0;
for($i=0;$i<=$page_;$i++){
$af=$page/$a_max;
if($PC){$P=$page_; $M=0;}else{$P=$af+2; $M=$af-2;}
	if($i eq $af || $i > $P || $i < $M){ $html.= "$i\n";}
	else{$html.= "<a href=\"$cgi_f?mode=del&page=$a&log=$file&pass=$pass\">$i</a>\n";}
$a+=$a_max;
}
	&foot_;
}
#
# [�G���[�\��]
#
sub er_ {
if (-e $lockf) { unlink($lockf); }
	&hed_;
	$html.= "<center>[<a href=\"$cgi_f?no=$no\">��</a>]<br>ERROR<br>$_[0]</center>\n";
	&foot_;
}

#
# [�����o��]
#
sub htmlp {
$len = length($html);
print "Content-type: text/html\n";
if($i_){print "Content-length: $len\n";}
print "\n";
print "$html";
exit;
}
#
# [���O����]
#
sub l_m {
open(DB,">$_[0]") || &er_("Can't write $_[0]");
print DB "";
close(DB);

chmod(0666,"$_[0]");
}

#
# [�Ǘ�����]
#
sub Edit {
&hed_;
$html.=<<_EDIT_;
<form action="$cgi_f" method=$met>
-�F��-<br>
<input type=hidden name=mode value=del>
Pass/<input type=password name=pass size=8><br>
<input type=submit value="�F��">
</form>
_EDIT_
&foot_;
}
