document.addEventListener("DOMContentLoaded", function() {
    const timerElement = document.createElement("div"); // Declare timerElement globally
    let startTime, timerInterval;

    const questions = [
        {
            question: "What is the capital of France?",
            options: ["Paris", "London", "Berlin", "Rome"],
            correctAnswer: "Paris"
        },
        {
            question: "What is the largest planet in our solar system?",
            options: ["Earth", "Mars", "Jupiter", "Saturn"],
            correctAnswer: "Jupiter"
        }
        // Add more questions as needed
    ];

    function displayQuestions() {
        const optionsContainer = document.getElementById("options");
        optionsContainer.innerHTML = "";

        questions.forEach((question, index) => {
            const questionCard = document.createElement("div");
            questionCard.classList.add("question-card");

            const questionText = document.createElement("p");
            questionText.classList.add("question-text");
            questionText.textContent = question.question;
            questionCard.appendChild(questionText);

            const optionsDiv = document.createElement("div");
            optionsDiv.classList.add("options");
            question.options.forEach(option => {
                const optionBtn = document.createElement("button");
                optionBtn.classList.add("option-btn");
                optionBtn.textContent = option;
                optionBtn.addEventListener("click", () => {
                    const optionBtns = optionBtn.parentElement.querySelectorAll(".option-btn");
                    optionBtns.forEach(btn => {
                        btn.classList.remove("clicked");
                    });
                    optionBtn.classList.add("clicked");
                });
                optionsDiv.appendChild(optionBtn);
            });
            questionCard.appendChild(optionsDiv);

            optionsContainer.appendChild(questionCard);
        });
    }

    function startTimer() {
        startTime = new Date();
        timerInterval = setInterval(updateTimer, 1000);
    }

    function updateTimer() {
        const currentTime = new Date();
        const timeDifference = Math.round((currentTime - startTime) / 1000); // Time difference in seconds

        const minutes = Math.floor(timeDifference / 60);
        const seconds = timeDifference % 60;

        timerElement.textContent = minutes + ":" + (seconds < 10 ? "0" : "") + seconds; // Update timer display
    }

    function showQuestionsAndStartTimer() {
        displayQuestions();
        startTimer();
        document.querySelector(".container").style.display = "none"; // Hide container with title and start button
        document.querySelector(".quiz-container").style.display = "block"; // Show quiz container

        // Append the timer element to the quiz container
        timerElement.id = "timer";
        timerElement.textContent = "0:00";
        timerElement.style.fontSize = "24px";
        timerElement.style.fontWeight = "bold";
        timerElement.style.textAlign = "right";
        timerElement.style.marginTop = "20px";
        timerElement.style.marginRight = "20px"; // Add margin-right
        const quizContainer = document.querySelector(".quiz-container");
        quizContainer.insertBefore(timerElement, quizContainer.firstChild); // Insert timer as first child

        document.getElementById("submit-btn").style.display = "block"; // Display the submit button
    }

    function submitQuiz() {
        clearInterval(timerInterval);
        const endTime = new Date();
        const totalTimeTaken = Math.round((endTime - startTime) / 1000); // Total time taken in seconds
        console.log("Total time taken: " + totalTimeTaken + " seconds");

        // Clear the quiz container
        const quizContainer = document.querySelector(".quiz-container");
        quizContainer.innerHTML = "";

        // Display the message
        const messageElement = document.createElement("div");
        messageElement.textContent = `Submitted successfully!\nTime taken: ${totalTimeTaken} seconds`;
        messageElement.classList.add("submitted-message"); // Add CSS class
        quizContainer.appendChild(messageElement);

        // Send totalTimeTaken to backend for storage
    }

    window.onload = () => {
        document.getElementById("start-btn").addEventListener("click", showQuestionsAndStartTimer);
        document.getElementById("submit-btn").addEventListener("click", submitQuiz);
    };
});
