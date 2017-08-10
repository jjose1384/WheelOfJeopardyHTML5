/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var timerInSeconds;

function CountdownTimer(timer)
{
    timerInSeconds = timer;
}

CountdownTimer.prototype = {

    startCountdownTimer: function()
    { 
        var outputId = "timer";
        var x = setInterval(function () {    
            // Display the result in the element with outputId
            document.getElementById(outputId).innerHTML = timerInSeconds;

            // If the count down is finished, write some text 
            if (timerInSeconds <= 0) {
                clearInterval(x);
                document.getElementById(outputId).innerHTML = "EXPIRED";
                
                // play timeup sound
                var audio = new Audio('sound/timeUp.mp3');
                audio.play();
            }

            timerInSeconds--;

        }, 1000);
    }

};


