##�`�P�b�g�\��t�H�[�� �ݒ�t�@�C���@2002/03/03
## -------------------------------------------------------------------
## ���̃X�N���v�g�݂͂̃m�[�g������seo���������܂����B
$MKNAME  = '�݂̃m�[�g';        # v1.0 1999/10/12
$MKURL   = 'http://www.mino.net/cgi/';
## ���̃X�N���v�g���g�p���������Ȃ鑹�Q����҂͂��̐ӂ𕉂��܂���B
## -------------------------------------------------------------------
## -------------------------------------------------------------------
## --- ��{�ݒ� �C�ӂɏC�� [*]���ڂ͔C�� �ȗ�����ꍇ''
## -------------------------------------------------------------------

$MGRPASS = 'curry1012';		# �Ǘ��p�X���[�h���K���ύX

# �e�t�@�C�����̐ݒ�
$MENUCGI = './form.cgi';	# ���[���t�H�[���b�f�h
$MAILCGI = './mail.cgi';	# ���[�����M�b�f�h
$MGRCGI  = './mgr.cgi';		# �Ǘ�&�w���v��ʂb�f�h
$FILEDIR = './';		# �e��t�@�C���i�[�f�B���N�g��
$LSTFILE = 'day.dat';		# �����f�[�^�ꗗ�t�@�C������������
$LOCKFILE= 'day.loc';		# ���b�N�t�@�C������������

# ���[���ݒ�
$sendmail = '/usr/sbin/sendmail'; #sendmail�̃p�X �v���o�C�_�Ɋm�F���邱��
$admin_email = 'info@gekidan-curryrice.com';	# �Ǘ��҃��[���A�h���X
					# ���q�l�ɒʒm����܂��B
$send_email = 'uchuzine@gmail.com';	# ��ȊO�̑��t�惁�[���A�h���X�A�q�ւ̒ʒm�Ȃ�
					# �����ݒ肷��Ƃ��̓J���}(,)�ł�����

# �\��f�[�^�i�[�t�@�C���ݒ�
$csvmode = '1';		# 0->�S�f�[�^��1�t�@�C���ɁB1->�������ƂɃt�@�C������
			# ��read.cgi���g���ꍇ�́A1�ɂ��邱�ƁB
$csvf = 'yoyaku.csv';	# 0�̏ꍇ�K�v�B�\�����O�t�@�C�������������A�K�����O�ύX
$csvd = './log/';	# 1�̏ꍇ�K�v�B�\�����O�i�[�ꏊ�̃p�X
			# ���p�[�~�b�V����707�ɂč쐬�A�K�����O�ύX

# ��ʂ̐ݒ�
$TITLE   = '�\��\���݃t�H�[��';# �y�[�W�^�C�g��

$BGGIF   = '';	# �w�i�摜[*]
$BGCOLOR = '#FFFFFF';	# �w�i�F[*]
$FGCOLOR = '#333333';	# �����F
$LINK    = '#0000FF';	# LINK�F
$VLINK   = '#FF0000';	# VLINK�F
$ALINK   = '#00FF00';	# ALINK�F
$BASURL  = 'http://gekidan-curryrice.com/';	# ���Ȃ���HP�̃A�h���X
$HEADMSG = 		# �y�[�W�w�b�_�[���b�Z�[�W[*]
'��������̂��\���݂͂����炩��';

$zan= '100';		# �`�P�b�g�����̖����ȉ��ɂȂ�����c���\��
			# �\���������Ȃ��ꍇ��0

$end= '6';		# �J��$end���ԑO�ɂȂ������t�I��
			# ���������؂�̂āB13��30���J���̏ꍇ�́A2����͂����11��00���I���B
			# �����O���ɏI�����ő�ݒ�i�������Ԉȏ�̐������́j

$MGRFLG  = 'ON';	# �Ǘ��t���O�i�Ǘ��{�^���L�^���j
	
## ���j���[�̐ݒ�
$SORTFLG = 1;		# �\������
			#   0:���t�̐V�������̂���
			#   1:���t�̌Â����̂���
			#   2:�`�P�b�g�c���̏��Ȃ����̂���

## --- ��{�ݒ� �����܂�
$BCKURL  = "$MENUCGI";	# ���j���[��ʈȊO����̃o�b�N�t�q�k

## -------------------------------------------------------------------
## �p�b�P�[�W�E���C�u�����錾
## -------------------------------------------------------------------
package Com;
## -------------------------------------------------------------------
## �������
## -------------------------------------------------------------------
sub getagv {
	if ($ENV{'REQUEST_METHOD'} eq 'POST') {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else {
		$buffer = $ENV{'QUERY_STRING'};
	}
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/\r//g;
		$value =~ s/<!--(.|\n)*-->//g;	#SSI 	����(�Z�L�����e�B�΍�)
		$value =~ s/applet//gi;		#Java		����(�Z�L�����e�B�΍�)
		$value =~ s/<script//gi;		#Javascript	����(�Z�L�����e�B�΍�)
		$value =~ s/<META(.+)Refresh(.*)>(\s*)(\n?)//ig; #META�^�O��΂��֎~
		$value =~ s/<(.*)style(\s*)=(.|\n)*>//ig;        #Style�^�O�֎~
		&jcode'convert(*value, 'sjis');
		$FORM{$name} = $value;
	}
}
## -------------------------------------------------------------------
## ���X�g�擾�����T�u���[�`��
## -------------------------------------------------------------------
sub GetList {
	local($lfile,$flg,*list,*msg) = @_;
	@list = ();
	if ( open( FP,$lfile ) ) {
		while ( <FP> ) {
			chop $_;
			$line = $_;
			&jcode'convert(*line, 'sjis');
			if ( $flg == 2 ) {
				( $file,$title,$name ) = split( /,/,$line );
				$line = "$title,$file,$name";
			}
			push( @list,$line );
		}
		close( FP );
	}
	if ( $#list < 0 ) {
		$msg = '���݂��\���݂��󂯕t���Ă���܂���B';
		return 1;
	}
	@list = sort( @list );
	if ( $flg == 0 ) { @list = reverse( @list ); }
	if ( $flg == 2 ) {
		@list2 = ();
		foreach $line ( @list ) {
			( $title,$file,$name ) = split( /,/,$line );
			$line = "$file,$title,$name";
			push( @list2,$line );
		}
		@list = @list2;
	}
	return 0;
}
## -------------------------------------------------------------------
## �{���\�������T�u���[�`��
## -------------------------------------------------------------------
sub GetData {
	local($lfile,*msg) = @_;
	$msg = '';
	if ( open( FP,$lfile ) ) {
		while ( <FP> ) {
			$msg = "$msg$_";
		}
		close( FP );
	}
	&jcode'convert(*msg, 'sjis');
}
## -------------------------------------------------------------------
## ���b�N�����T�u���[�`��
## -------------------------------------------------------------------
sub lockon {
	local($lfile) = @_;
	$lckkey = 0;
	foreach (1 .. 5) {
		unless (-e "$lfile") {
			open(LOCK,">$lfile");
			close(LOCK);
			$lckkey = 9;
			last;
		} else { sleep(1); }
	}
	if ($lckkey == 0) { return 0; }
	return 9;
}
## -------------------------------------------------------------------
## �A�����b�N�����T�u���[�`��
## -------------------------------------------------------------------
sub lockoff {
	local($lfile,$key) = @_;
	if ($key == 9) { unlink("$lfile"); }
}
1;

