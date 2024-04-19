// JavaScript validation logic
function validateTeamID() {
    // Check if Team ID field is empty
    var teamID = $('#team-id').val();
    if (teamID.trim() === '') {
        alert('Please fill out the Team ID field.');
        return false;
    } else {
        $('#error-message').text(''); // Clear error message if there was one
        return true;
    }
}

$(document).ready(function() {
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
        const questionsContainer = document.getElementById("options");
        questionsContainer.innerHTML = "";

        questions.forEach((question, index) => {
            const questionCard = document.createElement("div");
            questionCard.classList.add("question-card");

            const questionText = document.createElement("p");
            questionText.classList.add("question-text");
            questionText.textContent = question.question;
            questionCard.appendChild(questionText);

            const answerInput = document.createElement("input");
            answerInput.classList.add("answer-input");
            answerInput.placeholder = "Type your answer here...";
            questionCard.appendChild(answerInput);

            questionsContainer.appendChild(questionCard);
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
        const teamIdInput = document.getElementById("team-id");
        if (teamIdInput.value.trim() === "") {
            teamIdInput.setCustomValidity("Please fill out this field."); // Show custom error message
            teamIdInput.reportValidity(); // Display the error message
            return;
        }

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
        console.log("Total time taken: " + totalTimeTaken);
    
        // Calculate the number of correct answers
        let correctAnswers = 0;
        const answerInputs = document.querySelectorAll(".answer-input");
        answerInputs.forEach((input, index) => {
            const userAnswer = input.value.trim().toLowerCase();
            if (userAnswer === questions[index].correctAnswer.toLowerCase()) {
                correctAnswers++;
            }
        });
    
        console.log("Correct answers: " + correctAnswers);
    
        // Calculate the purse value based on correct answers and time taken
        let purseValue = 40 + correctAnswers * 10; // Start with default value and add bonus for correct answers
        purseValue = Math.min(100, purseValue); // Ensure purse value does not exceed 100
    
        // Adjust purse value based on time taken
        const maxTime = 1800; // 30 minutes in seconds
        const timeFactor = 1 - (totalTimeTaken / maxTime); // Calculate the factor based on time taken
        purseValue *= timeFactor; // Adjust purse value based on time taken
        purseValue = Math.round(Math.max(40, purseValue)); // Ensure purse value is at least 40
    
        console.log("Purse value: " + purseValue);
    
        // Send data to the backend for storage
        const formData = new FormData();
        formData.append('correct_answers', correctAnswers);
        formData.append('purse_value', purseValue);
        formData.append('team_id', document.getElementById("team-id").value); // Get the team ID from the input box
    
        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken // Include the CSRF token in the headers
            }
        })
        .then(response => response.json())
        .then(data => {
            // Handle success
            console.log(data);
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
        });
    
        // Clear the quiz container
        const quizContainer = document.querySelector(".quiz-container");
        quizContainer.innerHTML = "";
    
        // Display the message
        const messageElement = document.createElement("div");
        messageElement.textContent = `Submitted successfully!\nCorrect answers: ${correctAnswers}\nTime taken: ${totalTimeTaken} seconds\nPurse value: ${purseValue}`;
        messageElement.classList.add("submitted-message"); // Add CSS class
        quizContainer.appendChild(messageElement);
    }

    // Enable the start button when a team ID is entered
    document.getElementById("team-id").addEventListener("input", function() {
        const startButton = document.getElementById("start-btn");
        if (this.value.trim() !== "") {
            startButton.disabled = false;
        } else {
            startButton.disabled = true;
        }
        // Remove the custom validation message when the input is changed
        this.setCustomValidity("");
    });

    // Enable form submission when Enter key is pressed in the team ID input
    document.getElementById("team-id").addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent form submission
            showQuestionsAndStartTimer(); // Start the quiz
        }
    });

    // Start the quiz when the start button is clicked
    document.getElementById("start-btn").addEventListener("click", showQuestionsAndStartTimer);

    // Submit the quiz when the submit button is clicked
    document.getElementById("submit-btn").addEventListener("click", submitQuiz);
});