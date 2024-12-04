let passwordSet = false; // 비밀번호 입력이 완료되었는지 여부를 체크하는 플래그

// 비밀번호 일치 여부 확인 함수
function checkPasswordMatch() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var message = document.getElementById("passwordMessage");

    if (password === confirmPassword && confirmPassword !== "") {
        message.textContent = "비밀번호가 일치합니다.";
        message.classList.remove("mismatch");
        message.classList.add("match");
    } else {
        message.textContent = "비밀번호가 일치하지 않습니다.";
        message.classList.remove("match");
        message.classList.add("mismatch");
    }
}

// 비밀번호 입력란의 값이 첫 번째로 입력될 때만 실행
function onPasswordChange() {
    // 첫 번째 입력 후 비밀번호 입력 상태를 설정
    if (!passwordSet) {
        passwordSet = true;
        return; // 첫 입력은 그냥 지나가도록 함
    }
    // 이후 비밀번호 수정 시, 비밀번호 확인란을 비워놓고 메시지를 초기화
    document.getElementById("confirmPassword").value = "";
    document.getElementById("passwordMessage").textContent = "";
}

// 비밀번호 확인란의 값이 변경될 때만 실행
function onConfirmPasswordChange() {
    checkPasswordMatch(); // 비밀번호 확인란이 수정될 때마다 검증
}

function handleSubmit(event) {
    event.preventDefault(); // 폼 제출 후 페이지 리로드 방지

    // 폼 데이터를 객체로 수집
    const formData = new FormData(event.target);
    const data = {};
    const temp = [];
    formData.forEach((value, key) => {
        if (key == 'hobby') {                                   
            temp.push(value)
            data[key] = temp 
        }                                   
        else 
            data[key] = value;              

    });

    // 데이터를 localStorage에 저장
    localStorage.setItem('formData', JSON.stringify(data));

    // 결과 페이지로 리디렉션
    window.location.href = 'output.html'; // 결과를 출력할 페이지
}

// login.html
function handleLogin(event) {
    event.preventDefault(); // 폼 제출 후 페이지 리로드 방지

    // 폼 데이터 수집
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // 로컬 스토리지에서 저장된 데이터 가져오기
    const storedData = JSON.parse(localStorage.getItem('formData'));

    // 이메일과 비밀번호 확인
    if (storedData && storedData.email === email && storedData.password === password) {
        // 로그인 성공
        window.location.href = 'welcome.html'; // 로그인 후 이동할 페이지
    } else {
        // 로그인 실패
        document.getElementById("loginErrorMessage").textContent = "이메일 또는 비밀번호가 일치하지 않습니다.";
    }
}

// welcome.html 
// 로그아웃 기능
 function handleLogout() {
    localStorage.removeItem('formData'); // 로컬 스토리지에서 데이터 삭제
    window.location.href = 'sigin.html'; // 로그인 페이지로 리디렉션
}