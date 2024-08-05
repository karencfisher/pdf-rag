const questionButton = document.getElementById('question-button');
const questionText = document.getElementById('question');
const answerDiv = document.getElementById('answer');

questionButton.addEventListener("click", async () => {
    const query = questionText.value;
    if (query === "") {
        answerDiv.innerHTML = "<span style=\"color: red\">Need to ask a question!</span>";
        questionText.focus();
        return;
    }
    const url = `/query?question=${query}`;
    answerDiv.innerHTML = "<span style=\"color: red\">Waiting for response. This may take a moment.</span>";
    document.body.style.cursor = 'wait';

    try {
        response = await fetch(url);
        const answer = await response.json();
        if (!response.ok) {
            const errorText = answer.error;
            throw new Error(`Something went wrong<br>Response status: ${response.status}<br>${errorText}`)
        }
        const htmlContent = marked.parse(answer.answer);
        answerDiv.innerHTML = htmlContent;
    }
    catch(error) {
        answerDiv.innerHTML = `<span style=\"color: red\">${error.message}</span>`;
    }
    answerDiv.focus();
    document.body.style.cursor = 'default';
});

const clearButton = document.getElementById('clear-button');
clearButton.addEventListener("click", () => {
    questionText.value = "";
});

addEventListener("load", () => {
    questionText.focus();
});
