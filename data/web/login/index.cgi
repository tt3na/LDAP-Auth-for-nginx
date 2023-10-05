#!/bin/bash -vx

homd=/home/abc
sesd=$homd/session
logd=$homd/log
tmp=/tmp/tmp_$$

# logfile=LOG.${HOSTNAME}.$(basename $0)_$(date +%Y%m%d%H%M%S)_$$
# exec 2>$logd/$logfile

ERROR_HOLDER(){
	echo "Content-type: text/html; charset=UTF-8"
	echo ""
	echo "error"
	rm -rf $tmp-*
	exit 1	
}

trap ERROR_HOLDER ERR
set -o pipefail

echo "Content-type: text/html"
echo ""
cat << FIN
<!DOCTYPE html>
<html>
	<head>
		<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0">
		<meta charset="UTF-8" />
		<title>ログイン</title>
		<script>
			const postURL = (url,formId) => {
				var form = document.getElementById(formId);
				form.action = url;
				form.method = "POST";
				form.submit();
			}
		</script>
		<style>
			*{
				padding: 0;
				margin: 0;
			}
			
			body{
				font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif;
				font-weight: 350;
			}

			label{
				font-size: 1.1rem;
			}
			
			.input-form{
				position: absolute;
				top: 40%;
				left: 50%;
				transform: translate(-50%,-50%);
				background-color: #E8E8E8;
				padding: 20px 20px 15px 20px;
				border-radius: 5px;
			}

			input{
				display: block;
				width: 300px;
				height: 35px;
				margin-top: 2px;
				border-radius: 4px;
				border: 1px #dfdfdf solid;
				font-size: 1.0rem;
			}

			input:autofill{
				background: #fff;
			}

			.sendBtn{
				margin-top:10px;
				height: 35px;
				width: 305px;
				color: #FFFFFF;
				border: 0px;
				border-radius: 3px;
				font-size: 1rem;
				font-weight: 400;
				vertical-align: middle;
				background-color: #3A6EA5;
				box-shadow: 0px 4px 0px 0px rgb(19, 61, 74);
				cursor: pointer;
			}

			@media screen and (max-width: 980px) {
				label{
					font-size: 1.3rem;	
				}
				input{
					width: 250px;
					height: 40px;
					border: 2px #dfdfdf solid;
					font-size: 1.5rem;	
				}
				.password{
					margin-bottom: 20px;
				}
				.sendBtn{
					margin-top: 15px;
					width: 100%;
					height: 45px;
					font-size: 1.4rem;
					border-radius: 6px;
					box-shadow: 0px 4px 0px 0px rgb(19, 61, 74);
				}
			}

			.user{
				margin-bottom: 7px;
			}

			.sendBtn:hover{
				filter: brightness(1.15);
			}
		</style>
	</head>
	<body>
		<div class="input-form">
			<form id="FORM" method="POST">
				<label for="user">ユーザーID</label>
				<input class="user" id="user" type="text" style="padding-left:5px;" name="USER" />
				<label for="pass" id="label_pass">パスワード</label>
				<input class="pass" id="pass" type="password" style="padding-left:5px;" name="PASSWORD" />
			</form>
			<button class="sendBtn" type="button" onclick="postURL('/login/login_check.cgi','FORM')">ログイン</button> 
			<small style="display:block;margin-top:10px;text-align:right;">LDAP Auth</small>
		</div>
	</body>
</html>
FIN


rm -rf $tmp-*
exit 0
