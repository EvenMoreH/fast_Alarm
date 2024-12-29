from fasthtml.common import * # type: ignore
from fasthtml.common import (Form, Fieldset, Label, Input, Button, Html, Head, Body, Div, P, Title, Titled, A, Link, Audio ,FileResponse)
from starlette.responses import FileResponse

# for docker
app, rt = fast_app(static_path="static") # type: ignore

# for local
# app, rt = fast_app(static_path="app/static", debug=True) # type: ignore


@rt("/")
def homepage():
    return Html(
        Head(
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Title("Fast Alarm"),
            Link(rel="stylesheet", href="styles.css"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png"),
        ),
        Body(
            Div(
                H1(
                    "Fast Alarm", cls="title",
                ),
                cls="column",
                style="margin-top: 5%",
            ),
            Div(
                Div(
                    Div(
                        H1("Timer #1", style="margin-left: 1vw"),
                        Div(
                            Div(
                                Input(type="text", name="name", id="timer-name-1", placeholder="Timer Name",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            Div(
                                Input(type="number", name="time", id="delay-time-1", placeholder="Time (minutes)",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            cls="inline",
                        ),
                    ),
                    Div(
                        Button("Start Timer #1", id="start-button-1", onclick="timer1.playAudio()"),
                        Button("Stop Timer #1", onclick="timer1.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-1", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="separator"),
                Div(
                    Div(
                        H1("Timer #2", style="margin-left: 1vw"),
                        Div(
                            Div(
                                Input(type="text", name="name", id="timer-name-2", placeholder="Timer Name",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            Div(
                                Input(type="number", name="time", id="delay-time-2", placeholder="Time (minutes)",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            cls="inline",
                        ),
                    ),
                    Div(
                        Button("Start Timer #2", id="start-button-2", onclick="timer2.playAudio()"),
                        Button("Stop Timer #2", onclick="timer2.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-2", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="separator"),
                Div(
                    Div(
                        H1("Timer #3", style="margin-left: 1vw"),
                        Div(
                            Div(
                                Input(type="text", name="name", id="timer-name-3", placeholder="Timer Name",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            Div(
                                Input(type="number", name="time", id="delay-time-3", placeholder="Time (minutes)",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            cls="inline",
                        ),
                    ),
                    Div(
                        Button("Start Timer #3", id="start-button-3", onclick="timer3.playAudio()"),
                        Button("Stop Timer #3", onclick="timer3.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-3", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="separator"),
                Div(
                    Div(
                        H1("Timer #4", style="margin-left: 1vw"),
                        Div(
                            Div(
                                Input(type="text", name="name", id="timer-name-4", placeholder="Timer Name",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            Div(
                                Input(type="number", name="time", id="delay-time-4", placeholder="Time (minutes)",
                                    style="width: clamp(150px, 20vw, 350px);"),
                            ),
                            cls="inline",
                        ),
                    ),
                    Div(
                        Button("Start Timer #4", id="start-button-4", onclick="timer4.playAudio()"),
                        Button("Stop Timer #4", onclick="timer4.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-4", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="bob"),
                cls="row",
            ),
            Div(
                Button("Start All", id="start-all-button", onclick="timers.startAll()", style="margin-top: 3rem"),
                Button("Reset All", onclick="timers.cancelAll()", style="margin-top: 3rem"),
                cls="globalButtonGrid",
            ),

            # GPT enhanced script to manage timers:
            Script(
                """
                function Timer(timerId, inputId, nameId, boxId, audioSrc, startButtonId) {
                    this.timerId = timerId;
                    this.inputId = inputId; // Time input field ID
                    this.nameId = nameId; // Name input field ID
                    this.boxId = boxId; // Countdown display box ID
                    this.startButtonId = startButtonId; // Start button ID
                    this.audioSrc = audioSrc;
                    this.countdownInterval = null;
                    this.isCancelled = false;
                    this.audio = null;

                    this.playAudio = function () {
                        var delayInput = document.getElementById(this.inputId);
                        var startButton = document.getElementById(this.startButtonId);
                        var startAllButton = document.getElementById("start-all-button");

                        var delay = parseInt(delayInput.value * 60) || 0; // Get delay in minutes
                        if (delay <= 0) return; // Skip if no valid delay is provided

                        var countdownBox = document.getElementById(this.boxId);

                        // Disable the time input, Start button, and Start All button
                        delayInput.disabled = true;
                        delayInput.style.backgroundColor = "3C3C3C"; // Grey out the input
                        startButton.disabled = true;
                        startAllButton.disabled = true;

                        // Reset cancel state
                        this.isCancelled = false;

                        // Create a new audio object
                        this.audio = new Audio(this.audioSrc);

                        // Start a countdown
                        var remainingTime = delay;
                        countdownBox.textContent = this.formatTime(remainingTime); // Initial display

                        this.countdownInterval = setInterval(() => {
                            if (this.isCancelled) {
                                clearInterval(this.countdownInterval); // Stop countdown if cancelled
                                countdownBox.textContent = "Resetting...";
                                this.stopAudio(); // Stop audio playback if playing
                                delayInput.disabled = false; // Re-enable input field
                                delayInput.style.backgroundColor = ""; // Reset style
                                startButton.disabled = false; // Re-enable Start button
                                timers.checkStartAllButton(); // Re-enable Start All button if no timer is active
                                return;
                            }

                            remainingTime -= 1;
                            if (remainingTime <= 0) {
                                clearInterval(this.countdownInterval); // Stop countdown
                                countdownBox.textContent = "Time's Up!";
                                this.audio.play(); // Play the audio
                                delayInput.disabled = false; // Re-enable input field
                                delayInput.style.backgroundColor = ""; // Reset style
                                startButton.disabled = false; // Re-enable Start button
                                timers.checkStartAllButton(); // Re-enable Start All button if no timer is active
                            } else {
                                countdownBox.textContent = this.formatTime(remainingTime); // Update display
                            }
                        }, 1000); // Update every second
                    };

                    this.cancelCountdown = function () {
                        this.isCancelled = true; // Set cancel flag
                        clearInterval(this.countdownInterval); // Stop the interval
                        this.stopAudio(); // Stop audio playback if playing

                        var delayInput = document.getElementById(this.inputId);
                        var startButton = document.getElementById(this.startButtonId);
                        var startAllButton = document.getElementById("start-all-button");

                        var countdownBox = document.getElementById(this.boxId);
                        var nameInput = document.getElementById(this.nameId);

                        countdownBox.textContent = "Resetting..."; // Update the countdown box

                        // Clear the input fields
                        delayInput.value = "";
                        nameInput.value = "";

                        // Re-enable input field and reset its style
                        delayInput.disabled = false;
                        delayInput.style.backgroundColor = "";
                        startButton.disabled = false; // Re-enable Start button
                        timers.checkStartAllButton(); // Re-enable Start All button if no timer is active

                        // Set a timeout to clear the text after 3 seconds
                        setTimeout(() => {
                            countdownBox.textContent = ""; // Clear the text
                        }, 3000); // 3000 milliseconds = 3 seconds
                    };

                    this.stopAudio = function () {
                        if (this.audio && !this.audio.paused) {
                            this.audio.pause(); // Pause the audio
                            this.audio.currentTime = 0; // Reset the audio playback position
                        }
                    };

                    this.formatTime = function (timeInSeconds) {
                        var hours = Math.floor(timeInSeconds / 3600); // Calculate hours
                        var minutes = Math.floor((timeInSeconds % 3600) / 60); // Calculate remaining minutes
                        var seconds = timeInSeconds % 60; // Get remaining seconds

                        if (hours > 0) {
                            // If time is greater than 1 hour, include hours in the format
                            return `${hours}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
                        } else {
                            // Otherwise, show only minutes:seconds
                            return `${minutes}:${seconds.toString().padStart(2, "0")}`;
                        }
                    };
                }

                // Manage multiple timers in a centralized way
                var timers = {
                    timerInstances: [],

                    addTimer: function (timer) {
                        this.timerInstances.push(timer);
                    },

                    cancelAll: function () {
                        this.timerInstances.forEach((timer) => {
                            timer.cancelCountdown();

                            // Clear all input fields
                            var delayInput = document.getElementById(timer.inputId);
                            var nameInput = document.getElementById(timer.nameId);
                            delayInput.value = "";
                            nameInput.value = "";

                            // Re-enable input field and reset its style
                            delayInput.disabled = false;
                            delayInput.style.backgroundColor = "";
                            var startButton = document.getElementById(timer.startButtonId);
                            startButton.disabled = false; // Re-enable Start button
                        });

                        // Re-enable Start All button
                        var startAllButton = document.getElementById("start-all-button");
                        startAllButton.disabled = false;
                    },

                    startAll: function () {
                        this.timerInstances.forEach((timer) => {
                            var delayInput = document.getElementById(timer.inputId);
                            if (delayInput.value.trim() !== "") {
                                timer.playAudio(); // Start the timer if input is not empty
                            }
                        });
                    },

                    checkStartAllButton: function () {
                        // Disable Start All button if any timer is running
                        var startAllButton = document.getElementById("start-all-button");
                        var anyRunning = this.timerInstances.some((timer) => timer.isCancelled === false && timer.countdownInterval !== null);
                        startAllButton.disabled = anyRunning;
                    },
                };

                // Initialize timers
                var timer1 = new Timer("timer1", "delay-time-1", "timer-name-1", "countdown-box-1", "/static/sound/alarm.mp3", "start-button-1");
                var timer2 = new Timer("timer2", "delay-time-2", "timer-name-2", "countdown-box-2", "/static/sound/alarm.mp3", "start-button-2");
                var timer3 = new Timer("timer3", "delay-time-3", "timer-name-3", "countdown-box-3", "/static/sound/alarm.mp3", "start-button-3");
                var timer4 = new Timer("timer4", "delay-time-4", "timer-name-4", "countdown-box-4", "/static/sound/alarm.mp3", "start-button-4");

                // Register timers
                timers.addTimer(timer1);
                timers.addTimer(timer2);
                timers.addTimer(timer3);
                timers.addTimer(timer4);
                """
            )
        )
    )

# endpoint strictly for setting media type for the audio file (not used for displaying anything)
@rt("/static/{path:path}")
def static_files(path: str):
    return FileResponse(f"app/static/{path}", media_type="audio/mpeg")


if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5010) # type: ignore