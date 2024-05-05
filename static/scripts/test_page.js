document.querySelector("#answer-btn").addEventListener('click', (e) => {
    const answer = e.target.parentNode.querySelector('input[name="answer"]:checked').value;
    const answer_div = document.querySelector("#answer-div");
    const next_btn = document.querySelector("#next");
    const get_results = document.querySelector("#get-results");

    let xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://127.0.0.1:9999/check_answer/');
    xhr.responseType = 'json';
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*")
    xhr.send(JSON.stringify({ answer: answer }));
    xhr.onload = function () {
        if (xhr.status == 200) {
            if (xhr.response["status"] == 'ok') {
                answer_div.innerHTML = "Правильный ответ";
                answer_div.classList.add("alert-success");
            }
            else {
                if (xhr.response['correct_answers'].length == 1) {
                    answer_div.innerHTML = `Неправильный ответ. Правильный ответ: ${xhr.response['correct_answers']}`;
                }
                else {
                    answer_div.innerHTML = `Неправильный ответ. Правильные ответы: ${xhr.response['correct_answers']}`;
                }
                answer_div.classList.add("alert-danger");
            }
            answer_div.hidden = false;
            next_btn.disabled = false;
            get_results.disabled = false;
            e.target.disabled = true;
        }
        else {
            console.log('not 200');
        }
    };
})

document.querySelector("#next").addEventListener('click', (e) => {
    location.href = 'http://127.0.0.1:9999/test/';
})

document.querySelector("#get-results").addEventListener('click', (e) => {
    location.href = 'http://127.0.0.1:9999/test_results/';
})