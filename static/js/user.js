let mainButton = document.getElementById("mainPage");
mainButton.href = `/?token=${getCookie('login_token')}&email=${getCookie('email')}`