#////////////////////////////////////////////////////////////////#
#                   sendmail.pl for にふちー
#////////////////////////////////////////////////////////////////#
# 書式 ： perl sendmail.pl [-itfr] [address]

#配布元： http://wan.magical.gr.jp
#////////////////////////////////////////////////////////////////#
# 設定(メール受信設定と同じIDとPASSを記入)

$user = 'curryrice';         # にふちー用ユーザーＩＤ
$pass = 'curry1012';         # にふちー用ぱすわーど(メール受信用)

$logs = 0 ;                 # 1 = エラーログの作成


#////////////////////////////////////////////////////////////////#
# タイムアウト処理(10秒でＯＫ？)

$SIG{"ALRM"} = sub {&error('#Error#タイムアウト！')};
alarm 10;


#////////////////////////////////////////////////////////////////#
# 各サーバーＩＰアドレス(変更されたら独自調査で書きなおす事♪)

$smtp = "mbe.nifty.com";    # smtpサーバーのＩＰあどれす
$pop3 = "mbe.nifty.com";    # pop3サーバーのＩＰあどれす
$from = $user . 'curryrice@mbe.nifty.com';# にふちー用メールアドレス


#////////////////////////////////////////////////////////////////#
# POP before SMTP 対策

&pop3;


#////////////////////////////////////////////////////////////////#
# コマンドライン引数解析処理

$p="rf";

while($_ = shift @ARGV){
	if(s/^-(.)(.*)/$2 ne "" && "-$2"/e){
		if(index($p,$1) >= 0){
			$P{$1} = $2 ne "" ? $2 : shift @ARGV;
		}else{
			$P{$1} = 1;
			redo;
		}
	}else{
		push(@tos,$_) if /^.+\@.+\..+$/;
	}
}


#////////////////////////////////////////////////////////////////#
# メール本文の受信

while(<>){
	last if !$P{i} && /^\.\x0D?\x0A/;
	s/^\./../;
	$mail .= $_;
	@head = split(/\x0D?\x0A/,$mail) if ! @head && /^\x0D?\x0A/;
}


#////////////////////////////////////////////////////////////////#
# ヘッダの解析 // -t 送信先の抽出/BCC削除/From書換処理/Bcc削除

foreach $i (0..$#head){
	if($head[$i] =~ /^([A-Z].*?)\s*:/){
		$HEAD{($n = $1)} = $head[$i];
		$HEAD{$n} .= $head[++$i] if $head[$i + 1] =~ /^\s/;
	}
}
$from = $P{'f'} if $P{'f'};
if($P{"t"}){
  $to = $HEAD{"To"};
  $cc = $HEAD{"Cc"};
 $bcc = $HEAD{"Bcc"};
}
$from =~ /^.+\@.+\..+$/ || &error("#Error#fromメールアドレスが不正です。$from");
for($from,$to,$cc,$bcc){
	s/^(?:To|Bcc|Cc|From)\s*:\s*//;
	s/"(?:[^"]|\")*"//g;
	1 while s/\([^()]*\)//g;
}
if($P{"t"}){
	 @to = split(/,/,$to);
	 @cc = split(/,/,$cc);
	@bcc = split(/,/,$bcc);
}
for($from,@to,@cc,@bcc,@tos){
	$_ = $1 if /<([^>]*)>/;
	s/^[\s\x0D\x0A]+|[\s\x0D\x0A]+$//g;
	undef $_ unless /^.+\@.+\..+$/;
	$tos++;
}
$mail =~ s/Bcc\s*:(?:\s+[^\x0D\x0A]*\x0D?\x0A)+//;
$mail =~ s/From\s*:(?:\s+[^\x0D\x0A]*\x0D?\x0A)+/From: $from\x0D\x0A/; 
#////////////////////////////////////////////////////////////////#
# 最終チェック

$ENV{'SERVER_NAME'} = $smtp unless $ENV{'SERVER_NAME'};
&error('#Error#送信元アドレスがありません') unless $from;
&error('#Error#送信先アドレスがありません') unless $tos;


#////////////////////////////////////////////////////////////////#
# メール送信 / 終了

$sock_addr = pack('S n a4 x8',2,25,pack("C4",split(/\./,$smtp)));
socket(SOCK, 2, 2, 6) || &error('#Error#socket関数でエラーが発生しました。');
connect(SOCK, $sock_addr) || &error('#Error#connect関数でエラーが発生しました。');
select(SOCK);$|=1;select(STDOUT);
&check(220,"SMTP");
for("HELO $ENV{'SERVER_NAME'}","MAIL FROM:<$from>"){
	print SOCK $_ , "\r\n";
	&check(250,"SMTP($_)");
}
foreach $head (@to,@cc,@bcc,@tos){
	next unless $head;
	print SOCK "RCPT TO:<$head>\r\n";
	&check(25,"SMTP(RCPT TO: <$head>)");
}

print SOCK "DATA\r\n";
&check(354,"SMTP");

print SOCK "$mail\r\n.\r\n";
&check(250,"SMTP");

print SOCK "QUIT\r\n";
close (SOCK);
alarm 0;
exit;


#////////////////////////////////////////////////////////////////#
# エラー処理 (sendmail.logファイルに書き出し)

sub error{
	@a=@_;
	print SOCK "QUIT\r\n";
	close(SOCK);
	if($logs && open(OUT,">> sendmail.log")){
		$a[0] =~ s/\r?\n//g;
		($sec,$min,$hour,$day,$mon)=localtime(time);$mon++;
		@d=("00".."59");
		print OUT "[$d[$mon]/$d[$day] $d[$hour]:$d[$min]:$d[$sec]] $a[0]\n";
		close(OUT);
	}
	exit;
}


#////////////////////////////////////////////////////////////////#
# 応答チェック

sub check{
	@a = @_;
	$res = <SOCK>;
	$res =~ /^\Q$a[0]/ || &error("#Error#$a[1]サーバーからのお返事がへんです。\n\t$res");
}


#////////////////////////////////////////////////////////////////#
# POP3処理

sub pop3{
	$sock_addr = pack('S n a4 x8',2,110,pack("C4",split(/\./,$pop3)));
	socket(SOCK, 2, 2, 6) || &error('#Error#socket関数でエラーが発生しました。');
	connect(SOCK, $sock_addr) || &error('#Error#connect関数でエラーが発生しました。');
	select(SOCK);$|=1;select(STDOUT);
	print SOCK "USER $user\r\n";
	&check("+OK","POP3");
	print SOCK "PASS $pass\r\n";
	&check("+OK","POP3");
	print SOCK "QUIT\r\n";
	&check("+OK","POP3");
	close(SOCK);
}

__END__
履歴： 2000/11/20 Ver 0.00 送信確認
       2000/11/21 Ver 0.01 sendmail.log
