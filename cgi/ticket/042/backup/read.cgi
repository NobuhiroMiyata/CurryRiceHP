#!/usr/bin/perl

require './jcode.pl';
require './cfg.cgi';
##チケット予約フォーム 一覧表示CGI　2002/03/03
## -------------------------------------------------------------------
## このスクリプトは以下のスクリプトを元にseoが改造しました。
## これを使うにはcfg.cgiの$csvmodeを1に設定してください。
#----------------------------
$ver="BBS-i v3.3";
# (i-mode向け簡易掲示板/日記)
#----------------------------
# Copyright(C) りゅういち
# E-Mail:ryu@cj-c.com
# W W W :http://www.cj-c.com/

#-- 設定ファイル -------------*

$met  = "POST";			# 送信形式(POST or GET(J-Skyの場合自動的にGETになります))
$pass = "curry1012";			# 管理用のパスワード※要変更
$a_max= 10;			# 1ページ表示件数

$cgi_f= "./read.cgi";		# このファイル

$lockf= "./bi.loc";		# ロックファイル(使用は17行目に依存)

# アクセス対象は?
# => (0=とくに無し 1=J-Sky 2=i-mode 3=ドットi 4=J-Sky及びi-mode及びドットi)
$access= 0;

#--- 設定ここまで---------------*
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
	if($access==1 && $j_==0){&er_("J-Sky端末でｱｸｾｽしてください!");}
	elsif($access==2 && $i_==0){&er_("i-mode端末でｱｸｾｽしてください!");}
	elsif($access==3 && $a_==0){&er_("ﾄﾞｯﾄi端末でｱｸｾｽしてください!");}
	elsif($access==4 && $a_==0 && $i_==0 && $j_==0){&er_("i-mode/J-Sky/ﾄﾞｯﾄi端末でｱｸｾｽして下さい!");}
}
&html_;
#
# [トップページ]
#
sub html_ {

open(LOG,"$LSTFILE") || &er_("Can't open $LSTFILE");
@lines = <LOG>;
close(LOG);

&hed_;
$html.= "\予\約一覧<hr>\n";
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
			$date = "$yy年$mm月$dd日\t$hh時$ff分開演";
		} else { $date = "不明"; }

$html.= "<input type=radio name=log value=$yy$mm$dd$hh$ff>\n";
$html.= "$date\t\t<font color=red>\n";

if ( $mai <= 0 ) {
$html.=  "販売終了\n";
}else{
$html.=  "残り$mai枚\n";}
$html.=  "</font><br>\n";

}

$html.= <<"_HTML_";
<input type=hidden name=mode value=del>
<input type=password name=pass size=6>
<input type=submit value="表\示"><br>
</form></div>
_HTML_
	&foot_;
}
#
# [ヘッダ表示]
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
# [フッタ表示]
#
sub foot_ {
	$html.= <<"_HTML_";
<hr><!--著作権表\示 削除不可-->
<a href="http://www.cj-c.com/i/" target=_top>BBS-i</a>
_HTML_
	$html.= "</body></html>\n";
	&htmlp;
}
#
# [フォームなどのデコード]
#
sub d_code_ {
if($ENV{'REQUEST_METHOD'} eq "POST"){
	if ($ENV{'CONTENT_LENGTH'} > 10000) { &er_("文章があまりに長すぎます!"); }
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
# [管理用ページ]
#
sub del_ {
if ($FORM{'pass'} ne "$pass") { &er_("パスワードが違います!"); }

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
			$date = "$yy年$mm月$dd日\t$hh時$ff分開演";
		} else { $date = "不明"; }

&hed_;
$html.= "<center>\n";
$html.= "$date\n";

$html.= <<"_HTML_";
<hr>
[<a href="$cgi_f">戻</a>]
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
$html.= "<tr><td>$name</td><td>$mai枚</td><td>$tel</td><td>$biko</td><td>$date_now</td></tr>\n";
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
# [エラー表示]
#
sub er_ {
if (-e $lockf) { unlink($lockf); }
	&hed_;
	$html.= "<center>[<a href=\"$cgi_f?no=$no\">戻</a>]<br>ERROR<br>$_[0]</center>\n";
	&foot_;
}

#
# [書き出し]
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
# [ログ生成]
#
sub l_m {
open(DB,">$_[0]") || &er_("Can't write $_[0]");
print DB "";
close(DB);

chmod(0666,"$_[0]");
}

#
# [管理入室]
#
sub Edit {
&hed_;
$html.=<<_EDIT_;
<form action="$cgi_f" method=$met>
-認証-<br>
<input type=hidden name=mode value=del>
Pass/<input type=password name=pass size=8><br>
<input type=submit value="認証">
</form>
_EDIT_
&foot_;
}
