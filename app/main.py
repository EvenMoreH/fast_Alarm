from fasthtml.common import * # type: ignore
from fasthtml.common import (Form, Fieldset, Label, Input, Button, Html, Head, Body, Div, P, Title, Titled, A, Link, Audio ,FileResponse)
from starlette.responses import FileResponse

# for docker
# app, rt = fast_app(static_path="static") # type: ignore

# for local
app, rt = fast_app(static_path="app/static", debug=True) # type: ignore


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
                        H1("Timer #1"),
                        Form(
                            Input(type="number", name="time", id="delay-time-1", placeholder="Time (minutes)",
                                style="width: clamp(150px, 20vw, 350px);")
                        ),
                    ),
                    Div(
                        Button("Start Timer #1", onclick="timer1.playAudio()"),
                        Button("Stop Timer #1", onclick="timer1.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-1", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="separator"),
                Div(
                    Div(
                        H1("Timer #2"),
                        Form(
                            Input(type="number", name="time", id="delay-time-2", placeholder="Time (minutes)",
                                style="width: clamp(150px, 20vw, 350px);")
                        ),
                    ),
                    Div(
                        Button("Start Timer #2", onclick="timer2.playAudio()"),
                        Button("Stop Timer #2", onclick="timer2.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-2", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="separator"),
                Div(
                    Div(
                        H1("Timer #3"),
                        Form(
                            Input(type="number", name="time", id="delay-time-3", placeholder="Time (minutes)",
                                style="width: clamp(150px, 20vw, 350px);")
                        ),
                    ),
                    Div(
                        Button("Start Timer #3", onclick="timer3.playAudio()"),
                        Button("Stop Timer #3", onclick="timer3.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-3", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="separator"),
                Div(
                    Div(
                        H1("Timer #4"),
                        Form(
                            Input(type="number", name="time", id="delay-time-4", placeholder="Time (minutes)",
                                style="width: clamp(150px, 20vw, 350px);"),
                        ),
                    ),
                    Div(
                        Button("Start Timer #4", onclick="timer4.playAudio()"),
                        Button("Stop Timer #4", onclick="timer4.cancelCountdown()"),
                        cls="buttonGrid",
                    ),
                    Div(id="countdown-box-4", cls="buttonGrid", style="margin-top: 1vw"),
                ),
                Div(cls="separator"),
                cls="row",
            ),
            Div(
                Button("Reset All", onclick="timers.cancelAll()", style="margin-top: 4rem"),
                cls="buttonGrid",
            ),

            # GPT enhanced script to manage timers:
            Script(
                """
                function Timer(timerId, inputId, boxId, audioSrc) {
                    this.timerId = timerId;
                    this.inputId = inputId;
                    this.boxId = boxId;
                    this.audioSrc = audioSrc;
                    this.countdownInterval = null;
                    this.isCancelled = false;
                    this.audio = null;

                    this.playAudio = function () {
                        var delayInput = document.getElementById(this.inputId);
                        var delay = parseInt(delayInput.value * 60) || 0; // Get delay in minutes
                        var countdownBox = document.getElementById(this.boxId);

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
                                countdownBox.textContent = "Cancelled!";
                                this.stopAudio(); // Stop audio playback if playing
                                return;
                            }

                            remainingTime -= 1;
                            if (remainingTime <= 0) {
                                clearInterval(this.countdownInterval); // Stop countdown
                                countdownBox.textContent = "Time's Up!";
                                this.audio.play(); // Play the audio
                            } else {
                                countdownBox.textContent = this.formatTime(remainingTime); // Update display
                            }
                        }, 1000); // Update every second
                    };

                    this.cancelCountdown = function () {
                        this.isCancelled = true; // Set cancel flag
                        clearInterval(this.countdownInterval); // Stop the interval
                        this.stopAudio(); // Stop audio playback if playing

                        var countdownBox = document.getElementById(this.boxId);
                        var delayInput = document.getElementById(this.inputId);

                        countdownBox.textContent = "Cancelled!"; // Update the countdown box

                        // Clear the input field
                        delayInput.value = "";

                        // Set a timeout to clear the text after 5 seconds
                        setTimeout(() => {
                            countdownBox.textContent = ""; // Clear the text
                        }, 5000); // 5000 milliseconds = 5 seconds
                    };

                    this.stopAudio = function () {
                        if (this.audio && !this.audio.paused) {
                            this.audio.pause(); // Pause the audio
                            this.audio.currentTime = 0; // Reset the audio playback position
                        }
                    };

                    this.formatTime = function (timeInSeconds) {
                        var hours = Math.floor(timeInSeconds / 3600);
                        var minutes = Math.floor((timeInSeconds % 3600) / 60);
                        var seconds = timeInSeconds % 60;

                        if (hours > 0) {
                            return `${hours}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
                        } else {
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
                            delayInput.value = "";
                        });
                    },
                };

                // Initialize timers
                var timer1 = new Timer("timer1", "delay-time-1", "countdown-box-1", "/static/sound/alarm.mp3");
                var timer2 = new Timer("timer2", "delay-time-2", "countdown-box-2", "/static/sound/alarm.mp3");
                var timer3 = new Timer("timer3", "delay-time-3", "countdown-box-3", "/static/sound/alarm.mp3");
                var timer4 = new Timer("timer4", "delay-time-4", "countdown-box-4", "/static/sound/alarm.mp3");

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


serve() # type: ignore