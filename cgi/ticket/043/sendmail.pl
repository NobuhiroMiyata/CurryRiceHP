#////////////////////////////////////////////////////////////////#
#                   sendmail.pl for �ɂӂ��[
#////////////////////////////////////////////////////////////////#
# ���� �F perl sendmail.pl [-itfr] [address]

#�z�z���F http://wan.magical.gr.jp
#////////////////////////////////////////////////////////////////#
# �ݒ�(���[����M�ݒ�Ɠ���ID��PASS���L��)

$user = 'curryrice';         # �ɂӂ��[�p���[�U�[�h�c
$pass = 'curry1012';         # �ɂӂ��[�p�ς���[��(���[����M�p)

$logs = 0 ;                 # 1 = �G���[���O�̍쐬


#////////////////////////////////////////////////////////////////#
# �^�C���A�E�g����(10�b�łn�j�H)

$SIG{"ALRM"} = sub {&error('#Error#�^�C���A�E�g�I')};
alarm 10;


#////////////////////////////////////////////////////////////////#
# �e�T�[�o�[�h�o�A�h���X(�ύX���ꂽ��Ǝ������ŏ����Ȃ�������)

$smtp = "mbe.nifty.com";    # smtp�T�[�o�[�̂h�o���ǂꂷ
$pop3 = "mbe.nifty.com";    # pop3�T�[�o�[�̂h�o���ǂꂷ
$from = $user . 'curryrice@mbe.nifty.com';# �ɂӂ��[�p���[���A�h���X


#////////////////////////////////////////////////////////////////#
# POP before SMTP �΍�

&pop3;


#////////////////////////////////////////////////////////////////#
# �R�}���h���C��������͏���

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
# ���[���{���̎�M

while(<>){
	last if !$P{i} && /^\.\x0D?\x0A/;
	s/^\./../;
	$mail .= $_;
	@head = split(/\x0D?\x0A/,$mail) if ! @head && /^\x0D?\x0A/;
}


#////////////////////////////////////////////////////////////////#
# �w�b�_�̉�� // -t ���M��̒��o/BCC�폜/From��������/Bcc�폜

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
$from =~ /^.+\@.+\..+$/ || &error("#Error#from���[���A�h���X���s���ł��B$from");
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
# �ŏI�`�F�b�N

$ENV{'SERVER_NAME'} = $smtp unless $ENV{'SERVER_NAME'};
&error('#Error#���M���A�h���X������܂���') unless $from;
&error('#Error#���M��A�h���X������܂���') unless $tos;


#////////////////////////////////////////////////////////////////#
# ���[�����M / �I��

$sock_addr = pack('S n a4 x8',2,25,pack("C4",split(/\./,$smtp)));
socket(SOCK, 2, 2, 6) || &error('#Error#socket�֐��ŃG���[���������܂����B');
connect(SOCK, $sock_addr) || &error('#Error#connect�֐��ŃG���[���������܂����B');
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
# �G���[���� (sendmail.log�t�@�C���ɏ����o��)

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
# �����`�F�b�N

sub check{
	@a = @_;
	$res = <SOCK>;
	$res =~ /^\Q$a[0]/ || &error("#Error#$a[1]�T�[�o�[����̂��Ԏ����ւ�ł��B\n\t$res");
}


#////////////////////////////////////////////////////////////////#
# POP3����

sub pop3{
	$sock_addr = pack('S n a4 x8',2,110,pack("C4",split(/\./,$pop3)));
	socket(SOCK, 2, 2, 6) || &error('#Error#socket�֐��ŃG���[���������܂����B');
	connect(SOCK, $sock_addr) || &error('#Error#connect�֐��ŃG���[���������܂����B');
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
�����F 2000/11/20 Ver 0.00 ���M�m�F
       2000/11/21 Ver 0.01 sendmail.log
